# --- Default / Positive Test Cases --- #
def test_create_incident(client):
    # Create a service first
    service_resp = client.post(
        "/services/", json={"name": "Email Service", "status": "operational"}
    )
    service = service_resp.json()

    # Create an incident for that service
    incident_data = {
        "service_id": service["id"],
        "description": "Email delivery delayed",
        "start_time": "2025-10-27T00:00:00",
        "resolved_time": None,
    }
    response = client.post("/incidents/", json=incident_data)
    assert response.status_code == 200
    data = response.json()
    assert data["description"] == "Email delivery delayed"
    assert data["service_id"] == service["id"]


def test_list_incidents(client):
    response = client.get("/incidents/")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) >= 1


def test_get_incident_by_id(client):
    response = client.get("/incidents/")
    assert response.status_code == 200
    data = response.json()
    first_id = data[0]["id"]

    response = client.get(f"/incidents/{first_id}")
    assert response.status_code == 200
    assert response.json()["id"] == first_id


# --- Negative / Error Test Cases --- #
def test_create_incident_invalid_service(client):
    incident_data = {
        "service_id": 99999,  # non-existent service
        "description": "Fake incident",
        "start_time": "2025-10-27T00:00:00",
        "resolved_time": None,
    }
    response = client.post("/incidents/", json=incident_data)
    assert response.status_code in (404, 422)


def test_get_incident_not_found(client):
    response = client.get("/incidents/99999")  # non-existent ID
    assert response.status_code == 404
    assert response.json()["detail"] == "Incident not found"


def test_create_incident_missing_description(client):
    service_resp = client.post(
        "/services/", json={"name": "Email Service 2", "status": "operational"}
    )
    service = service_resp.json()

    incident_data = {
        "service_id": service["id"],
        "start_time": "2025-10-27T00:00:00",
        "resolved_time": None,
    }
    response = client.post("/incidents/", json=incident_data)
    assert response.status_code == 422


# --- Additional Edge Cases --- #
def test_create_incident_missing_service_id(client):
    incident_data = {"description": "No service provided"}
    response = client.post("/incidents/", json=incident_data)
    assert response.status_code == 422


def test_create_incident_resolved_before_start(client):
    service_resp = client.post("/services/", json={"name": "EdgeIncidentService"})
    service = service_resp.json()

    incident_data = {
        "service_id": service["id"],
        "description": "Backwards times",
        "start_time": "2025-10-27T01:00:00",
        "resolved_time": "2025-10-27T00:00:00",
    }
    response = client.post("/incidents/", json=incident_data)
    assert response.status_code == 200


def test_create_incident_invalid_types(client):
    # Ensure there is at least one service in DB
    client.post("/services/", json={"name": "TypeTestService"})

    incident_data = {
        "service_id": "not-an-int",
        "description": "Type error incident",
        "start_time": "2025-10-27T00:00:00",
    }

    response = client.post("/incidents/", json=incident_data)
    assert response.status_code == 422
