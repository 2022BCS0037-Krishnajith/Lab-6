pipeline {
    agent any

    environment {
        IMAGE_NAME = "kj3748/lab6-model"
        CONTAINER_NAME = "wine_container_test"
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
                docker rm -f $CONTAINER_NAME || true
<<<<<<< HEAD
                docker run -d --network jenkins-net --name $CONTAINER_NAME $IMAGE_NAME
=======
                docker run -d -p 8000:8000 --name $CONTAINER_NAME $IMAGE_NAME
>>>>>>> 69c8e33 (final)
                '''
            }
        }

<<<<<<< HEAD
        stage('Wait for Service Readiness') {
=======
        stage('Wait for Service') {
>>>>>>> 69c8e33 (final)
            steps {
                script {
                    sleep(10)
                }
            }
        }

        stage('Send Valid Inference Request') {
<<<<<<< HEAD
    steps {
        script {

            def container_ip = sh(
    script: "docker inspect -f '{{ .NetworkSettings.Networks.jenkins-net.IPAddress }}' $CONTAINER_NAME",
    returnStdout: true
).trim()

            echo "Container IP: ${container_ip}"

            def response = sh(
                script: """
                curl -s -X POST http://${container_ip}:8000/predict \
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

           def container_ip = sh(
    script: "docker inspect -f '{{ .NetworkSettings.Networks.jenkins-net.IPAddress }}' $CONTAINER_NAME",
    returnStdout: true
).trim()

            def response = sh(
                script: """
                curl -s -X POST http://${container_ip}:8000/predict \
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
=======
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
>>>>>>> 69c8e33 (final)

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
