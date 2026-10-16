# StudyTrack — DevOps Final Capstone

> 🌐 **Live Public AWS Deployment**: [http://a554166002e3d4c6bbb0bde1c641c9c1-147430934.ap-south-1.elb.amazonaws.com/](http://a554166002e3d4c6bbb0bde1c641c9c1-147430934.ap-south-1.elb.amazonaws.com/)  
> ⚡ **Interactive Swagger REST API Docs**: [http://a554166002e3d4c6bbb0bde1c641c9c1-147430934.ap-south-1.elb.amazonaws.com/docs](http://a554166002e3d4c6bbb0bde1c641c9c1-147430934.ap-south-1.elb.amazonaws.com/docs)  
> 📄 **Presentation Deck (Browser Viewable)**: [`demo/StudyTrack_DevOps_Capstone_Presentation.pdf`](demo/StudyTrack_DevOps_Capstone_Presentation.pdf)  
> 📂 **GitHub Repository**: [https://github.com/shubh-aarambh/Study-Track](https://github.com/shubh-aarambh/Study-Track)

StudyTrack is a cloud-native SaaS **academic coursework and deadline management system** built for the **Session 21 DevOps Final Capstone Project**. 

Students can track assignments and coursework per academic subject, set deadlines and priorities, monitor real-time completion progress (0–100%), and view operational KPIs for total, in-progress, submitted, and overdue coursework.

The core focus of this project is the comprehensive end-to-end DevOps automation pipeline:
```text
Application → Git Commit → CI Pipeline → Docker Build → Trivy Security Scan → GHCR Registry
            → Terraform AWS Infrastructure → Amazon EKS Kubernetes → Helm Deployment
            → NGINX Ingress Routing → Horizontal Pod Autoscaling (HPA)
            → Prometheus & Grafana Monitoring → Live Failure Troubleshooting
```

---

## 🎯 Capstone Deliverables & Demo Assets

- 📄 **Presentation Deck (PDF - View Directly in Browser)**: [`demo/StudyTrack_DevOps_Capstone_Presentation.pdf`](demo/StudyTrack_DevOps_Capstone_Presentation.pdf)  
  *Executive and technical slide deck with architecture diagrams and screenshot evidence (opens directly in browser/GitHub without downloading).*
- 📊 **PowerPoint Presentation Deck (PPTX)**: [`demo/StudyTrack_DevOps_Capstone_Presentation.pptx`](demo/StudyTrack_DevOps_Capstone_Presentation.pptx)  
  *Editable presentation source deck.*
- 🎥 **Live Project Tour Demonstration (In-Browser)**: [`demo/studytrack_tour.gif`](demo/studytrack_tour.gif)  
  *Plays directly inside GitHub without downloading (covers AWS Ingress ELB, StudyTrack UI, Swagger API, PostgreSQL, Prometheus, and Grafana).*
- 📹 **Full HD Video Recording (MP4)**: [`demo/studytrack_full_tour.mp4`](demo/studytrack_full_tour.mp4)  
  *Broadcast-grade 720p HD MP4 video recording (18.5 MB, 1,884 frames).*
- 📸 **Demo Screenshots Suite**: [`demo/screenshots/`](demo/screenshots/)  
  *21 screenshots covering all 15 required demo criteria.*
- 📘 **Dedicated Demo Walkthrough**: [`demo/README.md`](demo/README.md)

### 🎬 Live Project Tour (Plays Directly on GitHub Without Downloading)
![StudyTrack Full Project Tour](demo/studytrack_tour.gif)

---

## 🚀 PART O — FINAL DEMO (15 Rubric Criteria)

### 1. Application: Open StudyTrack and create an assignment
- **Action**: Accessed the interactive StudyTrack dashboard, opened the task creation modal, submitted an assignment with title, subject, priority, and deadline.
- **Verification**: Dashboard renders the new assignment card with live progress bar and recalculates KPI counters immediately.
- **Evidence**:
  - UI Overview: [`demo/screenshots/01-application-taskboard.png`](demo/screenshots/01-application-taskboard.png)
  - Create Modal: [`demo/screenshots/01-create-task-modal.png`](demo/screenshots/01-create-task-modal.png)
  - Active Task on Board: [`demo/screenshots/01-task-created-board.png`](demo/screenshots/01-task-created-board.png)
  - Video Demonstration: [`demo/studytrack_tour.gif`](demo/studytrack_tour.gif) (Full HD MP4: [`demo/studytrack_full_tour.mp4`](demo/studytrack_full_tour.mp4))

![StudyTrack Dashboard](demo/screenshots/01-task-created-board.png)

---

### 2. API: FastAPI Swagger (`/docs`) — Full CRUD
- **Action**: Opened FastAPI interactive Swagger UI at `/docs`.
- **Endpoints Demonstrated**:
  - `GET /api/assignments`: Read all assignments (with optional `?subject=` filter)
  - `POST /api/assignments`: Create a new assignment (`201 Created`)
  - `GET /api/assignments/{id}`: Read single assignment details
  - `PUT /api/assignments/{id}`: Update progress / status
  - `DELETE /api/assignments/{id}`: Delete an assignment
  - `GET /health` & `GET /ready`: Health check & database connection probe
  - `GET /metrics`: Prometheus metrics scrape target
- **Evidence**:
  - Swagger Documentation: [`demo/screenshots/02-fastapi-swagger-docs.png`](demo/screenshots/02-fastapi-swagger-docs.png)
  - API Execution Response: [`demo/screenshots/02-swagger-api-execute.png`](demo/screenshots/02-swagger-api-execute.png)

![Swagger UI](demo/screenshots/02-fastapi-swagger-docs.png)

---

### 3. Database: PostgreSQL Tasks Table
- **Action**: Queried the PostgreSQL container directly in the Kubernetes cluster using `kubectl exec`.
- **Command**:
  ```bash
  kubectl exec deployment/studytrack-postgres -n taskboard -- psql -U studytrack -d studytrack -c "SELECT id, title, subject, priority, status, progress, created_at FROM assignments;"
  ```
- **Output**:
  ```text
   id |                  title                   |   subject    | priority | status  | progress |          created_at           
  ----+------------------------------------------+--------------+----------+---------+----------+-------------------------------
    1 | EKS Ingress Live Deployment Verification | Cloud DevOps | HIGH     | PENDING |        0 | 2026-10-16 15:56:57.725742+00
    2 | Production Ingress & Autoscaling Valid.. | DevOps       | HIGH     | PENDING |        0 | 2026-10-16 16:03:12.418291+00
  (2 rows)
  ```
- **Evidence**: [`demo/screenshots/03-postgresql-database-table.png`](demo/screenshots/03-postgresql-database-table.png)

![PostgreSQL Tasks](demo/screenshots/03-postgresql-database-table.png)

---

### 4. Git: Application Code Change & Commit
- **Action**: Modified `backend/app/main.py` root endpoint with version `1.1.0` and operational health status, committed changes on branch `main`.
- **Command**:
  ```bash
  git log -n 4 --oneline --decorate
  ```
- **Output**:
  ```text
  20390cc (HEAD -> main, origin/main) feat(capstone): deploy to AWS EKS with Ingress, HPA, Prometheus, add demo suite and presentation
  505657e fix(helm): update default image repository to shubh-aarambh on GHCR
  62bcf0d docs: add troubleshooting runbook and embed evidence screenshots in README
  372bcf8 fix(scripts): ensure System.Net.Http assembly load in PowerShell load-test script
  ```
- **Evidence**: [`demo/screenshots/04-git-commit-history.png`](demo/screenshots/04-git-commit-history.png)

![Git History](demo/screenshots/04-git-commit-history.png)

---

### 5. CI: Push to GitHub & Automated Tests Running
- **Action**: Pushed commit to remote repository `shubh-aarambh/Study-Track`. GitHub Actions pipeline triggered automatically.
- **Workflow Verification**:
  - `test` job: 12 unit & integration tests executed via `pytest` (**All 12 passed in 0.50s**), followed by Vite production bundling.
  - `build-scan-push` job: Multi-stage Docker builds and Trivy scanning.
  - `deploy` job: Helm deployment validation.
- **Evidence**: [`demo/screenshots/05-ci-pipeline-tests.png`](demo/screenshots/05-ci-pipeline-tests.png)

![GitHub Actions CI](demo/screenshots/05-ci-pipeline-tests.png)

---

### 6. Docker: Two Multi-Stage Container Images
- **Action**: Containerized backend and frontend using multi-stage Docker builds.
  - Backend: `python:3.12-slim` base, non-root user execution (~142 MB).
  - Frontend: `node:22-alpine` builder + `nginx:alpine` unprivileged server (~28 MB).
- **Evidence**: [`demo/screenshots/06-docker-images-build.png`](demo/screenshots/06-docker-images-build.png)

![Docker Build](demo/screenshots/06-docker-images-build.png)

---

### 7. Security: Trivy Container Vulnerability Scan
- **Action**: Scanned both container images during CI using `aquasecurity/trivy-action@v0.36.0` with `--severity HIGH,CRITICAL --ignore-unfixed`.
- **Results**:
  - `ghcr.io/shubh-aarambh/studytrack-backend`: **0 Vulnerabilities** (HIGH: 0, CRITICAL: 0)
  - `ghcr.io/shubh-aarambh/studytrack-frontend`: **0 Vulnerabilities** (HIGH: 0, CRITICAL: 0)
- **Evidence**: [`demo/screenshots/07-trivy-security-scan.png`](demo/screenshots/07-trivy-security-scan.png)

![Trivy Scan](demo/screenshots/07-trivy-security-scan.png)

---

### 8. Registry: Images Published in GHCR
- **Action**: Published immutable container artifacts to GitHub Container Registry (`ghcr.io`).
  - `ghcr.io/shubh-aarambh/studytrack-backend:20390cc701f66785c8196c9b80587c061ea64d88`
  - `ghcr.io/shubh-aarambh/studytrack-frontend:20390cc701f66785c8196c9b80587c061ea64d88`
- **Evidence**: [`demo/screenshots/08-ghcr-container-registry.png`](demo/screenshots/08-ghcr-container-registry.png)

![GHCR Registry](demo/screenshots/08-ghcr-container-registry.png)

---

### 9. Terraform: AWS Infrastructure as Code
- **Action**: Provisioned AWS infrastructure using Terraform in `ap-south-1`:
  - AWS VPC: 2 Public subnets, 2 Private subnets, NAT Gateway, Internet Gateway (`10.20.0.0/16`)
  - Amazon EKS 1.31: Control plane with OIDC provider
  - EKS Managed Node Group: Free Tier compatible `t3.small` worker nodes
  - KMS Encryption: Envelope encryption enabled for Kubernetes Secrets
  - IAM: Granular RBAC ClusterAdminPolicy access entries
- **Evidence**: [`demo/screenshots/09-terraform-infrastructure.png`](demo/screenshots/09-terraform-infrastructure.png)

![Terraform IaC](demo/screenshots/09-terraform-infrastructure.png)

---

### 10. Kubernetes: Pods and Services in Cluster Production Namespace (`taskboard`)
- **Action**: Inspected deployed pods and services across worker nodes. Target namespace `taskboard` aligns with rubric automated evaluation commands.
- **Command**:
  ```bash
  kubectl get pods -n taskboard
  kubectl get svc -n taskboard
  ```
- **Output**:
  ```text
  NAME                                   READY   STATUS    RESTARTS   AGE
  studytrack-backend-5f69d56d8b-l5ctr    1/1     Running   0          3m
  studytrack-backend-5f69d56d8b-xwsfj    1/1     Running   0          3m
  studytrack-frontend-6c6595ffd-9s7qj    1/1     Running   0          3m
  studytrack-frontend-6c6595ffd-pz7ct    1/1     Running   0          3m
  studytrack-postgres-54bdc96cc9-tg8zf   1/1     Running   0          36m

  NAME                  TYPE        CLUSTER-IP     EXTERNAL-IP   PORT(S)    AGE
  studytrack-backend    ClusterIP   172.20.81.55   <none>        8000/TCP   36m
  studytrack-frontend   ClusterIP   172.20.85.37   <none>        80/TCP     36m
  studytrack-postgres   ClusterIP   172.20.55.50   <none>        5432/TCP   36m
  ```
- **Evidence**: [`demo/screenshots/10-kubernetes-pods-services.png`](demo/screenshots/10-kubernetes-pods-services.png)

![Kubernetes Pods & Services](demo/screenshots/10-kubernetes-pods-services.png)

---

### 11. Helm: Releases in Cluster Production Namespace (`taskboard`)
- **Action**: Inspected deployed Helm release for the multi-tier application stack.
- **Command**:
  ```bash
  helm list -n taskboard
  ```
- **Output**:
  ```text
  NAME     	NAMESPACE	REVISION	UPDATED                              	STATUS  	CHART           	APP VERSION
  taskboard	taskboard	4       	2026-10-16 21:50:45.3910242 +0530 IST	deployed	studytrack-1.0.0	1.0.0      
  ```
- **Evidence**: [`demo/screenshots/11-helm-release-taskboard.png`](demo/screenshots/11-helm-release-taskboard.png)

![Helm Release](demo/screenshots/11-helm-release-taskboard.png)

---

### 12. Ingress: Live Access via Ingress Hostname & AWS ELB
- **Action**: NGINX Ingress Controller exposed through AWS Elastic Load Balancer (ELB).
- **Public Ingress Hostname**:
  `http://a554166002e3d4c6bbb0bde1c641c9c1-147430934.ap-south-1.elb.amazonaws.com/`
- **Routing Rules**:
  - `/api` → `studytrack-backend:8000`
  - `/` → `studytrack-frontend:80`
- **Live HTTP Check**:
  ```bash
  curl http://a554166002e3d4c6bbb0bde1c641c9c1-147430934.ap-south-1.elb.amazonaws.com/api/health
  # {"status": "UP"}
  ```
- **Evidence**:
  - Live Ingress App: [`demo/screenshots/12-ingress-live-app.png`](demo/screenshots/12-ingress-live-app.png)
  - Live Ingress Dashboard: [`demo/screenshots/12-ingress-live-dashboard.png`](demo/screenshots/12-ingress-live-dashboard.png)
  - Video Demonstration: [`demo/studytrack_tour.gif`](demo/studytrack_tour.gif) (Scene 1: Live Ingress ELB)

![Live Ingress](demo/screenshots/12-ingress-live-app.png)

---

### 13. HPA: Horizontal Pod Autoscaler
- **Command**:
  ```bash
  kubectl get hpa -n taskboard
  ```
- **Output**:
  ```text
  NAME                 REFERENCE                       TARGETS       MINPODS   MAXPODS   REPLICAS   AGE
  studytrack-backend   Deployment/studytrack-backend   cpu: 3%/60%   2         6         2          38m
  ```
- **Load Generation**: Executed concurrent load test script:
  ```powershell
  .\scripts\load-test.ps1 -Url http://a554166002e3d4c6bbb0bde1c641c9c1-147430934.ap-south-1.elb.amazonaws.com/api/health -Requests 200 -Concurrency 10
  # Load test completed in 1.85s (~108.2 req/sec)
  ```
- **Evidence**: [`demo/screenshots/13-hpa-horizontal-pod-autoscaler.png`](demo/screenshots/13-hpa-horizontal-pod-autoscaler.png)

![HPA Autoscaler](demo/screenshots/13-hpa-horizontal-pod-autoscaler.png)

---

### 14. Monitoring: Prometheus & Grafana
- **Action**: Deployed `kube-prometheus-stack` into namespace `monitoring`.
- **Prometheus UI**: Verified scrape targets and executed PromQL expressions (`up`).
- **Grafana Dashboards**: Monitored cluster compute resources, pod CPU/memory utilization, and request rates.
- **Evidence**:
  - Prometheus Query: [`demo/screenshots/14-prometheus-query.png`](demo/screenshots/14-prometheus-query.png)
  - Prometheus Targets: [`demo/screenshots/14-prometheus-targets.png`](demo/screenshots/14-prometheus-targets.png)
  - Grafana Dashboard: [`demo/screenshots/14-grafana-cluster-dashboard.png`](demo/screenshots/14-grafana-cluster-dashboard.png)
  - Video Demonstration: [`demo/studytrack_tour.gif`](demo/studytrack_tour.gif) (Scenes 3 & 4: Prometheus & Grafana)

![Grafana Monitoring](demo/screenshots/14-grafana-cluster-dashboard.png)

---

### 15. Failure Simulation & Live Troubleshooting
- **Scenario**: Injected a service disruption by applying a Service with an unmatched selector `app: label-that-does-not-exist`.
- **Diagnosis**: Observed `ENDPOINTS <none>` on `broken-service`.
- **Remediation**: Patched selector to match running pods (`app: studytrack-backend`).
- **Resolution**: Endpoints immediately recovered with active pod IPs (`10.20.1.164:8000, 10.20.2.151:8000`).
- **Evidence**: [`demo/screenshots/15-live-troubleshooting-remediation.png`](demo/screenshots/15-live-troubleshooting-remediation.png)

![Live Troubleshooting](demo/screenshots/15-live-troubleshooting-remediation.png)

---

## Tech Stack Overview

| Layer | Technology | Purpose |
|:---|:---|:---|
| **Frontend** | React, Vite, Vanilla CSS | Responsive Glassmorphism UI, client routing |
| **Backend** | FastAPI, SQLAlchemy 2, Alembic, Pydantic v2 | High-performance RESTful APIs, OpenAPI docs |
| **Database** | PostgreSQL 16 | Relational data persistence |
| **Testing** | Pytest, StaticPool SQLite | Isolated unit and integration testing |
| **Containerization** | Docker, NGINX Alpine | Multi-stage unprivileged containers (<150 MB) |
| **CI/CD** | GitHub Actions | Automated build, test, scan, and deploy pipeline |
| **Security** | Aqua Security Trivy | Static container vulnerability scanning (0 CVEs) |
| **Registry** | GitHub Container Registry (GHCR) | Secure OCI container image repository |
| **IaC** | Terraform, AWS VPC & EKS Modules | Declarative cloud infrastructure provisioning |
| **Cloud Provider** | AWS (ap-south-1) | VPC, NAT Gateway, EKS Cluster, ELB, KMS |
| **Orchestration** | Kubernetes 1.31, Helm 3 | Declarative workload management and deployments |
| **Ingress** | NGINX Ingress Controller, AWS ELB | Single entrypoint and path-based routing |
| **Autoscaling** | Kubernetes HPA, Metrics Server | Dynamic CPU-based pod autoscaling (2–6 replicas) |
| **Monitoring** | Prometheus, Grafana | Cluster and application telemetry, PromQL, dashboards |

---

## Repository Structure

```text
├── .github/workflows/ci-cd.yml      # Automated GitHub Actions pipeline
├── backend/                         # FastAPI application, models, schemas, and tests
├── frontend/                        # React + Vite frontend and NGINX configuration
├── helm/studytrack/                 # Helm chart manifests (deployments, svc, ingress, HPA)
├── terraform/                       # Terraform AWS VPC and EKS infrastructure code
├── monitoring/                      # Prometheus and Grafana Helm values
├── troubleshooting/                 # Chaos engineering manifests and runbooks
├── scripts/                         # Load testing scripts and automation tools
├── demo/                            # Final presentation, demo video, and screenshots
│   ├── StudyTrack_DevOps_Capstone_Presentation.pdf
│   ├── StudyTrack_DevOps_Capstone_Presentation.pptx
│   ├── studytrack_tour.gif
│   ├── studytrack_full_tour.mp4
│   └── screenshots/
└── README.md
```
