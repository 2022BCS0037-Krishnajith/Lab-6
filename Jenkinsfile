pipeline {
    agent any

    environment {
        IMAGE_NAME = "kj3748/lab6-model"
        CONTAINER_NAME = "wine_container_test"
        PORT = "8000"
    }

    stages {

        stage('Pull Image') {
            steps {
                sh 'docker pull $IMAGE_NAME'
            }
        }

        stage('Run Container') {
            steps {
                sh '''
                docker run -d -p 8000:8000 --name $CONTAINER_NAME $IMAGE_NAME
                '''
            }
        }

        stage('Wait for Service Readiness') {
            steps {
                script {
                    sleep(10)
                }
            }
        }

        stage('Send Valid Inference Request') {
            steps {
                script {
                    def response = sh(
                        script: """
                        curl -s -X POST http://host.docker.internal:8000/predict \
                        -H "Content-Type: application/json" \
                        -d @test_valid.json
                        """,
                        returnStdout: true
                    ).trim()

                    echo "Valid Response: ${response}"

                    if (!response.contains("wine_quality")) {
                        error("Valid inference test failed!")
                    }
                }
            }
        }

        stage('Send Invalid Request') {
            steps {
                script {
                    def response = sh(
                        script: """
                        curl -s -X POST http://host.docker.internal:8000/predict \
                        -H "Content-Type: application/json" \
                        -d @test_invalid.json
                        """,
                        returnStdout: true
                    ).trim()

                    echo "Invalid Response: ${response}"

                    if (!response.contains("detail")) {
                        error("Invalid input test failed!")
                    }
                }
            }
        }

        stage('Stop Container') {
            steps {
                sh '''
                docker stop $CONTAINER_NAME
                docker rm $CONTAINER_NAME
                '''
            }
        }
    }
}
