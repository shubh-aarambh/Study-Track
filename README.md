# StudyTrack — DevOps Final Capstone

StudyTrack is a SaaS-style **assignment and deadline tracker for students**. Students add assignments per subject, set a due date and priority, track progress (0–100 %), and see KPIs for total / in-progress / submitted / **overdue** work.

The point of the project is the DevOps pipeline around the app: it travels from a laptop to a monitored Kubernetes cluster.

```text
Developer -> GitHub -> GitHub Actions (pytest, frontend build, docker build, Trivy, push to GHCR)
          -> Terraform (AWS VPC + EKS) -> Helm (frontend, backend, postgres, ingress, HPA)
          -> Prometheus -> Grafana
```

## Tech stack

| Layer | Tech |
|-------|------|
| Frontend | React + Vite, responsive CSS, served by unprivileged Nginx |
| Backend | FastAPI, SQLAlchemy 2, Alembic, Pydantic v2 |
| Database | PostgreSQL 16 |
| Tests | pytest (in-memory SQLite, never the real DB) |
| Containers | Docker multi-stage builds, non-root users, Docker Compose |
| CI/CD | GitHub Actions, GHCR, image tag = Git commit SHA |
| Security | Trivy (HIGH/CRITICAL fail the build) |
| IaC | Terraform: AWS VPC + EKS |
| Orchestration | Kubernetes, Helm, Ingress, HPA |
| Observability | `/metrics`, Prometheus (ServiceMonitor), Grafana |

## API

```text
GET    /                       service info
GET    /health                 liveness
GET    /ready                  readiness (checks DB)
GET    /metrics                Prometheus metrics
GET    /api/assignments        list (optional ?subject=)
GET    /api/assignments/stats  KPI counters
GET    /api/assignments/{id}
POST   /api/assignments
PUT    /api/assignments/{id}
DELETE /api/assignments/{id}
```

Swagger UI: `http://localhost:8000/docs`.

## Run locally

### Docker Compose (recommended)
```bash
docker compose up --build
# UI:      http://localhost:3000
# API:     http://localhost:8000/docs
# Metrics: http://localhost:8000/metrics
docker compose down -v
```

### Without Docker (SQLite, for quick dev)
```bash
cd backend
python -m venv .venv && source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
export DATABASE_URL=sqlite:///./dev.db               # or a PostgreSQL URL
alembic upgrade head
uvicorn app.main:app --reload --port 8000

cd ../frontend && npm install && npm run dev        # http://localhost:5173
```

## Tests
```bash
cd backend && pytest -v
```
12 tests cover health/ready/root, full CRUD, validation, filtering, stats (overdue logic) and `/metrics`. `tests/conftest.py` overrides the DB dependency with an in-memory SQLite database.

## CI/CD (`.github/workflows/ci-cd.yml`)
1. **test** — pytest (fails the pipeline) + frontend build
2. **build-scan-push** — build both images, **Trivy** scan (HIGH/CRITICAL → fail), push to GHCR tagged with `${{ github.sha }}`
3. **deploy** — `helm upgrade --install` with the SHA tag (needs the `KUBE_CONFIG_DATA` secret)

## Infrastructure (Terraform)
```bash
cd terraform
cp terraform.tfvars.example terraform.tfvars
terraform init && terraform plan
terraform apply
aws eks update-kubeconfig --region ap-south-1 --name studytrack-eks
# ... when finished, to avoid AWS cost:
terraform destroy
```
Creates a VPC with two public and two private subnets, one NAT gateway, and an EKS cluster with a managed node group (2× t3.medium). **No credentials are committed.**

## Kubernetes + Helm
```bash
kubectl apply -f k8s/namespace.yaml
helm upgrade --install studytrack ./helm/studytrack -n studytrack \
  --set frontend.image=ghcr.io/<owner>/studytrack-frontend --set frontend.tag=<sha> \
  --set backend.image=ghcr.io/<owner>/studytrack-backend   --set backend.tag=<sha> \
  --set ingress.enabled=true
kubectl get pods,svc -n studytrack
helm list -n studytrack
```
Backend and frontend run with 2 replicas behind ClusterIP services; Ingress routes `/` to the frontend and `/api` to the backend; an HPA scales the backend on CPU.

## Monitoring
```bash
helm repo add prometheus-community https://prometheus-community.github.io/helm-charts
helm upgrade --install kube-prometheus-stack prometheus-community/kube-prometheus-stack \
  -n monitoring --create-namespace -f monitoring/prometheus-values.yaml
kubectl port-forward -n monitoring svc/kube-prometheus-stack-grafana 3001:80
```
Useful Grafana/PromQL queries:
- `sum(rate(http_requests_total[1m])) by (handler)` — request rate
- `histogram_quantile(0.95, sum(rate(http_request_duration_seconds_bucket[5m])) by (le))` — p95 latency
- `sum(rate(http_requests_total{status="5xx"}[1m]))` — error rate

## Troubleshooting exercises
`troubleshooting/` has deliberately broken manifests (bad image tag → `ImagePullBackOff`, wrong service selector → no endpoints).

## Repository layout
```text
backend/   FastAPI app, Alembic migrations, tests, Dockerfile
frontend/  React + Vite UI, Nginx template, Dockerfile
helm/      studytrack Helm chart      k8s/  namespace manifest
terraform/ AWS VPC + EKS              monitoring/  Prometheus/Grafana values
docs/      screenshots and evidence   .github/workflows/  CI/CD
```
