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
