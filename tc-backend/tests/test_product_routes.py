def test_get_product(client):
    response = client.get("/api/v1/products")
    assert response.status_code == 200
    assert response.get_json() == [{"name": "wine"}]
