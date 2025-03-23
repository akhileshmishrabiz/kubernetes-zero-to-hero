# Deploying Craftista Microservices with ArgoCD

This guide explains how to deploy the Craftista Origami application to a Kubernetes cluster using ArgoCD.

## Prerequisites

- Minikube or any Kubernetes cluster running
- ArgoCD installed on the cluster
- kubectl configured to access your cluster
- Git repository with the application code and manifests

## Repository Structure

The repository should be structured as follows for ArgoCD:

```
microservices-on-k8s/
├── k8s-manifests/
│   ├── kustomization.yaml
│   ├── namespace.yaml
│   ├── catalogue-service.yaml
│   ├── frontend-service.yaml
│   ├── recommendation-service.yaml
│   ├── voting-service.yaml
│   └── ingress.yaml
└── argocd/
    └── application.yaml
```

## Deployment Steps

### 1. Install ArgoCD (if not already installed)

```bash
# Create ArgoCD namespace
kubectl create namespace argocd

# Install ArgoCD
kubectl apply -n argocd -f https://raw.githubusercontent.com/argoproj/argo-cd/stable/manifests/install.yaml

# Access ArgoCD UI
kubectl port-forward svc/argocd-server -n argocd 8080:443
```

The default admin username is `admin`. To get the password:

```bash
kubectl -n argocd get secret argocd-initial-admin-secret -o jsonpath="{.data.password}" | base64 -d
```

### 2. Apply the ArgoCD Application Manifest

```bash
kubectl apply -f argocd/application.yaml
```

### 3. Verify Deployment

1. Check the ArgoCD UI to see if the application is syncing correctly.
2. Check the deployments and pods in the craftista namespace:

```bash
kubectl get all -n craftista
```

### 4. Access the Application

If using Minikube:

```bash
# Get Minikube IP
minikube ip

# Add to /etc/hosts
echo "$(minikube ip) craftista.local" | sudo tee -a /etc/hosts

# Enable Ingress addon if not already enabled
minikube addons enable ingress

# Access the application at:
# http://craftista.local
```

## Updating the Application

To update the application:

1. Make changes to your application code or Kubernetes manifests
2. Commit and push the changes to the Git repository 
3. ArgoCD will automatically detect the changes and sync the application based on the syncPolicy defined in the Application resource

## Troubleshooting

If there are issues with the deployment:

1. Check ArgoCD logs:
```bash
kubectl logs -n argocd deploy/argocd-application-controller
```

2. Check the pod logs for specific microservices:
```bash
kubectl logs -n craftista deploy/catalogue-service
kubectl logs -n craftista deploy/frontend-service 
kubectl logs -n craftista deploy/recommendation-service
kubectl logs -n craftista deploy/voting-service
```

3. Verify the ConfigMaps and Secrets:
```bash
kubectl get configmaps -n craftista
kubectl get secrets -n craftista
```


4. fix the aws creds issue 
```bash
kubectl create secret generic aws-credentials \
  --from-literal=aws_access_key_id=AWS_ACCESS_KEY \
  --from-literal=aws_secret_access_key=AWS_SECERT_KEY \
  -n craftista
```