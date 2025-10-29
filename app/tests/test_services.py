# --- Default / Positive Test Cases --- #
def test_create_service(client):
    response = client.post(
        "/services/", json={"name": "API Gateway"}
    )  # default set in schema `operational`
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "API Gateway"
    assert data["status"] == "operational"
    assert "id" in data


def test_list_services(client):
    response = client.get("/services/")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) >= 1  # at least one created by previous test


def test_get_service_by_id(client):
    service_list = client.get("/services/").json()
    service_id = service_list[0]["id"]

    response = client.get(f"/services/{service_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == service_id


# --- Nested / Relationship Tests --- #
def test_service_includes_incidents(client):
    # Create service
    service_resp = client.post("/services/", json={"name": "NestedService"})
    service = service_resp.json()

    # Add incidents to that service
    incidents_data = [
        {"service_id": service["id"], "description": "Nested Incident 1"},
        {"service_id": service["id"], "description": "Nested Incident 2"},
    ]
    for incident in incidents_data:
        client.post("/incidents/", json=incident)

    # Fetch service and verify incidents
    response = client.get(f"/services/{service['id']}")
    data = response.json()
    assert response.status_code == 200
    assert "incidents" in data
    assert len(data["incidents"]) == len(incidents_data)
    descriptions = [inc["description"] for inc in data["incidents"]]
    assert "Nested Incident 1" in descriptions
    assert "Nested Incident 2" in descriptions


# --- Negative / Error Test Cases --- #
def test_create_service_invalid_status(client):
    response = client.post(
        "/services/", json={"name": "Cache Service", "status": "invalid_status"}
    )
    assert response.status_code == 422  # Pydantic validation for Literal


def test_get_service_not_found(client):
    response = client.get("/services/99999")  # non-existent ID
    assert response.status_code == 404
    assert response.json()["detail"] == "Service not found"


def test_create_service_duplicate_name(client):
    client.post(
        "/services/", json={"name": "DuplicateService", "status": "operational"}
    )
    response = client.post(
        "/services/", json={"name": "DuplicateService", "status": "operational"}
    )
    assert response.status_code in (400, 409)  # Unique constraint error


def test_service_name_whitespace_only(client):
    response = client.post("/services/", json={"name": "   "})
    assert response.status_code == 422  # Pydantic validation


def test_create_service_missing_status(client):
    response = client.post("/services/", json={"name": "NoStatusService"})
    data = response.json()
    assert response.status_code == 200
    assert data["status"] == "operational"  # default value
