pipeline {
    agent any

    environment {
        IMAGE = "kj3748/lab6-model:latest"
        CONTAINER = "wine-test-container"
        NETWORK = "jenkins-net"
        PORT = "8000"
    }

    stages {

        stage('Pull Image') {
            steps {
                sh '''
                echo "Pulling Docker image..."
                docker pull $IMAGE
                '''
            }
        }

        stage('Create Network') {
            steps {
                sh '''
                docker network create $NETWORK || true
                docker network connect $NETWORK jenkins || true
                '''
            }
        }

        stage('Run Container') {
            steps {
                sh '''
                echo "Starting container..."

                docker rm -f $CONTAINER || true

                docker run -d \
                    --name $CONTAINER \
                    --network $NETWORK \
                    $IMAGE

                docker ps
                '''
            }
        }

        stage('Wait for API Readiness') {
            steps {
                sh '''
                echo "Waiting for API..."

                timeout=30

                while true
                do
                    STATUS=$(curl -s -o /dev/null -w "%{http_code}" http://$CONTAINER:$PORT/health)

                    if [ "$STATUS" = "200" ]; then
                        echo "API is ready"
                        break
                    fi

                    if [ "$timeout" -le 0 ]; then
                        echo "API failed to start"
                        docker logs $CONTAINER
                        exit 1
                    fi

                    sleep 2
                    timeout=$((timeout-2))
                done
                '''
            }
        }

        stage('Valid Inference Test') {
            steps {
                sh '''
                echo "Testing valid input..."

                response=$(curl -s -X POST http://$CONTAINER:$PORT/predict \
                -H "Content-Type: application/json" \
                -d @tests/valid_input.json)

                echo "Response: $response"

                echo $response | jq '.prediction' > /dev/null

                if [ $? -ne 0 ]; then
                    echo "Prediction missing"
                    exit 1
                fi
                '''
            }
        }

        stage('Invalid Input Test') {
            steps {
                sh '''
                echo "Testing invalid input..."

                status=$(curl -s -o /dev/null -w "%{http_code}" \
                -X POST http://$CONTAINER:$PORT/predict \
                -H "Content-Type: application/json" \
                -d @tests/invalid_input.json)

                echo "Status: $status"

                if [ "$status" = "200" ]; then
                    echo "Invalid input test failed"
                    exit 1
                fi
                '''
            }
        }

        stage('Stop Container') {
            steps {
                sh '''
                docker stop $CONTAINER
                docker rm $CONTAINER
                '''
            }
        }
    }

    post {
        always {
            sh 'docker rm -f $CONTAINER || true'
        }
    }
}