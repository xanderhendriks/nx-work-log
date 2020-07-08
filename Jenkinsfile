pipeline {
    agent any
    stages {
        stage('Environment') {
            steps{
                sh '''#!/usr/bin/env bash
                      ls -la
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
