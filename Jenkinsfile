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

        stage('Run Container') {
            steps {
                sh '''
                echo "Starting container..."

                docker rm -f $CONTAINER || true

                docker network create $NETWORK || true

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
                echo "Waiting for API to become ready..."

                timeout=30

                while true
                do
                    STATUS=$(docker exec $CONTAINER curl -s -o /dev/null -w "%{http_code}" http://localhost:$PORT/health)

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
                echo "Sending valid inference request..."

                response=$(docker exec $CONTAINER curl -s -X POST http://localhost:$PORT/predict \
                -H "Content-Type: application/json" \
                -d @tests/valid_input.json)

                echo "Response: $response"

                echo $response | jq '.prediction' > /dev/null

                if [ $? -ne 0 ]; then
                    echo "Prediction field missing"
                    exit 1
                fi

                echo "Valid inference test passed"
                '''
            }
        }

        stage('Invalid Input Test') {
            steps {
                sh '''
                echo "Sending invalid inference request..."

                status=$(docker exec $CONTAINER curl -s -o /dev/null -w "%{http_code}" \
                -X POST http://localhost:$PORT/predict \
                -H "Content-Type: application/json" \
                -d @tests/invalid_input.json)

                echo "Status code: $status"

                if [ "$status" = "200" ]; then
                    echo "Invalid input test failed"
                    exit 1
                fi

                echo "Invalid input correctly rejected"
                '''
            }
        }

        stage('Stop Container') {
            steps {
                sh '''
                echo "Stopping container..."

                docker stop $CONTAINER
                docker rm $CONTAINER

                echo "Container stopped and removed"
                '''
            }
        }
    }

    post {
        always {
            sh '''
            docker rm -f $CONTAINER || true
            '''
        }

        success {
            echo "Pipeline completed successfully"
        }

        failure {
            echo "Pipeline failed"
        }
    }
}s