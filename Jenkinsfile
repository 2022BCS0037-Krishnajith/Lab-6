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

                sleep 5

                docker logs $CONTAINER
                '''
            }
        }

        stage('Wait for API') {
            steps {
                sh '''
                timeout=30

                while true
                do
                    STATUS=$(curl -s -o /dev/null -w "%{http_code}" http://$CONTAINER:$PORT/health || true)

                    echo "STATUS=$STATUS"

                    if [ "$STATUS" = "200" ]; then
                        echo "API READY"
                        break
                    fi

                    if [ "$timeout" -le 0 ]; then
                        echo "FAILED"
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
                curl -X POST http://$CONTAINER:$PORT/predict \
                -H "Content-Type: application/json" \
                -d @tests/valid_input.json
                '''
            }
        }
    }

    post {
        always {
            sh 'docker rm -f $CONTAINER || true'
        }
    }
}s