def test_create_service(client):
    response = client.post("/services/", json={"name": "API Gateway"}) # default set in schema `operational``
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
