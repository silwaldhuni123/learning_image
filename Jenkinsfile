pipeline {
    agent any
    stages{
        stages("build"){
            steps{
                echo 'buliding the app'
                pip install -r requirements.txt
            }
        }
        stages("testing"){
            steps{
                echo 'testing app'
            }
        }
    }
}