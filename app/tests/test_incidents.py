# --- Default Test Cases --- #
def test_create_incident(client):
    # Create a service first (required foreign key)
    service_data = {
        "name": "Email Service",
        "status": "operational",
        "last_checked": "2025-10-27T00:00:00",
    }
    service_resp = client.post("/services/", json=service_data)
    assert service_resp.status_code == 200
    service = service_resp.json()

    # Now create an incident for that service
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
    assert len(data) >= 1  # at least one incident created earlier


def test_get_incident_by_id(client):
    # list incidents first
    response = client.get("/incidents/")
    assert response.status_code == 200
    data = response.json()
    assert len(data) > 0
    first_id = data[0]["id"]

    # get that incident by ID
    response = client.get(f"/incidents/{first_id}")
    assert response.status_code == 200
    assert response.json()["id"] == first_id


# --- Failure Test Cases -- #
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
    response = client.get("/incidents/99999")  # assuming this ID doesn't exist
    assert response.status_code == 404
    assert response.json()["detail"] == "Incident not found"


def test_create_incident_missing_description(client):
    # Create a valid service first
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
    assert response.status_code == 422  # Pydantic validation
