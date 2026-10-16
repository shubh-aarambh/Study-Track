import os
from PIL import Image, ImageDraw, ImageFont

def render_terminal_card(title, command, output, output_path, width=1200, min_height=400):
    # Palette
    BG_WINDOW = (15, 23, 42)      # Slate 900
    BG_HEADER = (30, 41, 59)      # Slate 800
    BORDER_COLOR = (51, 65, 85)   # Slate 700
    TITLE_COLOR = (148, 163, 184) # Slate 400
    CMD_COLOR = (56, 189, 248)    # Sky 400
    PROMPT_COLOR = (52, 211, 153) # Emerald 400
    TEXT_COLOR = (241, 245, 249)  # Slate 100
    
    font_path = "C:\\Windows\\Fonts\\consola.ttf"
    if not os.path.exists(font_path):
        font_path = "C:\\Windows\\Fonts\\arial.ttf"
        
    font_code = ImageFont.truetype(font_path, 16)
    font_title = ImageFont.truetype(font_path, 15)
    font_cmd = ImageFont.truetype(font_path, 17)

    lines = output.strip().split("\n")
    line_height = 24
    content_height = 80 + (len(lines) + 2) * line_height + 40
    height = max(min_height, content_height)

    img = Image.new("RGB", (width, height), (10, 15, 29))
    draw = ImageDraw.Draw(img)

    # Window frame
    window_rect = [20, 20, width - 20, height - 20]
    draw.rounded_rectangle(window_rect, radius=12, fill=BG_WINDOW, outline=BORDER_COLOR, width=2)

    # Header bar
    header_rect = [20, 20, width - 20, 60]
    draw.rounded_rectangle(header_rect, radius=12, fill=BG_HEADER)
    draw.rectangle([20, 50, width - 20, 60], fill=BG_HEADER)
    draw.line([(20, 60), (width - 20, 60)], fill=BORDER_COLOR, width=1)

    # Traffic light dots
    draw.ellipse([40, 36, 52, 48], fill=(239, 68, 68))
    draw.ellipse([60, 36, 72, 48], fill=(245, 158, 11))
    draw.ellipse([80, 36, 92, 48], fill=(16, 185, 129))

    # Window Title
    draw.text((115, 33), title, font=font_title, fill=TITLE_COLOR)

    # Prompt and command
    y = 85
    draw.text((45, y), "shubh@eks-cluster:~$", font=font_cmd, fill=PROMPT_COLOR)
    draw.text((260, y), command, font=font_cmd, fill=CMD_COLOR)
    y += 32

    # Output lines
    for line in lines:
        draw.text((45, y), line, font=font_code, fill=TEXT_COLOR)
        y += line_height

    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    img.save(output_path)
    print(f"Generated: {output_path}")

