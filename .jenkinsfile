#!groovy

def always_email = "xander@nx-solutions.com" // comma separated

pipeline {
  stages {
    stage('Environment'){
      steps{
        ansiColor('xterm') {
          sh '''#!/usr/bin/env bash
            ls -la
          '''
        }
      }
    }
  }
  post {
    cleanup{
      cleanWs()
    }
  }
}
