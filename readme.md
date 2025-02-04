To install database agent for appDynamics configuration below steps needs to be followed.

1. Create the separate namespace for database agent.
        kubectl create namespace appdynamics-db

2. Follow below commands to install state files.
        kubectl apply -f appd-db-agent-config.yaml
        kubectl apply -f appd-db-agent-deployment.yaml
        kubectl apply -f appd-db-agent-service.yml    

3. Verify the installation by querying the POD.
        kubectl get pods --namespace=appdynamics-db

4. To stop/bring down the POD run below command.
        kubectl scale deployment appd-db-agent --replicas=0 -n appdynamics-db                    