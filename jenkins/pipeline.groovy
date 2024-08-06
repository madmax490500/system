pipeline {
    agent any

    parameters {
        string(name : 'TAG_VERSION', defaultValue : '0.1', description : 'docker version tag')
    }

    environment {
        ECR_REPOSITORY = "docker-repo.idomain.co.kr:443/crm"
        ECR_DOCKER_TAG = "${params.TAG_VERSION}"
        TARGET_USER = "madmax00"
        TARGET_SERVER = "123.123.123.123"
        CONTAINER_NAME = "crm"
        PORT = "10002"
        ENV_PARAM = "prod"
        
        // 메일발송 관련 전역 변수 정의
        JOB_RESULT = 'FAILURE'
        MAIL_FROM = 'system@domain.co.kr'
        MAIL_TO = 'dev@domain.co.kr'
        MAIL_SUBJECT = ''
        MAIL_BODY = ''
    }

    stages {
                stage('Git') {
            steps {
                //checkout([$class: 'GitSCM', branches: [[name: '*/main']], extensions: [], userRemoteConfigs: [[url: 'https://token@github.com/domain/crm.git']]])
                checkout([$class: 'GitSCM', branches: [[name: '*/main']], extensions: [], userRemoteConfigs: [[url: 'https://token@github.com/domain/crm.git']]])
            }
        }
        
        stage('Frontend Build') {
            steps {
                dir("$JENKINS_HOME/workspace/crm/backend/dist") {
                    deleteDir()
                }
                dir("$JENKINS_HOME/workspace/crm/frontend") {
                    sh 'pnpm install'
                    sh 'pnpm build:stage'
                }
            }
        }
        
        stage('Backend Build') {
            steps {
                
                sh 'echo ${ENV_PARAM}'
                sh '''#!/bin/bash
                    cat backend/Dockerfile | grep env
                    sed -i '' 's|env .*|env '${ENV_PARAM}'|' backend/Dockerfile
                    cat backend/Dockerfile | grep env
                    '''
                
                dir("$JENKINS_HOME/workspace/crm/backend") {
                    sh 'docker build --platform linux/amd64 -t crm .'
                }
                sh 'docker tag crm docker-repo.idomain.co.kr:443/crm:${ECR_DOCKER_TAG}'
                sh 'docker push docker-repo.idomain.co.kr:443/crm:${ECR_DOCKER_TAG}'
            }
        }
        
        stage('Deploy') {
            steps{
                sshagent (credentials: ["registry-ssh"]) {
                    sh '''#!/bin/bash
                        ssh -o UserKnownHostsFile=/dev/null -o StrictHostKeyChecking=no \
                            ${TARGET_USER}@${TARGET_SERVER} \
                            'export IMAGE='${ECR_REPOSITORY}'; \
                            export TAG='${ECR_DOCKER_TAG}'; \
                            export CNAME='${CONTAINER_NAME}'-'${ECR_DOCKER_TAG}'; \
                            export PORT='${PORT}'; \
                            docker-compose -f crm/docker-compose.yml down; 
                            docker-compose -f crm/docker-compose.yml up -d';
                        '''
                    echo "complete"
                }
            }
        }
    }
    
    post {
        always {
            script {
                
                def buildUserId = ''
                
                wrap([$class: 'BuildUser']) {
                    buildUserId = "${BUILD_USER}"
                }
                
                MAIL_SUBJECT = "Jenkins 빌드 : ${env.JOB_NAME} ${params.TAG_VERSION} "
                MAIL_BODY = "JOB Name : ${env.JOB_NAME}\nVerion : ${params.TAG_VERSION}\nJOB URL : ${env.JOB_URL}\nBuild URL : ${env.BUILD_URL}\n작업자 : ${buildUserId}"
            }
        }

        success {
            script {
                MAIL_SUBJECT = "[성공] ${MAIL_SUBJECT}"
                MAIL_BODY = "${MAIL_BODY} \n결과 : Success"
                mail bcc: '', subject:"${MAIL_SUBJECT}", body: "${MAIL_BODY}", from: "${MAIL_FROM}",  to: "${MAIL_TO}" , cc: '', replyTo: ''
            }
        }

        failure {
            script {
                MAIL_SUBJECT = "[실패] ${MAIL_SUBJECT}"
                MAIL_BODY = "${MAIL_BODY} \n결과 : Fail"
                mail bcc: '', subject:"${MAIL_SUBJECT}", body: "${MAIL_BODY}", from: "${MAIL_FROM}", to: "${MAIL_TO}" , cc: '', replyTo: ''
            }
        }
    }
}