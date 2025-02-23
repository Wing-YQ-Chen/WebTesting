pipeline {
	agent any
    stages {

		stage('Build') {
			steps {
				bat """
				mvn clean validate test-compile
                """

            }
        }


		stage('Run Testing') {
			steps {
				bat """
				mvn test
				"""
			}
			post {
				always {
					archiveArtifacts artifacts: 'reports/cucumber-reports.html', allowEmptyArchive: true
				}
			}
		}

    }
}
