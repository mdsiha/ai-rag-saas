def test_register_user(client):
    response = client.post(
        "/register",
        json={"email": "a@b.com", "password": "123456"},
    )
    assert response.status_code == 201
    assert response.json() == {"message": "User registered successfully"}


def test_register_duplicate_email(client):
    client.post(
        "/register",
        json={"email": "a@b.com", "password": "123456"},
    )
    response = client.post(
        "/register",
        json={"email": "a@b.com", "password": "123456"},
    )
    assert response.status_code == 400
    assert "already registered" in response.json()["detail"]


def test_login_success(client):
    client.post(
        "/register", json={"email": "login@example.com", "password": "password123"}
    )
    response = client.post(
        "/login", data={"username": "login@example.com", "password": "password123"}
    )
    assert response.status_code == 200
    assert "access_token" in response.json()
    assert response.json()["token_type"] == "bearer"