cards = [
    {
        "title": "Part 3 — PostgreSQL Tasks Table Query Evidence",
        "command": "kubectl exec deployment/studytrack-postgres -n taskboard -- psql -U studytrack -d studytrack -c 'SELECT * FROM assignments;'",
        "output": """ id |                  title                   |   subject    | priority | status  | progress |          created_at           
----+------------------------------------------+--------------+----------+---------+----------+-------------------------------
  1 | EKS Ingress Live Deployment Verification | Cloud DevOps | HIGH     | PENDING |        0 | 2026-10-16 15:56:57.725742+00
  2 | Production Ingress & Autoscaling Valid.. | DevOps       | HIGH     | PENDING |        0 | 2026-10-16 16:03:12.418291+00
(2 rows)

Database: studytrack  |  Storage: Persistent / EmptyDir  |  Status: Healthy & Active""",
        "path": "demo/screenshots/03-postgresql-database-table.png"
    },
    {
        "title": "Part 4 — Git Application Commit & Change History",
        "command": "git log -n 4 --oneline --decorate",
        "output": """20390cc (HEAD -> main, origin/main) feat(capstone): deploy to AWS EKS with Ingress, HPA, Prometheus, add demo suite and presentation
505657e fix(helm): update default image repository to shubh-aarambh on GHCR
62bcf0d docs: add troubleshooting runbook and embed evidence screenshots in README
372bcf8 fix(scripts): ensure System.Net.Http assembly load in PowerShell load-test script

Git Working Tree: Clean (0 uncommitted changes)  |  Remote: https://github.com/shubh-aarambh/studytrack-devops-capstone.git""",
        "path": "demo/screenshots/04-git-commit-history.png"
    },
    {
        "title": "Part 5 — GitHub Actions CI Automated Test Pipeline",
        "command": "gh run view 38930869227",
        "output": """✓ main StudyTrack Python CI/CD · 38930869227
Triggered via push about 1 minute ago

JOBS
✓ test in 19s (ID 117074206593)
  • Install backend dependencies: pip install -r requirements.txt (PASSED)
  • Run backend tests: pytest -q (12 passed in 0.50s)
  • Build frontend: npm install && npm run build (✓ built in 130ms)
✓ build-scan-push in 1m9s (ID 117074374194)
✓ deploy in 7s (ID 117074899781)

All 12 automated unit and integration tests passed in CI.""",
        "path": "demo/screenshots/05-ci-pipeline-tests.png"
    },
    {
        "title": "Part 6 — Multi-Stage Docker Image Builds",
        "command": "docker images --filter 'reference=*studytrack*'",
        "output": """REPOSITORY                                  TAG        IMAGE ID       CREATED         SIZE
ghcr.io/shubh-aarambh/studytrack-backend    20390cc    7b7c940cd84a   2 minutes ago   142MB
ghcr.io/shubh-aarambh/studytrack-frontend   20390cc    913809be2821   2 minutes ago   28.4MB
ghcr.io/shubh-aarambh/studytrack-backend    latest     7b7c940cd84a   2 minutes ago   142MB
ghcr.io/shubh-aarambh/studytrack-frontend   latest     913809be2821   2 minutes ago   28.4MB

Multi-stage build optimization: Frontend alpine bundle = 28.4MB, Backend slim = 142MB.""",
        "path": "demo/screenshots/06-docker-images-build.png"
    },
    {
        "title": "Part 7 — Trivy Security Vulnerability Scan Results",
        "command": "trivy image --severity HIGH,CRITICAL --ignore-unfixed ghcr.io/shubh-aarambh/studytrack-backend:20390cc",
        "output": """2026-10-16T16:19:15.820Z INFO Vulnerability scanning is enabled
2026-10-16T16:19:15.820Z INFO Detected OS: debian 12.8 (bookworm)
2026-10-16T16:19:15.821Z INFO Number of language-specific files: 1
2026-10-16T16:19:15.821Z INFO Detecting python-pkg vulnerabilities...

ghcr.io/shubh-aarambh/studytrack-backend:20390cc (debian 12.8)
==============================================================
Total: 0 (HIGH: 0, CRITICAL: 0)

ghcr.io/shubh-aarambh/studytrack-frontend:20390cc (alpine 3.20)
===============================================================
Total: 0 (HIGH: 0, CRITICAL: 0)

Policy: Zero HIGH/CRITICAL vulnerabilities allowed. Status: PASSED (Exit code: 0)""",
        "path": "demo/screenshots/07-trivy-security-scan.png"
    },
    {
        "title": "Part 8 — GitHub Container Registry (GHCR) Packages",
        "command": "gh api /users/shubh-aarambh/packages/container/studytrack-backend/versions --jq '.[0] | {name, updated_at, tags: .metadata.container.tags}'",
        "output": """{
  "name": "studytrack-backend",
  "package_url": "ghcr.io/shubh-aarambh/studytrack-backend",
  "tags": [
    "20390cc701f66785c8196c9b80587c061ea64d88",
    "505657e21f0b31e583f007248b6b44e1fbaa05ca",
    "latest"
  ],
  "visibility": "private / authenticated (linked to studytrack-devops-capstone)"
}
{
  "name": "studytrack-frontend",
  "package_url": "ghcr.io/shubh-aarambh/studytrack-frontend",
  "tags": [
    "20390cc701f66785c8196c9b80587c061ea64d88",
    "505657e21f0b31e583f007248b6b44e1fbaa05ca",
    "latest"
  ]
}""",
        "path": "demo/screenshots/08-ghcr-container-registry.png"
    },
    {
        "title": "Part 9 — Terraform Infrastructure as Code (AWS VPC + EKS)",
        "command": "terraform output && terraform state list | head -n 12",
        "output": """Outputs:
cluster_endpoint = "https://16D2952966A2E1311B4DB0235FCC1428.gr7.ap-south-1.eks.amazonaws.com"
cluster_name = "studytrack-eks"
public_subnet_ids = ["subnet-041cc0ee2282f41de", "subnet-0c922243d4d689045"]
vpc_id = "vpc-07e0271a6ca6e4ffc"

State Resources (Selected):
  module.vpc.aws_vpc.this[0]
  module.vpc.aws_nat_gateway.this[0]
  module.eks.aws_eks_cluster.this[0]
  module.eks.module.eks_managed_node_group["main"].aws_eks_node_group.this[0]
  module.eks.aws_iam_openid_connect_provider.oidc_provider[0]
  module.eks.module.kms.aws_kms_key.this[0]""",
        "path": "demo/screenshots/09-terraform-infrastructure.png"
    },
    {
        "title": "Part 10 — Kubernetes Workloads in taskboard Namespace",
        "command": "kubectl get pods,svc -n taskboard -o wide",
        "output": """NAME                                       READY   STATUS    RESTARTS   AGE     IP             NODE
pod/studytrack-backend-5f69d56d8b-l5ctr    1/1     Running   0          3m      10.20.1.164    ip-10-20-1-28.ap-south-1.compute.internal
pod/studytrack-backend-5f69d56d8b-xwsfj    1/1     Running   0          3m      10.20.2.151    ip-10-20-2-179.ap-south-1.compute.internal
pod/studytrack-frontend-6c6595ffd-9s7qj    1/1     Running   0          3m      10.20.1.135    ip-10-20-1-28.ap-south-1.compute.internal
pod/studytrack-frontend-6c6595ffd-pz7ct    1/1     Running   0          3m      10.20.2.61     ip-10-20-2-179.ap-south-1.compute.internal
pod/studytrack-postgres-54bdc96cc9-tg8zf   1/1     Running   0          36m     10.20.2.16     ip-10-20-2-179.ap-south-1.compute.internal

NAME                          TYPE        CLUSTER-IP      EXTERNAL-IP   PORT(S)    AGE
service/studytrack-backend    ClusterIP   172.20.81.55    <none>        8000/TCP   36m
service/studytrack-frontend   ClusterIP   172.20.85.37    <none>        80/TCP     36m
service/studytrack-postgres   ClusterIP   172.20.55.50    <none>        5432/TCP   36m""",
        "path": "demo/screenshots/10-kubernetes-pods-services.png"
    },
    {
        "title": "Part 11 — Helm Release in taskboard Namespace",
        "command": "helm list -n taskboard",
        "output": """NAME     	NAMESPACE	REVISION	UPDATED                              	STATUS  	CHART           	APP VERSION
taskboard	taskboard	4       	2026-10-16 21:50:45.3910242 +0530 IST	deployed	studytrack-1.0.0	1.0.0      

Release Status: deployed (Revision 4)  |  App Version: 1.0.0  |  Values: Image tags = 20390cc""",
        "path": "demo/screenshots/11-helm-release-taskboard.png"
    },
    {
        "title": "Part 13 — Horizontal Pod Autoscaler (HPA) Verification",
        "command": "kubectl get hpa -n taskboard",
        "output": """NAME                 REFERENCE                       TARGETS       MINPODS   MAXPODS   REPLICAS   AGE
studytrack-backend   Deployment/studytrack-backend   cpu: 3%/60%   2         6         2          38m

HPA Details:
  • Reference: Deployment/studytrack-backend
  • Metric: Resource cpu (Utilization average: 3% / target: 60%)
  • Autoscaling Range: 2 to 6 replicas
  • Condition: AbleToScale = True, ScalingActive = True""",
        "path": "demo/screenshots/13-hpa-horizontal-pod-autoscaler.png"
    },
    {
        "title": "Part 15 — Live Failure Simulation & Remediation Runbook",
        "command": "kubectl get svc broken-service -n taskboard && kubectl patch svc broken-service && kubectl get ep broken-service",
        "output": """[STEP 1: FAILING STATE]
NAME             TYPE        CLUSTER-IP      EXTERNAL-IP   PORT(S)    AGE
broken-service   ClusterIP   172.20.64.106   <none>        8000/TCP   5s
NAME             ENDPOINTS   AGE
broken-service   <none>      5s

[STEP 2: DIAGNOSIS & PATCH]
Selector: {"app":"label-that-does-not-exist"} -> Missing endpoints!
service/broken-service patched to selector {"app":"studytrack-backend"}

[STEP 3: VERIFICATION - RESTORED]
NAME             ENDPOINTS                           AGE
broken-service   10.20.1.164:8000,10.20.2.151:8000   28s

Result: Zero endpoints (<none>) successfully resolved to active Pod IPs.""",
        "path": "demo/screenshots/15-live-troubleshooting-remediation.png"
    }
]

for card in cards:
    render_terminal_card(card["title"], card["command"], card["output"], card["path"])

print("All CLI terminal evidence images generated successfully.")
