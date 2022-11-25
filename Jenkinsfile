pipeline {
    agent any
    stages{
        stage("build"){
            steps{
                echo 'buliding the app'
                pip install -r requirements.txt
            }
        }
        stage("testing"){
            steps{
                echo 'testing app'
            }
        }
    }
}