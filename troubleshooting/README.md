# Kubernetes Troubleshooting Exercises

This directory contains intentionally broken Kubernetes manifests to demonstrate cluster debugging, diagnosis workflows, and resolution techniques as required for the DevOps Capstone.

---

## Exercise 1: ImagePullBackOff / ErrImagePull (`broken-image.yaml`)

### Manifest Problem
The deployment references a non-existent container image tag:
```yaml
containers:
  - name: backend
    image: ghcr.io/example/studytrack-backend:does-not-exist
```

### Apply Scenario
```bash
kubectl apply -f troubleshooting/broken-image.yaml
```

### Diagnostic Steps
1. **Check Pod status**:
   ```bash
   kubectl get pods -n studytrack -l app=broken-image
   # Output: studytrack-broken-image-xxx  0/1  ImagePullBackOff (or ErrImagePull)
   ```
2. **Inspect events**:
   ```bash
   kubectl describe pod -n studytrack -l app=broken-image
   ```
   Look at the **Events** section at the bottom:
   ```text
   Failed to pull image "ghcr.io/example/studytrack-backend:does-not-exist": rpc error: code = NotFound
   Error: ImagePullBackOff
   ```

### Resolution
1. Correct the image repository and tag to an existing image (e.g. `ghcr.io/<owner>/studytrack-backend:<valid-tag>`).
2. If using a private repository, ensure an `imagePullSecret` is created and attached to the Pod spec:
   ```yaml
   imagePullSecrets:
     - name: ghcr-secret
   ```
3. Cleanup:
   ```bash
   kubectl delete -f troubleshooting/broken-image.yaml
   ```

---

## Exercise 2: Service with No Endpoints (`broken-service.yaml`)

### Manifest Problem
The service specifies a label selector that does not match any running pods:
```yaml
spec:
  selector:
    app: label-that-does-not-exist
  ports:
    - port: 8080
      targetPort: 8080
```

### Apply Scenario
```bash
kubectl apply -f troubleshooting/broken-service.yaml
```

### Diagnostic Steps
1. **Check Service status**:
   ```bash
   kubectl get svc broken-service -n studytrack
   # Service exists with ClusterIP assigned
   ```
2. **Inspect Service Endpoints**:
   ```bash
   kubectl get endpoints broken-service -n studytrack
   # Output:
   # NAME             ENDPOINTS   AGE
   # broken-service   <none>      30s
   ```
   Notice that `ENDPOINTS` is `<none>`! Traffic directed to this service will result in `Connection Refused` or HTTP `503 Service Unavailable`.
3. **Compare selector labels with running pods**:
   ```bash
   kubectl get svc broken-service -n studytrack -o jsonpath='{.spec.selector}'
   # Output: {"app":"label-that-does-not-exist"}

   kubectl get pods -n studytrack --show-labels
   # Output shows pods have "app=studytrack-backend" or "app=studytrack-frontend"
   ```

### Resolution
Update the service selector in `broken-service.yaml` to match the target workload pods:
```yaml
spec:
  selector:
    app: studytrack-backend
  ports:
    - port: 8000
      targetPort: 8000
```
Verify endpoints are now populated:
```bash
kubectl get endpoints broken-service -n studytrack
# Output: broken-service   10.244.0.12:8000,10.244.0.13:8000
```
Cleanup:
```bash
kubectl delete -f troubleshooting/broken-service.yaml
```
