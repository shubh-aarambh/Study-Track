import sys
import os
from pptx import Presentation
from pptx.util import Inches, Pt
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
        p_title.font.size = Pt(22)
        p_title.font.bold = True
        p_title.font.color.rgb = TEXT_LIGHT

    def create_card(slide, left, top, width, height, title, items, badge="", badge_color=ACCENT_BLUE):
        shape = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, top, width, height)
        shape.fill.solid()
        shape.fill.fore_color.rgb = BG_CARD
        shape.line.color.rgb = RGBColor(51, 65, 85)
        shape.line.width = Pt(1)

        tb = slide.shapes.add_textbox(left + Inches(0.25), top + Inches(0.2), width - Inches(0.5), height - Inches(0.4))
        tf = tb.text_frame
        tf.word_wrap = True
        tf.margin_left = tf.margin_top = tf.margin_right = tf.margin_bottom = 0

        p_head = tf.paragraphs[0]
        p_head.text = title
        p_head.font.size = Pt(14)
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
            p.text = f"• {item}"
            p.font.size = Pt(10.5)
            p.font.color.rgb = TEXT_LIGHT
            p.space_after = Pt(3)

    def add_image_safe(slide, img_path, left, top, width, height):
        if os.path.exists(img_path):
            slide.shapes.add_picture(img_path, left, top, width, height)

    # -------------------------------------------------------------
    # SLIDE 1: TITLE SLIDE
    # -------------------------------------------------------------
    s1 = prs.slides.add_slide(blank_layout)
    bg1 = s1.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, Inches(13.333), Inches(7.5))
    bg1.fill.solid()
    bg1.fill.fore_color.rgb = BG_DARK
    bg1.line.fill.background()

    tb1 = s1.shapes.add_textbox(Inches(1.2), Inches(1.5), Inches(11), Inches(4.8))
    tf1 = tb1.text_frame
    tf1.word_wrap = True

    p = tf1.paragraphs[0]
    p.text = "DEVOPS CAPSTONE FINAL PRESENTATION — SESSION 21"
    p.font.size = Pt(13)
    p.font.bold = True
    p.font.color.rgb = ACCENT_BLUE
    p.space_after = Pt(12)

    p = tf1.add_paragraph()
    p.text = "StudyTrack"
    p.font.size = Pt(38)
    p.font.bold = True
    p.font.color.rgb = TEXT_LIGHT

    p = tf1.add_paragraph()
    p.text = "Production GitOps Architecture: From Code to Monitored AWS EKS Cluster"
    p.font.size = Pt(18)
    p.font.color.rgb = TEXT_MUTED
    p.space_after = Pt(24)

    p = tf1.add_paragraph()
    p.text = "Candidate: shubh-aarambh  |  Domain: Academic Coursework & Deadline Management System"
    p.font.size = Pt(13)
    p.font.bold = True
    p.font.color.rgb = ACCENT_GREEN
    p.space_after = Pt(12)

    p = tf1.add_paragraph()
    p.text = "Demonstrating the Complete 15-Stage DevOps Lifecycle:\nApplication → Git → CI Pipeline → Docker → Trivy Scan → GHCR → Terraform → Kubernetes → Helm → Ingress → Autoscaling → Monitoring → Troubleshooting"
    p.font.size = Pt(11)
    p.font.color.rgb = TEXT_MUTED

    # -------------------------------------------------------------
    # SLIDE 2: END-TO-END WORKFLOW
    # -------------------------------------------------------------
    s2 = prs.slides.add_slide(blank_layout)
    bg2 = s2.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, Inches(13.333), Inches(7.5))
    bg2.fill.solid()
    bg2.fill.fore_color.rgb = BG_DARK
    bg2.line.fill.background()
    add_header(s2, "End-to-End DevOps Architecture & Toolchain")

    create_card(s2, Inches(0.8), Inches(1.8), Inches(3.6), Inches(5.1), 
                "Phase 1: CI & Code Security",
                ["FastAPI + React (Vite) + PostgreSQL 16",
                 "12 Automated tests with pytest & SQLite isolation",
                 "Frontend production bundling with Vite & Node 22",
                 "Multi-stage Docker builds (slim / alpine)",
                 "Trivy vulnerability scanner: 0 HIGH / CRITICAL CVEs",
                 "Automated container publish to GHCR with commit SHA"],
                "AUTOMATED CI & GITOPS", ACCENT_BLUE)

    create_card(s2, Inches(4.8), Inches(1.8), Inches(3.6), Inches(5.1), 
                "Phase 2: Cloud Infrastructure",
                ["Terraform IaC provisioning in AWS ap-south-1",
                 "AWS VPC: 2 Public + 2 Private subnets + NAT Gateway",
                 "Amazon EKS 1.31 Managed Kubernetes Cluster",
                 "EKS Managed Node Group with Free Tier t3.small instances",
                 "OIDC Provider & IAM Least-Privilege Policies",
                 "KMS Envelope Encryption for Kubernetes Secrets"],
                "TERRAFORM & AWS EKS", ACCENT_INDIGO)

    create_card(s2, Inches(8.8), Inches(1.8), Inches(3.6), Inches(5.1), 
                "Phase 3: Delivery & SRE",
                ["Helm packaging with values for production cluster namespace",
                 "NGINX Ingress Controller with AWS ELB integration",
                 "Horizontal Pod Autoscaler (HPA) targeting 60% CPU",
                 "Prometheus metrics scraping (/metrics endpoint)",
                 "Grafana real-time telemetry dashboards",
                 "Chaos engineering & Live service troubleshooting runbook"],
                "HELM, INGRESS & OBSERVABILITY", ACCENT_GREEN)

    # -------------------------------------------------------------
    # SLIDE 3: PART 1 & 2 - APP & API
    # -------------------------------------------------------------
    s3 = prs.slides.add_slide(blank_layout)
    bg3 = s3.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, Inches(13.333), Inches(7.5))
    bg3.fill.solid()
    bg3.fill.fore_color.rgb = BG_DARK
    bg3.line.fill.background()
    add_header(s3, "Part 1 & 2 — Application UI & FastAPI Swagger REST API Suite")

    create_card(s3, Inches(0.8), Inches(1.8), Inches(5.6), Inches(2.5),
                "1. StudyTrack Academic Workspace UI",
                ["Modern glassmorphism UI with live assignment & deadline tracking",
                 "Status columns: PENDING, IN_PROGRESS, SUBMITTED",
                 "Real-time completion percentage calculations and progress bars",
                 "Interactive modal for task creation with validation"],
                "PART 1: APPLICATION", ACCENT_BLUE)

    create_card(s3, Inches(0.8), Inches(4.5), Inches(5.6), Inches(2.4),
                "2. FastAPI Swagger OpenAPI Suite (/docs)",
                ["GET /api/assignments — List & filter by subject",
                 "POST /api/assignments — Create task (201 Created)",
                 "GET/PUT/DELETE /api/assignments/{id} — Full CRUD operations",
                 "GET /health, /ready, /metrics — Probes & telemetry"],
                "PART 2: REST API", ACCENT_INDIGO)

    add_image_safe(s3, "demo/screenshots/01-application-taskboard.png", Inches(6.8), Inches(1.8), Inches(5.8), Inches(2.5))
    add_image_safe(s3, "demo/screenshots/02-fastapi-swagger-docs.png", Inches(6.8), Inches(4.5), Inches(5.8), Inches(2.4))

    # -------------------------------------------------------------
    # SLIDE 4: PART 3, 4, 5 - DATABASE, GIT & CI
    # -------------------------------------------------------------
    s4 = prs.slides.add_slide(blank_layout)
    bg4 = s4.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, Inches(13.333), Inches(7.5))
    bg4.fill.solid()
    bg4.fill.fore_color.rgb = BG_DARK
    bg4.line.fill.background()
    add_header(s4, "Part 3, 4, 5 — PostgreSQL Database, GitOps & CI Pipeline")

    create_card(s4, Inches(0.8), Inches(1.8), Inches(5.6), Inches(2.5),
                "3. PostgreSQL Relational Persistence",
                ["Stateful workload deployed in Kubernetes production namespace",
                 "SQLAlchemy ORM with strict Pydantic schemas",
                 "Persistent tasks verified directly via psql CLI in pod",
                 "Columns: id, title, subject, priority, status, progress, created_at"],
                "PART 3: DATABASE", ACCENT_GREEN)

    create_card(s4, Inches(0.8), Inches(4.5), Inches(5.6), Inches(2.4),
                "4 & 5. Git Commit & GitHub Actions CI",
                ["Automated trigger on push to branch 'main'",
                 "Pytest execution: 12 unit & integration tests passing in 0.50s",
                 "Vite client production compilation and artifact verification",
                 "Traceable Git commit SHA tagging for container images"],
                "PARTS 4 & 5: GIT & CI", ACCENT_BLUE)

    add_image_safe(s4, "demo/screenshots/03-postgresql-database-table.png", Inches(6.8), Inches(1.8), Inches(5.8), Inches(2.5))
    add_image_safe(s4, "demo/screenshots/05-ci-pipeline-tests.png", Inches(6.8), Inches(4.5), Inches(5.8), Inches(2.4))

    # -------------------------------------------------------------
    # SLIDE 5: PART 6, 7, 8 - DOCKER, TRIVY & REGISTRY
    # -------------------------------------------------------------
    s5 = prs.slides.add_slide(blank_layout)
    bg5 = s5.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, Inches(13.333), Inches(7.5))
    bg5.fill.solid()
    bg5.fill.fore_color.rgb = BG_DARK
    bg5.line.fill.background()
    add_header(s5, "Part 6, 7, 8 — Docker Packaging, Trivy Security Scan & GHCR")

    create_card(s5, Inches(0.8), Inches(1.8), Inches(5.6), Inches(2.5),
                "6 & 8. Docker Builds & GHCR Registry",
                ["Backend: python:3.12-slim base image (142 MB)",
                 "Frontend: Multi-stage node:22 build + unprivileged nginx (28 MB)",
                 "Published to GitHub Container Registry (ghcr.io)",
                 "Tagged with full commit SHA and 'latest' for production parity"],
                "PARTS 6 & 8: DOCKER & REGISTRY", ACCENT_BLUE)

    create_card(s5, Inches(0.8), Inches(4.5), Inches(5.6), Inches(2.4),
                "7. Trivy Static Security Scanning",
                ["Automated security gate in CI: fails on HIGH or CRITICAL CVEs",
                 "Backend scan result: 0 HIGH / 0 CRITICAL vulnerabilities",
                 "Frontend scan result: 0 HIGH / 0 CRITICAL vulnerabilities",
                 "Minimal attack surface with non-root runtime permissions"],
                "PART 7: SECURITY", ACCENT_AMBER)

    add_image_safe(s5, "demo/screenshots/06-docker-images-build.png", Inches(6.8), Inches(1.8), Inches(5.8), Inches(2.5))
    add_image_safe(s5, "demo/screenshots/07-trivy-security-scan.png", Inches(6.8), Inches(4.5), Inches(5.8), Inches(2.4))

    # -------------------------------------------------------------
    # SLIDE 6: PART 9, 10, 11 - TERRAFORM, K8S & HELM
    # -------------------------------------------------------------
    s6 = prs.slides.add_slide(blank_layout)
    bg6 = s6.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, Inches(13.333), Inches(7.5))
    bg6.fill.solid()
    bg6.fill.fore_color.rgb = BG_DARK
    bg6.line.fill.background()
    add_header(s6, "Part 9, 10, 11 — Terraform IaC, Kubernetes & Helm Releases")

    create_card(s6, Inches(0.8), Inches(1.8), Inches(5.6), Inches(2.5),
                "9. Terraform Infrastructure Code",
                ["Modular AWS VPC: 2 Public + 2 Private Subnets + NAT Gateway",
                 "Amazon EKS 1.31 cluster with AWS KMS encryption key",
                 "EKS Managed Node Group with Free Tier eligible t3.small instances",
                 "IAM Access Entries & ClusterAdminPolicy associated for root caller"],
                "PART 9: TERRAFORM", ACCENT_BLUE)

    create_card(s6, Inches(0.8), Inches(4.5), Inches(5.6), Inches(2.4),
                "10 & 11. Kubernetes & Helm Deployment",
                ["Production Workloads: backend (2 replicas), frontend (2 replicas), postgres (1)",
                 "Helm chart: helm/studytrack with values overriding image tags",
                 "ClusterIP services for secure internal communication",
                 "Automated rolling upgrades with zero service downtime"],
                "PARTS 10 & 11: K8S & HELM", ACCENT_INDIGO)

    add_image_safe(s6, "demo/screenshots/09-terraform-infrastructure.png", Inches(6.8), Inches(1.8), Inches(5.8), Inches(2.5))
    add_image_safe(s6, "demo/screenshots/10-kubernetes-pods-services.png", Inches(6.8), Inches(4.5), Inches(5.8), Inches(2.4))

    # -------------------------------------------------------------
    # SLIDE 7: PART 12 & 13 - INGRESS & HPA
    # -------------------------------------------------------------
    s7 = prs.slides.add_slide(blank_layout)
    bg7 = s7.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, Inches(13.333), Inches(7.5))
    bg7.fill.solid()
    bg7.fill.fore_color.rgb = BG_DARK
    bg7.line.fill.background()
    add_header(s7, "Part 12 & 13 — NGINX Ingress Routing & Horizontal Pod Autoscaler")

    create_card(s7, Inches(0.8), Inches(1.8), Inches(5.6), Inches(2.5),
                "12. NGINX Ingress Controller & AWS ELB",
                ["Single entrypoint provisioned via AWS Elastic Load Balancer (ELB)",
                 "Path-based routing: /api -> backend:8000, / -> frontend:80",
                 "Public hostname: a554166002e3d4c6bbb0bde1c641c9c1...ap-south-1.elb.amazonaws.com",
                 "Tested live across internet with HTTP 200 responses"],
                "PART 12: INGRESS", ACCENT_GREEN)

    create_card(s7, Inches(0.8), Inches(4.5), Inches(5.6), Inches(2.4),
                "13. Horizontal Pod Autoscaler (HPA)",
                ["Target metric: 60% CPU utilization with Metrics Server integration",
                 "Boundaries: Minimum 2 replicas, Maximum 6 replicas",
                 "Tested with scripts/load-test.ps1 (~108 req/sec concurrent load)",
                 "Automatic scale-up during traffic bursts and cooldown downscaling"],
                "PART 13: HPA", ACCENT_AMBER)

    add_image_safe(s7, "demo/screenshots/12-ingress-live-app.png", Inches(6.8), Inches(1.8), Inches(5.8), Inches(2.5))
    add_image_safe(s7, "demo/screenshots/13-hpa-horizontal-pod-autoscaler.png", Inches(6.8), Inches(4.5), Inches(5.8), Inches(2.4))

    # -------------------------------------------------------------
    # SLIDE 8: PART 14 & 15 - MONITORING & TROUBLESHOOTING
    # -------------------------------------------------------------
    s8 = prs.slides.add_slide(blank_layout)
    bg8 = s8.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, Inches(13.333), Inches(7.5))
    bg8.fill.solid()
    bg8.fill.fore_color.rgb = BG_DARK
    bg8.line.fill.background()
    add_header(s8, "Part 14 & 15 — Prometheus/Grafana Monitoring & Chaos Troubleshooting")

    create_card(s8, Inches(0.8), Inches(1.8), Inches(5.6), Inches(2.5),
                "14. Prometheus & Grafana Observability",
                ["kube-prometheus-stack deployed in namespace monitoring",
                 "FastAPI Instrumentator exposes metrics on /metrics",
                 "Prometheus scrapes pods, services, and cluster node metrics",
                 "Grafana dashboards visualize CPU, memory, request rates, p95 latency"],
                "PART 14: MONITORING", ACCENT_BLUE)

    create_card(s8, Inches(0.8), Inches(4.5), Inches(5.6), Inches(2.4),
                "15. Live Troubleshooting Simulation",
                ["Simulated failure: broken service with selector label mismatch",
                 "Diagnosis: kubectl get endpoints broken-service -> <none> detected",
                 "Remediation: Patched selector to app=studytrack-backend",
                 "Verification: Endpoints immediately populated with active Pod IPs"],
                "PART 15: CHAOS & SRE", ACCENT_RED)

    add_image_safe(s8, "demo/screenshots/14-grafana-cluster-dashboard.png", Inches(6.8), Inches(1.8), Inches(5.8), Inches(2.5))
    add_image_safe(s8, "demo/screenshots/15-live-troubleshooting-remediation.png", Inches(6.8), Inches(4.5), Inches(5.8), Inches(2.4))

    # -------------------------------------------------------------
    # SLIDE 9: SUMMARY & DEMO ARTIFACTS
    # -------------------------------------------------------------
    s9 = prs.slides.add_slide(blank_layout)
    bg9 = s9.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, Inches(13.333), Inches(7.5))
    bg9.fill.solid()
    bg9.fill.fore_color.rgb = BG_DARK
    bg9.line.fill.background()
    add_header(s9, "Summary & Demo Artifact Deliverables")

    create_card(s9, Inches(0.8), Inches(1.8), Inches(5.6), Inches(5.1),
                "Project Verification Checklist",
                ["✓ 1. Application: StudyTrack Academic UI interactive and responsive",
                 "✓ 2. API: FastAPI OpenAPI /docs with full CRUD endpoints verified",
                 "✓ 3. Database: PostgreSQL stateful storage with persistent rows",
                 "✓ 4. Git: Version-controlled commits on branch 'main'",
                 "✓ 5. CI: GitHub Actions automated pytest suite passing in CI",
                 "✓ 6. Docker: Multi-stage lightweight images (<150MB)",
                 "✓ 7. Security: Trivy scanner verified with 0 CVEs",
                 "✓ 8. Registry: Published to GitHub Container Registry (GHCR)",
                 "✓ 9. Terraform: Automated AWS VPC + EKS cluster in ap-south-1",
                 "✓ 10. Kubernetes: All pods & services running in production cluster namespace",
                 "✓ 11. Helm: Helm chart deployed with zero-downtime upgrades",
                 "✓ 12. Ingress: AWS ELB public routing with live browser demo",
                 "✓ 13. HPA: Horizontal Pod Autoscaler active with CPU utilization metrics",
                 "✓ 14. Monitoring: Prometheus and Grafana dashboards live",
                 "✓ 15. Troubleshooting: Live service endpoint failure diagnosed and resolved"],
                "100% OBJECTIVES ACHIEVED", ACCENT_GREEN)

    create_card(s9, Inches(6.8), Inches(1.8), Inches(5.7), Inches(5.1),
                "Generated Artifacts in demo/",
                ["📄 demo/StudyTrack_DevOps_Capstone_Presentation.pdf",
                 "   • Browser-viewable slide deck (opens directly without downloading)",
                 "",
                 "📁 demo/StudyTrack_DevOps_Capstone_Presentation.pptx",
                 "   • Complete 9-slide executive & technical slide deck source",
                 "",
                 "🎬 demo/studytrack_tour.gif",
                 "   • In-browser animated tour (plays directly on GitHub without downloading)",
                 "",
                 "📹 demo/studytrack_full_tour.mp4",
                 "   • Broadcast-grade 720p HD MP4 video recording (18.5 MB)",
                 "",
                 "🖼️ demo/screenshots/",
                 "   • 21 High-definition screenshots covering all 15 rubric criteria"],
                "DEMO ARTIFACTS", ACCENT_BLUE)

    prs.save(output_path)
    print(f"Successfully generated presentation at: {output_path}")

if __name__ == "__main__":
    out = os.path.abspath("demo/StudyTrack_DevOps_Capstone_Presentation.pptx")
    if len(sys.argv) > 1:
        out = sys.argv[1]
    create_deck(out)
