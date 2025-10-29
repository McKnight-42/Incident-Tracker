# --- Good test cases --- #
def test_create_service(client):
    response = client.post(
        "/services/", json={"name": "API Gateway"}
    )  # default set in schema `operational``
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
    # Get the first service created above
    service_list = client.get("/services/").json()
    service_id = service_list[0]["id"]

    response = client.get(f"/services/{service_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == service_id


# -- Error Tests -- #
def test_create_service_invalid_status(client):
    response = client.post(
        "/services/", json={"name": "Cache Service", "status": "invalid_status"}
    )
    assert response.status_code == 422  # Pydantic validation for Literal


def test_get_service_not_found(client):
    response = client.get("/services/99999")  # assuming this ID doesn't exist
    assert response.status_code == 404
    assert response.json()["detail"] == "Service not found"


def test_create_service_duplicate_name(client):
    client.post(
        "/services/", json={"name": "DuplicateService", "status": "operational"}
    )
    response = client.post(
        "/services/", json={"name": "DuplicateService", "status": "operational"}
    )
    assert response.status_code in (
        400,
        409,
    )  # depending on how you want to handle unique constraints
