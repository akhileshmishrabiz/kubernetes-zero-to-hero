
## Table of Contents
- [Table of Contents](#table-of-contents)
- [To run the app from docker compose app](#to-run-the-app-from-docker-compose-app)
- [Architecture Overview](#architecture-overview)
- [Deployment Requirements](#deployment-requirements)
  - [Service Dependencies](#service-dependencies)
  - [Network Configuration](#network-configuration)
- [Deployment Order](#deployment-order)
- [Example Kubernetes Configuration](#example-kubernetes-configuration)
- [Monitoring and Health Checks](#monitoring-and-health-checks)
- [Scaling Considerations](#scaling-considerations)


## To run the app from docker compose app
docker-compose up --build

## Architecture Overview

```
┌─────────────┐      ┌───────────────┐
│             │      │               │
│   Ingress   │─────▶│   Frontend    │
│             │      │               │
└─────────────┘      └───────┬───────┘
                             │
                             ▼
          ┌─────────────────┬─────────────────┐
          │                 │                 │
          ▼                 ▼                 ▼
┌─────────────────┐ ┌───────────────┐ ┌───────────────┐
│                 │ │               │ │               │
│   Catalogue     │ │Recommendation │ │    Voting     │
│                 │ │               │ │               │
└─────────────────┘ └───────────────┘ └───────────────┘
          │                                   ▲
          │                                   │
          └───────────────────────────────────┘
                 (Voting syncs from Catalogue)
```

## Deployment Requirements

### Service Dependencies

- **Frontend** depends on all backend services
- **Voting** depends on **Catalogue** for product data
- All services should be deployed in the same namespace

### Network Configuration

| Service | Port | Kubernetes Service Name |
|---------|------|-------------------------|
| Frontend | 3000 | frontend |
| Catalogue | 5000 | catalogue |
| Recommendation | 8080 | recco |
| Voting | 8080 | voting |

## Deployment Order

For initial deployment, follow this order:

1. Catalogue
2. Recommendation
3. Voting
4. Frontend

## Example Kubernetes Configuration

Here's an example `kustomization.yaml` to deploy all services:

```yaml
apiVersion: kustomize.config.k8s.io/v1beta1
kind: Kustomization

resources:
  - catalogue-deployment.yaml
  - catalogue-service.yaml
  - recommendation-deployment.yaml
  - recommendation-service.yaml
  - voting-deployment.yaml
  - voting-service.yaml
  - frontend-deployment.yaml
  - frontend-service.yaml
  - frontend-ingress.yaml

configMapGenerator:
  - name: catalogue-config
    files:
      - config.json=catalogue-config.json
  - name: recommendation-config
    files:
      - config.json=recommendation-config.json
  - name: frontend-config
    files:
      - config.json=frontend-config.json

secretGenerator:
  - name: db-secrets
    literals:
      - db_password=devops
```

## Monitoring and Health Checks

Each service exposes endpoints for health monitoring:

- Frontend: `/api/service-status`
- Catalogue: `/`
- Recommendation: `/api/recommendation-status`
- Voting: `/api/origamis`

## Scaling Considerations

- **Frontend** and **Catalogue** services may need more replicas during high traffic
- **Recommendation** service is less resource-intensive and can run with fewer replicas
- **Voting** service may require more careful scaling with proper database configuration