# Gnosari Documentation Kubernetes Deployment

This guide explains how to deploy the Gnosari AI Teams documentation using Kubernetes and Helm.

## Prerequisites

- Kubernetes cluster (1.18+)
- Helm 3.x installed
- Docker image pushed to a container registry
- kubectl configured to access your cluster

## Building and Pushing the Docker Image

First, build and push the documentation Docker image to your container registry:

```bash
# Build the Docker image
cd docs/
docker build -t your-registry/gnosari-docs:latest .

# Push to your registry
docker push your-registry/gnosari-docs:latest
```

## Deploying with Helm

### Quick Deployment

Deploy with default settings:

```bash
# Add your custom values
helm install gnosari-docs ./docs/chart \
  --set image.repository=your-registry/gnosari-docs \
  --set image.tag=latest
```

### Production Deployment

For production deployments, create a custom values file:

```bash
# Create production values file
cat > production-values.yaml << EOF
image:
  repository: your-registry/gnosari-docs
  tag: "v1.0.0"
  pullPolicy: Always

replicaCount: 3

resources:
  limits:
    cpu: 200m
    memory: 256Mi
  requests:
    cpu: 100m
    memory: 128Mi

autoscaling:
  enabled: true
  minReplicas: 2
  maxReplicas: 10
  targetCPUUtilizationPercentage: 70

ingress:
  enabled: true
  className: nginx
  annotations:
    cert-manager.io/cluster-issuer: letsencrypt-prod
    nginx.ingress.kubernetes.io/ssl-redirect: "true"
  hosts:
    - host: docs.gnosari.com
      paths:
        - path: /
          pathType: Prefix
  tls:
    - secretName: gnosari-docs-tls
      hosts:
        - docs.gnosari.com

healthCheck:
  enabled: true
  initialDelaySeconds: 30
  periodSeconds: 10
  timeoutSeconds: 5
  failureThreshold: 3
EOF

# Deploy with custom values
helm install gnosari-docs ./docs/chart -f production-values.yaml
```

## Configuration Options

### Image Configuration

```yaml
image:
  repository: your-registry/gnosari-docs  # Docker image repository
  tag: "latest"                          # Image tag
  pullPolicy: IfNotPresent               # Pull policy
```

### Service Configuration

```yaml
service:
  type: ClusterIP    # Service type (ClusterIP, NodePort, LoadBalancer)
  port: 80          # Service port
  targetPort: 3000  # Container port (matches Dockerfile EXPOSE)
```

### Ingress Configuration

```yaml
ingress:
  enabled: true
  className: nginx
  annotations:
    kubernetes.io/ingress.class: nginx
    cert-manager.io/cluster-issuer: letsencrypt-prod
  hosts:
    - host: docs.gnosari.com
      paths:
        - path: /
          pathType: Prefix
  tls:
    - secretName: gnosari-docs-tls
      hosts:
        - docs.gnosari.com
```

### Autoscaling Configuration

```yaml
autoscaling:
  enabled: true
  minReplicas: 2
  maxReplicas: 10
  targetCPUUtilizationPercentage: 70
  targetMemoryUtilizationPercentage: 80
```

### Resource Configuration

```yaml
resources:
  limits:
    cpu: 200m
    memory: 256Mi
  requests:
    cpu: 100m
    memory: 128Mi
```

## Common Operations

### Upgrade Deployment

```bash
# Upgrade with new image version
helm upgrade gnosari-docs ./docs/chart \
  --set image.tag=v1.1.0

# Upgrade with new values file
helm upgrade gnosari-docs ./docs/chart -f production-values.yaml
```

### Check Deployment Status

```bash
# Check Helm release
helm status gnosari-docs

# Check pods
kubectl get pods -l app.kubernetes.io/name=gnosari-docs

# Check service
kubectl get svc -l app.kubernetes.io/name=gnosari-docs

# Check ingress (if enabled)
kubectl get ingress -l app.kubernetes.io/name=gnosari-docs
```

### View Logs

```bash
# View logs from all pods
kubectl logs -l app.kubernetes.io/name=gnosari-docs

# Follow logs
kubectl logs -f deployment/gnosari-docs-gnosari-docs
```

### Scaling

```bash
# Manual scaling
kubectl scale deployment gnosari-docs-gnosari-docs --replicas=5

# Or update via Helm
helm upgrade gnosari-docs ./docs/chart --set replicaCount=5
```

## Troubleshooting

### Pod Not Starting

1. Check pod status:
   ```bash
   kubectl describe pod <pod-name>
   ```

2. Check image pull issues:
   ```bash
   kubectl get events --sort-by=.metadata.creationTimestamp
   ```

3. Verify image exists in registry and credentials are correct

### Service Not Accessible

1. Check service endpoints:
   ```bash
   kubectl get endpoints gnosari-docs-gnosari-docs
   ```

2. Test service connectivity:
   ```bash
   kubectl port-forward svc/gnosari-docs-gnosari-docs 8080:80
   # Access http://localhost:8080
   ```

### Ingress Issues

1. Check ingress controller logs
2. Verify DNS resolution
3. Check TLS certificate status (if using HTTPS)

## Cleanup

To remove the deployment:

```bash
# Uninstall Helm release
helm uninstall gnosari-docs

# Verify cleanup
kubectl get all -l app.kubernetes.io/name=gnosari-docs
```

## Environment Variables

If you need to pass environment variables to the container, use the `env` section in values.yaml:

```yaml
env:
  - name: NODE_ENV
    value: "production"
  - name: BASE_URL
    value: "https://docs.gnosari.com"
```

## Security Considerations

- Use specific image tags instead of `latest` in production
- Configure resource limits to prevent resource exhaustion
- Use TLS/SSL for external access
- Consider using Pod Security Standards
- Regularly update base images for security patches

## Monitoring

Consider adding monitoring annotations:

```yaml
podAnnotations:
  prometheus.io/scrape: "true"
  prometheus.io/port: "3000"
  prometheus.io/path: "/metrics"
```

This deployment configuration provides a robust, scalable setup for hosting the Gnosari documentation in Kubernetes.