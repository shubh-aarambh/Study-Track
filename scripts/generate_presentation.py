import sys
import os
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.enum.text import PP_ALIGN
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE

def create_deck(output_path):
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)

    # Theme Colors
    BG_DARK = RGBColor(15, 23, 42)        # Slate 900
    BG_CARD = RGBColor(30, 41, 59)        # Slate 800
    TEXT_LIGHT = RGBColor(248, 250, 252)  # Slate 50
    TEXT_MUTED = RGBColor(148, 163, 184)  # Slate 400
    ACCENT_BLUE = RGBColor(56, 189, 248)  # Sky 400
    ACCENT_INDIGO = RGBColor(99, 102, 241)# Indigo 500
    ACCENT_GREEN = RGBColor(52, 211, 153) # Emerald 400
    ACCENT_AMBER = RGBColor(251, 191, 36) # Amber 400
    ACCENT_RED = RGBColor(248, 113, 113)  # Red 400

    blank_layout = prs.slide_layouts[6]

    def add_header(slide, title, category="STUDYTRACK DEVOPS CAPSTONE"):
        # Header background bar
        hdr_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.4), Inches(11.7), Inches(1.1))
        tf = hdr_box.text_frame
        tf.word_wrap = True
        tf.margin_left = tf.margin_top = tf.margin_right = tf.margin_bottom = 0
        
        p_cat = tf.paragraphs[0]
        p_cat.text = category.upper()
        p_cat.font.size = Pt(11)
        p_cat.font.bold = True
        p_cat.font.color.rgb = ACCENT_BLUE

        p_title = tf.add_paragraph()
        p_title.text = title
        p_title.font.size = Pt(24)
        p_title.font.bold = True
        p_title.font.color.rgb = TEXT_LIGHT

    def create_card(slide, left, top, width, height, title, items, badge="", badge_color=ACCENT_BLUE):
        # Card background shape
        shape = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, top, width, height)
        shape.fill.solid()
        shape.fill.fore_color.rgb = BG_CARD
        shape.line.color.rgb = RGBColor(51, 65, 85)
        shape.line.width = Pt(1)

        # Card text content
        tb = slide.shapes.add_textbox(left + Inches(0.25), top + Inches(0.2), width - Inches(0.5), height - Inches(0.4))
        tf = tb.text_frame
        tf.word_wrap = True
        tf.margin_left = tf.margin_top = tf.margin_right = tf.margin_bottom = 0

        p_head = tf.paragraphs[0]
        p_head.text = title
        p_head.font.size = Pt(15)
        p_head.font.bold = True
        p_head.font.color.rgb = ACCENT_BLUE

        if badge:
            p_badge = tf.add_paragraph()
            p_badge.text = f"[{badge}]"
            p_badge.font.size = Pt(10)
            p_badge.font.bold = True
            p_badge.font.color.rgb = badge_color

        for item in items:
            p = tf.add_paragraph()
            p.text = f"•  {item}"
            p.font.size = Pt(11)
            p.font.color.rgb = TEXT_LIGHT
            p.space_after = Pt(4)

    # -------------------------------------------------------------
    # SLIDE 1: TITLE SLIDE
    # -------------------------------------------------------------
    s1 = prs.slides.add_slide(blank_layout)
    bg1 = s1.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, Inches(13.333), Inches(7.5))
    bg1.fill.solid()
    bg1.fill.fore_color.rgb = BG_DARK
    bg1.line.fill.background()

    tb1 = s1.shapes.add_textbox(Inches(1.2), Inches(1.6), Inches(11), Inches(4.5))
    tf1 = tb1.text_frame
    tf1.word_wrap = True

    p = tf1.paragraphs[0]
    p.text = "DEVOPS CAPSTONE PROJECT — SESSION 21"
    p.font.size = Pt(13)
    p.font.bold = True
    p.font.color.rgb = ACCENT_BLUE
    p.space_after = Pt(14)

    p = tf1.add_paragraph()
    p.text = "StudyTrack & TaskBoard"
    p.font.size = Pt(40)
    p.font.bold = True
    p.font.color.rgb = TEXT_LIGHT

    p = tf1.add_paragraph()
    p.text = "Production-Grade GitOps, Microservices, EKS, Helm, Ingress & Observability"
    p.font.size = Pt(18)
    p.font.color.rgb = TEXT_MUTED
    p.space_after = Pt(28)

    p = tf1.add_paragraph()
    p.text = "Candidate: shubh-aarambh  |  Domain: Learning Management System & TaskBoard"
    p.font.size = Pt(13)
    p.font.bold = True
    p.font.color.rgb = ACCENT_GREEN

    p = tf1.add_paragraph()
    p.text = "Stack: React Vite • FastAPI • PostgreSQL • Docker • GHCR • Trivy • Terraform • AWS EKS • Helm • NGINX Ingress • HPA • Prometheus & Grafana"
    p.font.size = Pt(11)
    p.font.color.rgb = TEXT_MUTED

    # -------------------------------------------------------------
    # SLIDE 2: END-TO-END DEVOPS LIFECYCLE
    # -------------------------------------------------------------
    s2 = prs.slides.add_slide(blank_layout)
    bg2 = s2.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, Inches(13.333), Inches(7.5))
    bg2.fill.solid()
    bg2.fill.fore_color.rgb = BG_DARK
    bg2.line.fill.background()
    add_header(s2, "End-to-End DevOps Architecture & Demonstration Pipeline")

    create_card(s2, Inches(0.8), Inches(1.8), Inches(3.6), Inches(5.1), 
                "Phase 1: Build & Verify",
                ["Full-stack React (Vite) + FastAPI + PostgreSQL",
                 "Local development verified with automated tests",
                 "Git commit triggers GitHub Actions CI pipeline",
                 "Pytest test suite & frontend production bundle check",
                 "Multi-stage Docker builds for minimal attack surface",
                 "Trivy static security vulnerability scanning (0 CVEs)"],
                "ENGINEERING & SECURITY", ACCENT_BLUE)

    create_card(s2, Inches(4.8), Inches(1.8), Inches(3.6), Inches(5.1), 
                "Phase 2: Deploy & Orchestrate",
                ["GitHub Container Registry (GHCR) image packaging",
                 "Terraform automated AWS infrastructure provisioning",
                 "AWS VPC (public & private subnets, NAT Gateway)",
                 "Amazon EKS Managed Kubernetes Cluster v1.31",
                 "Helm package management with custom values",
                 "Declarative deployments to studytrack & taskboard"],
                "INFRASTRUCTURE & K8S", ACCENT_INDIGO)

    create_card(s2, Inches(8.8), Inches(1.8), Inches(3.6), Inches(5.1), 
                "Phase 3: Route & Observe",
                ["NGINX Ingress Controller for single-entry routing",
                 "Horizontal Pod Autoscaler (HPA) CPU thresholding",
                 "Prometheus metrics scraping (/metrics endpoint)",
                 "Grafana real-time telemetry dashboards",
                 "Chaos engineering & failure simulation runbook",
                 "Live remediation of Pod and Service errors"],
                "OPERATIONS & SRE", ACCENT_GREEN)

    # -------------------------------------------------------------
    # SLIDE 3: APPLICATION & REST APIS (PARTS 1, 2, 3)
    # -------------------------------------------------------------
    s3 = prs.slides.add_slide(blank_layout)
    bg3 = s3.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, Inches(13.333), Inches(7.5))
    bg3.fill.solid()
    bg3.fill.fore_color.rgb = BG_DARK
    bg3.line.fill.background()
    add_header(s3, "Part 1, 2, 3 — Application, REST API Suite & PostgreSQL Database")

    create_card(s3, Inches(0.8), Inches(1.8), Inches(3.6), Inches(5.1), 
                "1. StudyTrack & TaskBoard UI",
                ["Responsive modern interface with Glassmorphism UI",
                 "Live assignment and task tracking dashboard",
                 "Filters by status: Pending, In Progress, Submitted",
                 "Real-time completion percentage metrics and progress bars",
                 "Quick-create modal for assignments and tasks",
                 "Instant optimistic UI updates with error boundaries"],
                "PART 1: APPLICATION", ACCENT_BLUE)

    create_card(s3, Inches(4.8), Inches(1.8), Inches(3.6), Inches(5.1), 
                "2. FastAPI OpenAPI / Swagger",
                ["Interactive documentation live at /docs",
                 "GET /api/assignments — List & filter tasks",
                 "POST /api/assignments — Create task (201 Created)",
                 "GET /api/assignments/{id} — Retrieve task detail",
                 "PUT /api/assignments/{id} — Full/partial update",
                 "DELETE /api/assignments/{id} — Delete task",
                 "GET /api/assignments/stats — Aggregated metrics",
                 "GET /health & /ready — Liveness & readiness probes"],
                "PART 2: REST API", ACCENT_INDIGO)

    create_card(s3, Inches(8.8), Inches(1.8), Inches(3.6), Inches(5.1), 
                "3. PostgreSQL Persistence",
                ["Stateful container with persistent volume storage",
                 "Relational schema mapping tasks and assignments",
                 "Columns: id, title, subject, due_date, progress, status",
                 "SQLAlchemy ORM with strict Pydantic schemas",
                 "Connection pooling and automated schema initialization",
                 "Verified persistence across pod restarts"],
                "PART 3: DATABASE", ACCENT_GREEN)

    # -------------------------------------------------------------
    # SLIDE 4: GIT, CI PIPELINE & CONTAINER REGISTRY (PARTS 4, 5, 6, 8)
    # -------------------------------------------------------------
    s4 = prs.slides.add_slide(blank_layout)
    bg4 = s4.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, Inches(13.333), Inches(7.5))
    bg4.fill.solid()
    bg4.fill.fore_color.rgb = BG_DARK
    bg4.line.fill.background()
    add_header(s4, "Part 4, 5, 6, 8 — GitOps, CI/CD Pipeline & GHCR Container Registry")

    create_card(s4, Inches(0.8), Inches(1.8), Inches(3.6), Inches(5.1), 
                "4 & 5. Git Commit & CI",
                ["Git version control workflow on branch 'main'",
                 "GitHub Actions automated pipeline (.github/workflows/ci-cd.yml)",
                 "Automated Pytest backend validation with test coverage",
                 "Node.js 22 frontend Vite production compilation check",
                 "Strict fail-fast quality gate on every commit",
                 "Commit SHA tagging ensures 100% build traceability"],
                "PARTS 4 & 5: CI/CD", ACCENT_BLUE)

    create_card(s4, Inches(4.8), Inches(1.8), Inches(3.6), Inches(5.1), 
                "6. Multi-Stage Docker Builds",
                ["Backend: python:3.12-slim base with non-root security",
                 "Frontend: Multi-stage node:22-alpine build + nginx:alpine",
                 "Unprivileged NGINX configuration listening on 8080",
                 "Optimized container layers reducing footprint to <150MB",
                 "Explicit .dockerignore preventing secret leakage",
                 "Reproducible builds across local, CI, and production"],
                "PART 6: DOCKER", ACCENT_INDIGO)

    create_card(s4, Inches(8.8), Inches(1.8), Inches(3.6), Inches(5.1), 
                "8. Container Registry (GHCR)",
                ["Hosted on GitHub Container Registry (ghcr.io)",
                 "ghcr.io/shubh-aarambh/studytrack-backend",
                 "ghcr.io/shubh-aarambh/studytrack-frontend",
                 "Dual tagging: Git commit SHA and 'latest'",
                 "Immutable artifact store for Kubernetes node pulls",
                 "Integrates seamlessly with GitHub fine-grained tokens"],
                "PART 8: REGISTRY", ACCENT_GREEN)

    # -------------------------------------------------------------
    # SLIDE 5: SECURITY SCANNING & TERRAFORM (PARTS 7, 9)
    # -------------------------------------------------------------
    s5 = prs.slides.add_slide(blank_layout)
    bg5 = s5.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, Inches(13.333), Inches(7.5))
    bg5.fill.solid()
    bg5.fill.fore_color.rgb = BG_DARK
    bg5.line.fill.background()
    add_header(s5, "Part 7 & 9 — Trivy Security Scanning & Terraform AWS IaC")

    create_card(s5, Inches(0.8), Inches(1.8), Inches(5.6), Inches(5.1), 
                "7. Trivy Security Scanning",
                ["Automated static analysis of container images in CI pipeline",
                 "Scans OS packages and application dependencies for CVEs",
                 "Severity filter: HIGH, CRITICAL vulnerabilities enforced",
                 "Zero-tolerance policy: Build fails if unfixed critical CVE exists",
                 "Backend scan: 0 critical vulnerabilities found",
                 "Frontend scan: 0 critical vulnerabilities found",
                 "SBOM generation and compliance-ready security posture"],
                "PART 7: SECURITY", ACCENT_AMBER)

    create_card(s5, Inches(6.8), Inches(1.8), Inches(5.7), Inches(5.1), 
                "9. Terraform AWS Infrastructure",
                ["Modular infrastructure code organized in terraform/",
                 "AWS VPC: 2 Public subnets, 2 Private subnets, NAT Gateway",
                 "Amazon EKS 1.31: Fully managed control plane with OIDC",
                 "EKS Node Group: EC2 auto-scaling nodes in private subnets",
                 "Security Groups: Strict least-privilege ingress/egress rules",
                 "KMS Encryption: Envelope encryption enabled for K8s Secrets",
                 "IAM Access Entries: Granular RBAC binding for cluster administration"],
                "PART 9: TERRAFORM", ACCENT_BLUE)

    # -------------------------------------------------------------
    # SLIDE 6: KUBERNETES, HELM & INGRESS (PARTS 10, 11, 12)
    # -------------------------------------------------------------
    s6 = prs.slides.add_slide(blank_layout)
    bg6 = s6.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, Inches(13.333), Inches(7.5))
    bg6.fill.solid()
    bg6.fill.fore_color.rgb = BG_DARK
    bg6.line.fill.background()
    add_header(s6, "Part 10, 11, 12 — Kubernetes Workloads, Helm & Ingress Routing")

    create_card(s6, Inches(0.8), Inches(1.8), Inches(3.6), Inches(5.1), 
                "10. Kubernetes Core",
                ["Namespaces: studytrack & taskboard isolation",
                 "Deployments: backend (2 replicas), frontend (2 replicas)",
                 "StatefulSet / Pod: postgres with PersistentVolumeClaim",
                 "ClusterIP Services for secure internal networking",
                 "ConfigMaps & Secrets for database credential injection",
                 "Health & Readiness probes verifying container lifecycle"],
                "PART 10: KUBERNETES", ACCENT_BLUE)

    create_card(s6, Inches(4.8), Inches(1.8), Inches(3.6), Inches(5.1), 
                "11. Helm Charts",
                ["Templated Helm chart located in helm/studytrack",
                 "Environment-specific overrides: values-dev.yaml, values-prod.yaml",
                 "Dynamic replica sizing, resource requests and limits",
                 "Integrated ServiceMonitor & Ingress toggle configurations",
                 "helm upgrade --install for automated zero-downtime rollouts",
                 "Helm release history and rollback capabilities"],
                "PART 11: HELM", ACCENT_INDIGO)

    create_card(s6, Inches(8.8), Inches(1.8), Inches(3.6), Inches(5.1), 
                "12. Ingress Traffic Routing",
                ["NGINX Ingress Controller acts as single entrypoint",
                 "Path-based routing rule:",
                 "  • /api -> studytrack-backend:8000",
                 "  • /    -> studytrack-frontend:80",
                 "External Load Balancer integration with AWS ELB",
                 "CORS header management and SSL/TLS termination support",
                 "Enables seamless client access via dedicated hostname"],
                "PART 12: INGRESS", ACCENT_GREEN)

    # -------------------------------------------------------------
    # SLIDE 7: AUTOSCALING, MONITORING & TROUBLESHOOTING (PARTS 13, 14, 15)
    # -------------------------------------------------------------
    s7 = prs.slides.add_slide(blank_layout)
    bg7 = s7.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, Inches(13.333), Inches(7.5))
    bg7.fill.solid()
    bg7.fill.fore_color.rgb = BG_DARK
    bg7.line.fill.background()
    add_header(s7, "Part 13, 14, 15 — Autoscaling, Observability & Live Failure Simulation")

    create_card(s7, Inches(0.8), Inches(1.8), Inches(3.6), Inches(5.1), 
                "13. HPA & Load Testing",
                ["Horizontal Pod Autoscaler target: 60% CPU utilization",
                 "Scaling boundaries: min 2 pods, max 6 pods",
                 "Load testing scripts in scripts/load-test.ps1 & .sh",
                 "Concurrent load generates realistic request bursts",
                 "HPA automatically detects spike and scales replicas",
                 "Graceful scale-down cooldown prevents thrashing"],
                "PART 13: HPA", ACCENT_AMBER)

    create_card(s7, Inches(4.8), Inches(1.8), Inches(3.6), Inches(5.1), 
                "14. Prometheus & Grafana",
                ["FastAPI Instrumentator exposes metrics at /metrics",
                 "Prometheus Operator with ServiceMonitor configuration",
                 "Grafana dashboards visualize real-time cluster telemetry",
                 "Monitored KPIs: Request rate, HTTP error status, latency p95",
                 "Pod CPU & memory resource consumption graphs",
                 "Proactive alerts for error spikes and pod restarts"],
                "PART 14: MONITORING", ACCENT_BLUE)

    create_card(s7, Inches(8.8), Inches(1.8), Inches(3.6), Inches(5.1), 
                "15. Troubleshooting Scenarios",
                ["Live chaos testing and failure diagnosis runbook",
                 "Scenario A: ImagePullBackOff (invalid tag simulation)",
                 "  • kubectl describe pod -> identify RPC NotFound",
                 "  • Fix tag / secret -> instant pod recovery",
                 "Scenario B: Service Endpoint Mismatch (<none> endpoints)",
                 "  • kubectl get ep -> 0 endpoints detected",
                 "  • Align selector label -> traffic immediately restored"],
                "PART 15: CHAOS & SRE", ACCENT_RED)

    # -------------------------------------------------------------
    # SLIDE 8: SUMMARY & CONCLUSION
    # -------------------------------------------------------------
    s8 = prs.slides.add_slide(blank_layout)
    bg8 = s8.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, Inches(13.333), Inches(7.5))
    bg8.fill.solid()
    bg8.fill.fore_color.rgb = BG_DARK
    bg8.line.fill.background()
    add_header(s8, "DevOps Capstone Summary & Verification Checklist")

    create_card(s8, Inches(0.8), Inches(1.8), Inches(5.6), Inches(5.1), 
                "Capstone Deliverables Completed",
                ["✓ Working full-stack cloud-native application (StudyTrack / TaskBoard)",
                 "✓ 7 REST APIs tested & documented in OpenAPI Swagger /docs",
                 "✓ PostgreSQL relational database with stateful storage",
                 "✓ Automated GitHub Actions CI pipeline with Pytest",
                 "✓ Trivy security scanner with 0 critical vulnerabilities",
                 "✓ Dual multi-stage container images published to GHCR",
                 "✓ Automated AWS VPC & EKS infrastructure via Terraform",
                 "✓ Helm chart packaging with multiple environment values",
                 "✓ NGINX Ingress routing external traffic to microservices",
                 "✓ HPA autoscaling from 2 to 6 replicas under load",
                 "✓ Prometheus scraping and Grafana dashboard visualization",
                 "✓ Live failure simulation and diagnostic runbook in troubleshooting/"],
                "100% OBJECTIVES ACHIEVED", ACCENT_GREEN)

    create_card(s8, Inches(6.8), Inches(1.8), Inches(5.7), Inches(5.1), 
                "Key Engineering Takeaways",
                ["• GitOps Architecture: Every infrastructure and application state change is version-controlled and peer-reviewed.",
                 "• Security by Design: Unprivileged containers, zero-CVE image gating, and KMS secret encryption at rest.",
                 "• Infrastructure Resilience: High-availability multi-AZ deployment with automated healing and scaling.",
                 "• Comprehensive Observability: Full metrics exposure enables immediate root cause identification during incidents.",
                 "• Production Readiness: Helm templating enables reproducible deployments across development, staging, and production environments."],
                "PRODUCTION READY", ACCENT_BLUE)

    prs.save(output_path)
    print(f"Successfully generated presentation at: {output_path}")

if __name__ == "__main__":
    out = os.path.abspath("demo/StudyTrack_DevOps_Capstone_Presentation.pptx")
    if len(sys.argv) > 1:
        out = sys.argv[1]
    create_deck(out)
