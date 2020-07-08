pipeline {
    agent any
    stages {
        stage('Environment') {
            steps{
                sh '''#!/usr/bin/env bash
                      ls -la
                      cat Jenkinsfile
                   '''
            }
        }
    }
    post {
        cleanup {
            cleanWs()
        }
    }
}
