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
		}
    }
}
