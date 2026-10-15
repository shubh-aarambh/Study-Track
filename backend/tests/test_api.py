from datetime import date, timedelta


def make(client, **overrides):
    body = {"title": "Complete DevOps capstone", "subject": "DevOps", "priority": "HIGH"}
    body.update(overrides)
    return client.post("/api/assignments", json=body)


def test_health(client):
    assert client.get("/health").json() == {"status": "UP"}


def test_ready_checks_database(client):
    assert client.get("/ready").json() == {"status": "READY"}


def test_root(client):
    response = client.get("/")
    assert response.status_code == 200
    assert response.json()["service"] == "StudyTrack API"


def test_create_assignment(client):
    response = make(client)
    assert response.status_code == 201
    data = response.json()
    assert data["title"] == "Complete DevOps capstone"
    assert data["status"] == "PENDING"
    assert data["progress"] == 0


def test_create_assignment_validation(client):
    assert client.post("/api/assignments", json={"title": ""}).status_code == 422
    assert make(client, priority="URGENT").status_code == 422


def test_list_and_filter_by_subject(client):
    make(client, title="A", subject="Math")
    make(client, title="B", subject="Physics")
    assert len(client.get("/api/assignments").json()) == 2
    math = client.get("/api/assignments", params={"subject": "Math"}).json()
    assert [a["title"] for a in math] == ["A"]


def test_get_assignment_and_404(client):
    created = make(client).json()
    assert client.get(f"/api/assignments/{created['id']}").status_code == 200
    assert client.get("/api/assignments/9999").status_code == 404


def test_update_assignment(client):
    created = make(client).json()
    response = client.put(f"/api/assignments/{created['id']}", json={"status": "IN_PROGRESS", "progress": 40})
    assert response.status_code == 200
    assert response.json()["status"] == "IN_PROGRESS"
    assert response.json()["progress"] == 40


def test_submitting_sets_progress_to_100(client):
    created = make(client).json()
    response = client.put(f"/api/assignments/{created['id']}", json={"status": "SUBMITTED"})
    assert response.json()["progress"] == 100


def test_delete_assignment(client):
    created = make(client).json()
    assert client.delete(f"/api/assignments/{created['id']}").status_code == 204
    assert client.get(f"/api/assignments/{created['id']}").status_code == 404


def test_stats_counts_overdue(client):
    yesterday = (date.today() - timedelta(days=1)).isoformat()
    make(client, title="late", due_date=yesterday)
    make(client, title="done", due_date=yesterday, status="SUBMITTED")
    stats = client.get("/api/assignments/stats").json()
    assert stats["total"] == 2
    assert stats["overdue"] == 1
    assert stats["submitted"] == 1


def test_metrics_endpoint(client):
    client.get("/health")
    body = client.get("/metrics").text
    assert "http_requests_total" in body
