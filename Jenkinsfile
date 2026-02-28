pipeline {
    agent any

    environment {
        IMAGE = "kj3748/lab6-model:latest"
        CONTAINER = "wine-test-container"
        NETWORK = "jenkins-net"
        PORT = "5000"
    }

    stages {

        stage('Pull Image') {
            steps {
                sh 'docker pull $IMAGE'
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
                timeout=30

                while true
                do
                    STATUS=$(curl -s -o /dev/null -w "%{http_code}" http://$CONTAINER:$PORT/health)

                    if [ "$STATUS" = "200" ]; then
                        echo "API is ready"
                        break
                    fi

                    if [ "$timeout" -le 0 ]; then
                        echo "API failed"
                        docker logs $CONTAINER
                        exit 1
                    fi

                    sleep 2
                    timeout=$((timeout-2))
                done
                '''
            }
        }

        stage('Valid Test') {
            steps {
                sh '''
                response=$(curl -s -X POST http://$CONTAINER:$PORT/predict \
                -H "Content-Type: application/json" \
                -d @tests/valid_input.json)

                echo $response | jq '.prediction' > /dev/null
                '''
            }
        }

        stage('Invalid Test') {
            steps {
                sh '''
                status=$(curl -s -o /dev/null -w "%{http_code}" \
                -X POST http://$CONTAINER:$PORT/predict \
                -H "Content-Type: application/json" \
                -d @tests/invalid_input.json)

                if [ "$status" = "200" ]; then
                    exit 1
                fi
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