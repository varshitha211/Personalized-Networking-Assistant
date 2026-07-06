import pytest


class TestSessionsRoutes:
    def test_list_sessions_empty(self, client):
        resp = client.get("/api/sessions/")
        assert resp.status_code == 200
        assert resp.json() == []

    def test_get_session_not_found(self, client):
        resp = client.get("/api/sessions/999")
        assert resp.status_code == 404

    def test_get_session_history_not_found(self, client):
        resp = client.get("/api/sessions/999/history")
        assert resp.status_code == 404


class TestStartersRoutes:
    def test_generate_starters_returns_starters(self, client, sample_event_description, sample_interests):
        resp = client.post(
            "/api/starters/generate",
            json={
                "event_description": sample_event_description,
                "interests": sample_interests,
            },
        )
        assert resp.status_code == 200
        data = resp.json()
        assert "session_id" in data
        assert "starters" in data
        assert len(data["starters"]) > 0
        assert "themes" in data

    def test_generate_starters_empty_event(self, client):
        resp = client.post(
            "/api/starters/generate",
            json={"event_description": "", "interests": ""},
        )
        assert resp.status_code == 422

    def test_generate_starters_defaults(self, client):
        resp = client.post(
            "/api/starters/generate",
            json={"event_description": "Tech meetup", "interests": ""},
        )
        assert resp.status_code == 200
        data = resp.json()
        assert len(data["starters"]) > 0

    def test_submit_feedback_not_found(self, client):
        resp = client.post(
            "/api/starters/feedback",
            json={"starter_id": 999, "feedback": 1},
        )
        assert resp.status_code == 404

    def test_submit_feedback_invalid_value(self, client):
        resp = client.post(
            "/api/starters/feedback",
            json={"starter_id": 1, "feedback": 99},
        )
        assert resp.status_code == 422

    def test_feedback_flow(self, client, sample_event_description):
        gen_resp = client.post(
            "/api/starters/generate",
            json={"event_description": sample_event_description, "interests": ""},
        )
        assert gen_resp.status_code == 200
        session_id = gen_resp.json()["session_id"]

        starters_resp = client.get(f"/api/starters/session/{session_id}")
        assert starters_resp.status_code == 200
        starters = starters_resp.json()
        assert len(starters) > 0

        sid = starters[0]["StarterID"]
        fb_resp = client.post(
            "/api/starters/feedback",
            json={"starter_id": sid, "feedback": 1},
        )
        assert fb_resp.status_code == 200
        assert fb_resp.json()["Feedback"] == 1

    def test_generate_with_interests(self, client):
        resp = client.post(
            "/api/starters/generate",
            json={
                "event_description": "Healthcare AI Summit",
                "interests": "machine learning, healthcare",
            },
        )
        assert resp.status_code == 200
        data = resp.json()
        assert len(data["starters"]) > 0


class TestFactCheckRoutes:
    def test_fact_check_returns_result(self, client):
        resp = client.post("/api/factcheck/", json={"query": "Python"})
        assert resp.status_code == 200
        data = resp.json()
        assert "query" in data
        assert "summary" in data
        assert "status" in data

    def test_fact_check_empty_query(self, client):
        resp = client.post("/api/factcheck/", json={"query": ""})
        assert resp.status_code == 422

    def test_list_fact_checks(self, client):
        resp = client.get("/api/factcheck/")
        assert resp.status_code == 200


class TestHistoryRoutes:
    def test_get_session_history_empty(self, client):
        resp = client.get("/api/history/sessions")
        assert resp.status_code == 200
        assert isinstance(resp.json(), list)

    def test_get_feedback_history_empty(self, client):
        resp = client.get("/api/history/feedback")
        assert resp.status_code == 200
        assert isinstance(resp.json(), list)

    def test_get_logs(self, client):
        resp = client.get("/api/history/logs")
        assert resp.status_code == 200

    def test_history_after_generation(self, client, sample_event_description):
        client.post(
            "/api/starters/generate",
            json={"event_description": sample_event_description, "interests": ""},
        )
        resp = client.get("/api/history/sessions")
        assert resp.status_code == 200
        data = resp.json()
        assert len(data) > 0
        assert "session_id" in data[0]
        assert "starters" in data[0]


class TestHealthCheck:
    def test_root_endpoint(self, client):
        resp = client.get("/")
        assert resp.status_code == 200
        assert resp.json()["status"] == "running"

    def test_health_endpoint(self, client):
        resp = client.get("/health")
        assert resp.status_code == 200
        assert resp.json()["status"] == "healthy"
