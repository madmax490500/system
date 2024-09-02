pipeline {
    agent any

    parameters {
        string(name : 'TAG_VERSION', defaultValue : '0.1', description : 'docker version tag')
    }

    environment {
        ECR_REPOSITORY = "docker-repo.igamepub.co.kr:443/deleteme"
        ECR_DOCKER_TAG = "${params.TAG_VERSION}"
        TARGET_USER = "gamepub"
        TARGET_SERVER = "192.168.0.36"
        CONTAINER_NAME = "deleteme"
        PORT = "8080"
        ENV_PARAM = "prod"
        
        // 메일발송 관련 전역 변수 정의
        JOB_RESULT = 'FAILURE'
        MAIL_FROM = 'system@gamepub.co.kr'
        MAIL_TO = 'jylee@gamepub.co.kr'
        MAIL_SUBJECT = ''
        MAIL_BODY = ''
    }

    stages {
                stage('Git') {
            steps {
                checkout([$class: 'GitSCM', branches: [[name: '*/main']], extensions: [], userRemoteConfigs: [[url: 'https://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@github.com/madmax490500/system.git']]])
            }
        }
        
       
        stage('Backend Build') {
            steps {
                
                sh 'echo ${ENV_PARAM}'
                sh '''#!/bin/bash
                    cat feed/Dockerfile | grep env
                    sed -i '' 's|env .*|env '${ENV_PARAM}'|' feed/Dockerfile
                    cat feed/Dockerfile | grep env
                    '''
                
                dir("$JENKINS_HOME/workspace/deleteme") {
                    sh 'docker build -t deleteme -f feed/Dockerfile .'
                    //sh 'docker build --platform linux/amd64 -t deleteme .'
                }
                sh 'docker tag deleteme docker-repo.igamepub.co.kr:443/deleteme:${ECR_DOCKER_TAG}'
                sh 'docker push docker-repo.igamepub.co.kr:443/deleteme:${ECR_DOCKER_TAG}'
            }
        }
     }
}