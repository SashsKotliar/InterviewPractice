# Rick and Morty Character API & DevOps Pipeline

This repository contains a DevOps engineering exercise that queries the Rick and Morty API to find specific characters, writes the results to a CSV file, and serves the data via a containerized REST API. 

The project includes containerization (Docker), local Kubernetes manifests, a scalable Helm chart, and a fully automated CI/CD pipeline using GitHub Actions.

## 1. Project Overview & Base Requirements

The core application is a Python script using Flask. 
When executed (or when the API endpoint is called), it queries the [Rick and Morty REST API](https://rickandmortyapi.com/documentation/#rest) for characters matching the following criteria:
* **Species:** Human
* **Status:** Alive
* **Origin:** Earth

It parses the JSON response and generates a local file named `alive-earth-humans.csv` containing the character's Name, Location, and Image Link.

## 2. Dockerizing as a Service

The application is containerized using a lightweight Python image. It runs as a Flask web service that generates the CSV locally and returns the exact same data as a JSON response.

### How to Build the Docker Image and run the code:
Navigate to the root directory and run:

* podman build -t rick-and-morty-api:latest .
* podman run -p 5000:5000 -v $(pwd)/app:/app rick-and-morty-api

### REST API Endpoints:
* Healthcheck: 
    curl http://localhost:5000/healthcheck
* Get data: 
    curl http://localhost:5000/api/characters/earth-humans

### Kubernetes deployment:
The application can be deployed to a local Kubernetes cluster (like Minikube or microk8s) using the raw YAML manifests located in the `yamls/` folder
* Start a minikube: 
    minikube start --driver=podman
* Load the local image into the cluster cache: 
    minikube image load localhost/rick-and-morty-api:latest
* Apply manifests: 
    kubectl apply -f yamls/ -n rick-morty
* Access app via port-forwarding/minikube tunnel

### Helm deployment:

* Install the release: 
    helm install rick-morty-release ./helm/rick-morty-api -n rick-morty --create-namespace
* Verify: 
    helm list -n rick-morty
    kubectl get pods -n rick-morty
    

### Github actions:
This repository includes a fully automated CI/CD workflow (`.github/workflows/ci.yaml`) that triggers on every push request to the main branch. 
The pipeline consists of a single job (`build-and-deploy`) running on an `ubuntu-latest` runner. 
It ensures the application can be built, deployed, and tested in a clean environment automatically.
For running the pipeline - update the changes and push them to the repository.