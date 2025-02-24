pipeline {
	agent any
    stages {

        stage('Build') {
			steps {
				bat """
				echo "Building"
				rmdir /s /q "Execution"
                python -m venv venv
                call venv\\Scripts\\activate
                pip list
                pip install -r requirements.txt.txt -i "https://mirrors.aliyun.com/pypi/simple/"
                pip list
                pyinstaller -p . -F "DemoScript\\main.py" -n "main.exe" --distpath "Execution\\Run" --workpath "Temp\\Build"
                """

            }
        }


		stage('Run Testing') {
			steps {
				bat """
				echo "Run Testing"
				cd Execution\\Run
				main.exe
				"""
			}
			post {
				always {
					archiveArtifacts artifacts: 'Execution\\**', allowEmptyArchive: true
				}
			}
		}
    }
}