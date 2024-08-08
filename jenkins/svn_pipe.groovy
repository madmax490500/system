pipeline {
    agent any

    parameters {
        string(name: 'RGAME_SERVERS', defaultValue: '1.1.1.1,2.2.2.2', description: '게임서버 IP주소 , 로 구분')
        string(name: 'RCHAT_SERVERS', defaultValue: '3.3.3.3,4.4.4.4', description: '채팅서버 IP주소 , 로 구분')
    }

    environment {
        TARGET_USER = "rocky"
        ENV_PARAM = "prod"
        JOB_RESULT = 'FAILURE'
        MAIL_FROM = 'system@gamepub.co.kr'
        MAIL_TO = 'system@gamepub.co.kr'
        MAIL_SUBJECT = ''
        MAIL_BODY = ''
        DEPLORY_NAME = 'live'
        PROJECT_NAME = 'pr'
        
        RADMIN_SERVER = "3.3.3.3"
        RGAME_SERVERS = "${params.RGAME_SERVERS}"
        RCHAT_SERVERS = "${params.RCHAT_SERVERS}"
        RSCHEDULE_SERVER = "5.5.5.5"
        RSHELL_SERVER = "6.6.6.6"
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
                                remote: 'svn://192.168.1.2/ProjectR/Live/Build' // SVN 저장소 URL
                            ]
                        ],
                        workspaceUpdater: [$class: 'UpdateUpdater']
                    ])
                }
            }
        }
        
        stage('Dotnet Build') {
            steps {
                // Dotnet Core 프로젝트를 빌드합니다.
                sh "dotnet --info"
                sh "cd ./Build/ServerPublish && chmod +x build.sh && ./build.sh ${DEPLORY_NAME}" //개발팀에서 아직 shell 에서 실행하기를 원함
            }
        }
        
        stage('Execute Balance Data Zip') {
            steps {
                // Balance Data Zip 파일 생성
                dir("$JENKINS_HOME/workspace/projectr-docker-live-balancedata/Build/ServerPublish/publish/rgame/BalanceData/") {
                    sh "tar -czf balancedata.tar.gz *"
                    sh "pwd"
                }
            }
        }
        
        stage('Transfer File') {
           parallel{
               stage('radmin-transfer'){
                    steps {
                        script {
                            // 파일 전송
                            def servers = RADMIN_SERVER.split(',')
                            servers.each { server ->
                                sshagent(credentials: ['projectr-aws']) {
                                    // SCP를 사용하여 파일 전송
                                    sh "scp -o UserKnownHostsFile=/dev/null -o StrictHostKeyChecking=no -r $JENKINS_HOME/workspace/projectr-docker-live-balancedata/Build/ServerPublish/publish/rgame/BalanceData/balancedata.tar.gz ${TARGET_USER}@${server}:~/"
                                    echo "radmin transferred"
                                }
                            }
                        }
                    }
               }
               stage('rgame-transfer'){
                    steps {
                        script {
                            // 파일 전송
                            def servers = RGAME_SERVERS.split(',')
                            servers.each { server ->
                                sshagent(credentials: ['projectr-aws']) {
                                    // SCP를 사용하여 파일 전송
                                    sh "scp -o UserKnownHostsFile=/dev/null -o StrictHostKeyChecking=no -r $JENKINS_HOME/workspace/projectr-docker-live-balancedata/Build/ServerPublish/publish/rgame/BalanceData/balancedata.tar.gz ${TARGET_USER}@${server}:~/"
                                    echo "rgame transferred"
                                }
                            }
                        }
                    }
               }
               stage('rchat-transfer'){
                    steps {
                        script {
                            // 파일 전송
                            def servers = RCHAT_SERVERS.split(',')
                            servers.each { server ->
                                sshagent(credentials: ['projectr-aws']) {
                                    // SCP를 사용하여 파일 전송
                                    sh "scp -o UserKnownHostsFile=/dev/null -o StrictHostKeyChecking=no -r $JENKINS_HOME/workspace/projectr-docker-live-balancedata/Build/ServerPublish/publish/rgame/BalanceData/balancedata.tar.gz ${TARGET_USER}@${server}:~/"
                                    echo "rchat transferred"
                                }
                            }
                        }
                    }
               }
               stage('rshell-transfer'){
                    steps {
                        script {
                            // 파일 전송
                            def servers = RSHELL_SERVER.split(',')
                            servers.each { server ->
                                sshagent(credentials: ['projectr-aws']) {
                                    // SCP를 사용하여 파일 전송
                                    sh "scp -o UserKnownHostsFile=/dev/null -o StrictHostKeyChecking=no -r $JENKINS_HOME/workspace/projectr-docker-live-balancedata/Build/ServerPublish/publish/rgame/BalanceData/balancedata.tar.gz ${TARGET_USER}@${server}:~/"
                                    echo "rshell transferred"
                                }
                            }
                        }
                    }
               }
               stage('rscheduler-transfer'){
                    steps {
                        script {
                            // 파일 전송
                            def servers = RSCHEDULE_SERVER.split(',')
                            servers.each { server ->
                                sshagent(credentials: ['projectr-aws']) {
                                    // SCP를 사용하여 파일 전송
                                    sh "scp -o UserKnownHostsFile=/dev/null -o StrictHostKeyChecking=no -r $JENKINS_HOME/workspace/projectr-docker-live-balancedata/Build/ServerPublish/publish/rgame/BalanceData/balancedata.tar.gz ${TARGET_USER}@${server}:~/"
                                    echo "rscheduler transferred"
                                }
                            }
                        }
                    }
               }
           }
        }

        stage('Execute Balance Data Unzip ') {
            parallel{
               stage('radmin-unzip'){
                    steps {
                        script {
                            // 파일 전송
                            def servers = RADMIN_SERVER.split(',')
                            servers.each { server ->
                                sshagent(credentials: ["projectr-aws"]) {
                                    sh """#!/bin/bash
                                        ssh -o UserKnownHostsFile=/dev/null -o StrictHostKeyChecking=no \
                                        ${TARGET_USER}@${server} \
                                        'export NAME=radmin; \
                                        export PROJECT_NAME='${PROJECT_NAME}'; \
                                        export DEPLORY_NAME='${DEPLORY_NAME}'; \
                                        ./deploy.sh';
                                        """
                                    echo "radmin is unzipped"
                                }
                            }
                        }
                    }
               }
              stage('rgame-unzip'){
                    steps {
                        script {
                            // 파일 전송
                            def servers = RGAME_SERVERS.split(',')
                            servers.each { server ->
                                sshagent(credentials: ["projectr-aws"]) {
                                    sh """#!/bin/bash
                                        ssh -o UserKnownHostsFile=/dev/null -o StrictHostKeyChecking=no \
                                        ${TARGET_USER}@${server} \
                                        'export NAME=rgame; \
                                        export PROJECT_NAME='${PROJECT_NAME}'; \
                                        export DEPLORY_NAME='${DEPLORY_NAME}'; \
                                        ./deploy.sh';
                                        """
                                    echo "rgame is unzipped"
                                }
                            }
                        }
                    }
               }
              stage('rchat-unzip'){
                    steps {
                        script {
                            // 파일 전송
                            def servers = RCHAT_SERVERS.split(',')
                            servers.each { server ->
                                sshagent(credentials: ["projectr-aws"]) {
                                    sh """#!/bin/bash
                                        ssh -o UserKnownHostsFile=/dev/null -o StrictHostKeyChecking=no \
                                        ${TARGET_USER}@${server} \
                                        'export NAME=rchat; \
                                        export PROJECT_NAME='${PROJECT_NAME}'; \
                                        export DEPLORY_NAME='${DEPLORY_NAME}'; \
                                        ./deploy.sh';
                                        """
                                    echo "rchat is unzipped"
                                    
                                }
                            }
                        }
                    }
               }
              stage('rshell-unzip'){
                    steps {
                        script {
                            // 파일 전송
                            def servers = RSHELL_SERVER.split(',')
                            servers.each { server ->
                                sshagent(credentials: ["projectr-aws"]) {
                                    sh """#!/bin/bash
                                        ssh -o UserKnownHostsFile=/dev/null -o StrictHostKeyChecking=no \
                                        ${TARGET_USER}@${server} \
                                        'export NAME=rshell; \
                                        export PROJECT_NAME='${PROJECT_NAME}'; \
                                        export DEPLORY_NAME='${DEPLORY_NAME}'; \
                                        ./deploy.sh';
                                        """
                                    echo "rshell is unzipped"
                                }
                            }
                        }
                    }
              }
              stage('rscheduler-unzip'){
                    steps {
                        script {
                            // 파일 전송
                            def servers = RSCHEDULE_SERVER.split(',')
                            servers.each { server ->
                                sshagent(credentials: ["projectr-aws"]) {
                                    sh """#!/bin/bash
                                        ssh -o UserKnownHostsFile=/dev/null -o StrictHostKeyChecking=no \
                                        ${TARGET_USER}@${server} \
                                        'export NAME=rscheduler; \
                                        export PROJECT_NAME='${PROJECT_NAME}'; \
                                        export DEPLORY_NAME='${DEPLORY_NAME}'; \
                                        ./deploy.sh';
                                        """
                                    echo "rscheduler is unzipped"
                                    
                                }
                            }
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

