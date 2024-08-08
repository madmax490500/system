pipeline {
    agent any
    
    parameters {
        string(name: 'TAG_VERSION', defaultValue: '0.1', description: '도커 태그 버전\nx.x.패치버전 은 SVN리비전으로 자동 등록됨')
    }

    environment {
        TARGET_USER = "gamepub"
        TARGET_SERVER = "1.1.1.1"
        ENV_PARAM = "prod"
        JOB_RESULT = 'FAILURE'
        MAIL_FROM = 'system@gamepub.co.kr'
        MAIL_TO = 'system@gamepub.co.kr'
        MAIL_SUBJECT = ''
        MAIL_BODY = ''
        DEPLORY_NAME = 'inspection'
        PROJECT_NAME = 'pr'
    }
    
    stages {
        stage('Checkout Pull') {
            steps {
                script {
                    // SVN Checkout with embedded credentials
                    def checkoutInfo = checkout([
                        $class: 'SubversionSCM',
                        locations: [
                            [
                                credentialsId: 'svn-jenkins', // 자격 증명 ID 직접 입력
                                remote: 'svn://1.1.1.1/ProjectR/Live/Build' // SVN 저장소 URL
                            ]
                        ],
                        workspaceUpdater: [$class: 'UpdateUpdater']
                    ])

                    // Extracting SVN revision number
                    def svnRevision = checkoutInfo.SVN_REVISION
                    echo "SVN Revision: ${svnRevision}"
                    env.ECR_DOCKER_TAG = "${params.TAG_VERSION}.${svnRevision}"
                }
            }
        }
        
        stage('Dotnet Build') {
            steps {
                // Dotnet Core 프로젝트를 빌드합니다.
                sh "dotnet --info"
                sh "cd ./Build/ServerPublish && chmod +x build.sh && ./build.sh ${DEPLORY_NAME}"
            }
        }

        stage('Docker Build') {
            parallel {
                stage('radmin-image') {
                    steps {      
                        dir("$JENKINS_HOME/workspace/projectr-docker-inspection/Build/ServerPublish/publish/radmin/") {
                            sh 'docker build --platform linux/amd64 -t ${PROJECT_NAME}-${DEPLORY_NAME}-radmin .'
                        }
                        sh 'docker tag ${PROJECT_NAME}-${DEPLORY_NAME}-radmin docker-repo.igamepub.co.kr:443/${PROJECT_NAME}-${DEPLORY_NAME}-radmin:${ECR_DOCKER_TAG}'
                        sh 'docker push docker-repo.igamepub.co.kr:443/${PROJECT_NAME}-${DEPLORY_NAME}-radmin:${ECR_DOCKER_TAG}'
                    }
                }
                // Uncomment the following stages if needed
                stage('rgame-image') {
                    steps {      
                        dir("$JENKINS_HOME/workspace/projectr-docker-inspection/Build/ServerPublish/publish/rgame/") {
                            sh 'docker build --platform linux/amd64 -t ${PROJECT_NAME}-${DEPLORY_NAME}-rgame .'
                        }
                        sh 'docker tag ${PROJECT_NAME}-${DEPLORY_NAME}-rgame docker-repo.igamepub.co.kr:443/${PROJECT_NAME}-${DEPLORY_NAME}-rgame:${ECR_DOCKER_TAG}'
                        sh 'docker push docker-repo.igamepub.co.kr:443/${PROJECT_NAME}-${DEPLORY_NAME}-rgame:${ECR_DOCKER_TAG}'
                    }
                }
                stage('rchat-image') {
                    steps {      
                        dir("$JENKINS_HOME/workspace/projectr-docker-inspection/Build/ServerPublish/publish/rchat/") {
                            sh 'docker build --platform linux/amd64 -t ${PROJECT_NAME}-${DEPLORY_NAME}-rchat .'
                        }
                        sh 'docker tag ${PROJECT_NAME}-${DEPLORY_NAME}-rchat docker-repo.igamepub.co.kr:443/${PROJECT_NAME}-${DEPLORY_NAME}-rchat:${ECR_DOCKER_TAG}'
                        sh 'docker push docker-repo.igamepub.co.kr:443/${PROJECT_NAME}-${DEPLORY_NAME}-rchat:${ECR_DOCKER_TAG}'
                    }
                }
                stage('rscheduler-image') {
                    steps {      
                        dir("$JENKINS_HOME/workspace/projectr-docker-inspection/Build/ServerPublish/publish/rscheduler/") {
                            sh 'docker build --platform linux/amd64 -t ${PROJECT_NAME}-${DEPLORY_NAME}-rscheduler .'
                        }
                        sh 'docker tag ${PROJECT_NAME}-${DEPLORY_NAME}-rscheduler docker-repo.igamepub.co.kr:443/${PROJECT_NAME}-${DEPLORY_NAME}-rscheduler:${ECR_DOCKER_TAG}'
                        sh 'docker push docker-repo.igamepub.co.kr:443/${PROJECT_NAME}-${DEPLORY_NAME}-rscheduler:${ECR_DOCKER_TAG}'
                    }
                }
                stage('rshell-image') {
                    steps {      
                        dir("$JENKINS_HOME/workspace/projectr-docker-inspection/Build/ServerPublish/publish/rshell/") {
                            sh 'docker build --platform linux/amd64 -t ${PROJECT_NAME}-${DEPLORY_NAME}-rshell .'
                        }
                        sh 'docker tag ${PROJECT_NAME}-${DEPLORY_NAME}-rshell docker-repo.igamepub.co.kr:443/${PROJECT_NAME}-${DEPLORY_NAME}-rshell:${ECR_DOCKER_TAG}'
                        sh 'docker push docker-repo.igamepub.co.kr:443/${PROJECT_NAME}-${DEPLORY_NAME}-rshell:${ECR_DOCKER_TAG}'
                    }
                }
            }
        }
        
        stage('Docker Deploy') {
            parallel {
                stage('Deploy-radmin') {
                    environment {
                        ECR_REPOSITORY = "docker-repo.igamepub.co.kr:443/${PROJECT_NAME}-${DEPLORY_NAME}-radmin"
                        CONTAINER_NAME = "${PROJECT_NAME}-${DEPLORY_NAME}-radmin"
                        PORT = "30100"
                        COMPOSE_FILEPATH = "${DEPLORY_NAME}/radmin/docker-compose.yml"
                        VOLUME_NAME = "${PROJECT_NAME}-${DEPLORY_NAME}"
                    }
                    steps {
                        sshagent(credentials: ["projectr-test"]) {
                            sh '''#!/bin/bash
                                ssh -o UserKnownHostsFile=/dev/null -o StrictHostKeyChecking=no \
                                    ${TARGET_USER}@${TARGET_SERVER} \
                                    'export IMAGE='${ECR_REPOSITORY}'; \
                                    export TAG='${ECR_DOCKER_TAG}'; \
                                    export CNAME='${CONTAINER_NAME}'-'${ECR_DOCKER_TAG}'; \
                                    export PORT='${PORT}'; \
                                    export VOLUME_NAME='${VOLUME_NAME}'; \
                                    docker-compose -p '${CONTAINER_NAME}' -f '${COMPOSE_FILEPATH}' down; 
                                    docker-compose -p '${CONTAINER_NAME}' -f '${COMPOSE_FILEPATH}' up -d';
                                '''
                            echo "radmin is complete"
                        }
                    }
                }
                stage('Deploy-rgame') {
                    environment {
                        ECR_REPOSITORY = "docker-repo.igamepub.co.kr:443/${PROJECT_NAME}-${DEPLORY_NAME}-rgame"
                        CONTAINER_NAME = "${PROJECT_NAME}-${DEPLORY_NAME}-rgame"
                        PORT = "30000"
                        COMPOSE_FILEPATH = "${DEPLORY_NAME}/rgame/docker-compose.yml"
                        VOLUME_NAME = "${PROJECT_NAME}-${DEPLORY_NAME}"
                    }
                    steps {
                        sshagent(credentials: ["projectr-test"]) {
                            sh '''#!/bin/bash
                                ssh -o UserKnownHostsFile=/dev/null -o StrictHostKeyChecking=no \
                                    ${TARGET_USER}@${TARGET_SERVER} \
                                    'export IMAGE='${ECR_REPOSITORY}'; \
                                    export TAG='${ECR_DOCKER_TAG}'; \
                                    export CNAME='${CONTAINER_NAME}'-'${ECR_DOCKER_TAG}'; \
                                    export PORT='${PORT}'; \
                                    export VOLUME_NAME='${VOLUME_NAME}'; \
                                    docker-compose -p '${CONTAINER_NAME}' -f '${COMPOSE_FILEPATH}' down; 
                                    docker-compose -p '${CONTAINER_NAME}' -f '${COMPOSE_FILEPATH}' up -d';
                                '''
                            echo "rgame is complete"
                        }
                    }
                }
                stage('Deploy-rchat') {
                    environment {
                        ECR_REPOSITORY = "docker-repo.igamepub.co.kr:443/${PROJECT_NAME}-${DEPLORY_NAME}-rchat"
                        CONTAINER_NAME = "${PROJECT_NAME}-${DEPLORY_NAME}-rchat"
                        PORT = "30300"
                        COMPOSE_FILEPATH = "${DEPLORY_NAME}/rchat/docker-compose.yml"
                        VOLUME_NAME = "${PROJECT_NAME}-${DEPLORY_NAME}"
                    }
                    steps {
                        sshagent(credentials: ["projectr-test"]) {
                            sh '''#!/bin/bash
                                ssh -o UserKnownHostsFile=/dev/null -o StrictHostKeyChecking=no \
                                    ${TARGET_USER}@${TARGET_SERVER} \
                                    'export IMAGE='${ECR_REPOSITORY}'; \
                                    export TAG='${ECR_DOCKER_TAG}'; \
                                    export CNAME='${CONTAINER_NAME}'-'${ECR_DOCKER_TAG}'; \
                                    export PORT='${PORT}'; \
                                    export VOLUME_NAME='${VOLUME_NAME}'; \
                                    docker-compose -p '${CONTAINER_NAME}' -f '${COMPOSE_FILEPATH}' down; 
                                    docker-compose -p '${CONTAINER_NAME}' -f '${COMPOSE_FILEPATH}' up -d';
                                '''
                            echo "rchat is complete"
                        }
                    }
                }
                stage('Deploy-rshell') {
                    environment {
                        ECR_REPOSITORY = "docker-repo.igamepub.co.kr:443/${PROJECT_NAME}-${DEPLORY_NAME}-rshell"
                        CONTAINER_NAME = "${PROJECT_NAME}-${DEPLORY_NAME}-rshell"
                        PORT = "30400"
                        COMPOSE_FILEPATH = "${DEPLORY_NAME}/rshell/docker-compose.yml"
                        VOLUME_NAME = "${PROJECT_NAME}-${DEPLORY_NAME}"
                    }
                    steps {
                        sshagent(credentials: ["projectr-test"]) {
                            sh '''#!/bin/bash
                                ssh -o UserKnownHostsFile=/dev/null -o StrictHostKeyChecking=no \
                                    ${TARGET_USER}@${TARGET_SERVER} \
                                    'export IMAGE='${ECR_REPOSITORY}'; \
                                    export TAG='${ECR_DOCKER_TAG}'; \
                                    export CNAME='${CONTAINER_NAME}'-'${ECR_DOCKER_TAG}'; \
                                    export PORT='${PORT}'; \
                                    export VOLUME_NAME='${VOLUME_NAME}'; \
                                    docker-compose -p '${CONTAINER_NAME}' -f '${COMPOSE_FILEPATH}' down; 
                                    docker-compose -p '${CONTAINER_NAME}' -f '${COMPOSE_FILEPATH}' up -d';
                                '''
                            echo "rshell is complete"
                        }
                    }
                }
                stage('Deploy-rscheduler') {
                    environment {
                        ECR_REPOSITORY = "docker-repo.igamepub.co.kr:443/${PROJECT_NAME}-${DEPLORY_NAME}-rscheduler"
                        CONTAINER_NAME = "${PROJECT_NAME}-${DEPLORY_NAME}-rscheduler"
                        COMPOSE_FILEPATH = "${DEPLORY_NAME}/rscheduler/docker-compose.yml"
                        VOLUME_NAME = "${PROJECT_NAME}-${DEPLORY_NAME}"
                    }
                    steps {
                        sshagent(credentials: ["projectr-test"]) {
                            sh '''#!/bin/bash
                                ssh -o UserKnownHostsFile=/dev/null -o StrictHostKeyChecking=no \
                                    ${TARGET_USER}@${TARGET_SERVER} \
                                    'export IMAGE='${ECR_REPOSITORY}'; \
                                    export TAG='${ECR_DOCKER_TAG}'; \
                                    export CNAME='${CONTAINER_NAME}'-'${ECR_DOCKER_TAG}'; \
                                    export VOLUME_NAME='${VOLUME_NAME}'; \
                                    sed -i "/^ *ports:/,+1d" '${COMPOSE_FILEPATH}';
                                    docker-compose -p '${CONTAINER_NAME}' -f '${COMPOSE_FILEPATH}' down; 
                                    docker-compose -p '${CONTAINER_NAME}' -f '${COMPOSE_FILEPATH}' up -d';
                                '''
                            echo "rscheduler is complete"
                        }
                    }
                }
            }
        }
    }
    // 파이프라인 종료 후 작업을 정의할 수 있습니다.
    post {
        success {
            echo 'Pipeline executed successfully!'
        }
        
        failure {
            echo 'Pipeline failed!'
        }
    }
}

