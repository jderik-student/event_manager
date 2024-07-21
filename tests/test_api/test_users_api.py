from builtins import str
from faker import Faker
import pytest
from httpx import AsyncClient
from app.main import app
from app.models.user_model import User
from app.utils.nickname_gen import generate_nickname
from app.utils.security import hash_password
from app.services.jwt_service import decode_token  # Import your FastAPI app

fake = Faker()

# Example of a test function using the async_client fixture
@pytest.mark.asyncio
async def test_create_user_access_denied(async_client, user_token, email_service):
    headers = {"Authorization": f"Bearer {user_token}"}
    # Define user data for the test
    user_data = {
        "nickname": generate_nickname(),
        "email": "test@example.com",
        "password": "sS#fdasrongPassword123!",
    }
    # Send a POST request to create a user
    response = await async_client.post("/users/", json=user_data, headers=headers)
    # Asserts
    assert response.status_code == 403

@pytest.mark.asyncio
async def test_create_admin_access_different_usernames(async_client, verified_user, admin_token):
    user_data_too_short = {
        "nickname": "short",
        "email": "test@example.com",
        "password": "sS#fdasrongPassword123!",
    }
    user_data_too_long = {
        "nickname": "0123456789012345678901",
        "email": "test@example.com",
        "password": "sS#fdasrongPassword123!",
    }
    user_data_invalid_character = {
        "nickname": "nickname!",
        "email": "test@example.com",
        "password": "sS#fdasrongPassword123!",
    }
    user_data_duplicate_username = {
        "nickname": verified_user.nickname,
        "email": "test@example.com",
        "password": "sS#fdasrongPassword123!",
    }
    user_data_valid_username = {
        "nickname": "joe_cool_123",
        "email": "test@example.com",
        "password": "sS#fdasrongPassword123!",
    }
    headers = {"Authorization": f"Bearer {admin_token}"}
    response = await async_client.post("/users/", json=user_data_too_short, headers=headers)
    assert response.status_code == 422
    response = await async_client.post("/users/", json=user_data_too_long, headers=headers)
    assert response.status_code == 422
    response = await async_client.post("/users/", json=user_data_invalid_character, headers=headers)
    assert response.status_code == 422
    response = await async_client.post("/users/", json=user_data_duplicate_username, headers=headers)
    assert response.status_code == 400
    response = await async_client.post("/users/", json=user_data_valid_username, headers=headers)
    assert response.status_code == 201
    assert response.json()["nickname"] == user_data_valid_username["nickname"]

# You can similarly refactor other test functions to use the async_client fixture
@pytest.mark.asyncio
async def test_retrieve_user_access_denied(async_client, verified_user, user_token):
    headers = {"Authorization": f"Bearer {user_token}"}
    response = await async_client.get(f"/users/{verified_user.id}", headers=headers)
    assert response.status_code == 403

@pytest.mark.asyncio
async def test_retrieve_user_access_allowed(async_client, admin_user, admin_token):
    headers = {"Authorization": f"Bearer {admin_token}"}
    response = await async_client.get(f"/users/{admin_user.id}", headers=headers)
    assert response.status_code == 200
    assert response.json()["id"] == str(admin_user.id)

@pytest.mark.asyncio
async def test_update_user_email_access_denied(async_client, verified_user, user_token):
    updated_data = {"email": f"updated_{verified_user.id}@example.com"}
    headers = {"Authorization": f"Bearer {user_token}"}
    response = await async_client.put(f"/users/{verified_user.id}", json=updated_data, headers=headers)
    assert response.status_code == 403

@pytest.mark.asyncio
async def test_update_user_email_access_allowed(async_client, admin_user, admin_token):
    updated_data = {"email": f"updated_{admin_user.id}@example.com"}
    headers = {"Authorization": f"Bearer {admin_token}"}
    response = await async_client.put(f"/users/{admin_user.id}", json=updated_data, headers=headers)
    assert response.status_code == 200
    assert response.json()["email"] == updated_data["email"]

@pytest.mark.asyncio
async def test_update_nicknames(async_client, admin_user, admin_token, verified_user):
    updated_data_too_short = {"nickname": "short"}
    updated_data_too_long = {"nickname": "0123456789012345678901"}
    updated_data_invalid_character = {"nickname": "nickname!"}
    updated_data_duplicate_nickname = {"nickname": verified_user.nickname}
    updated_data_valid_username = {"nickname": "joe_cool_123"}
    headers = {"Authorization": f"Bearer {admin_token}"}
    response = await async_client.put(f"/users/{admin_user.id}", json=updated_data_too_short, headers=headers)
    assert response.status_code == 422
    response = await async_client.put(f"/users/{admin_user.id}", json=updated_data_too_long, headers=headers)
    assert response.status_code == 422
    response = await async_client.put(f"/users/{admin_user.id}", json=updated_data_invalid_character, headers=headers)
    assert response.status_code == 422
    response = await async_client.put(f"/users/{admin_user.id}", json=updated_data_duplicate_nickname, headers=headers)
    assert response.status_code == 400
    response = await async_client.put(f"/users/{admin_user.id}", json=updated_data_valid_username, headers=headers)
    assert response.status_code == 200
    assert response.json()["nickname"] == updated_data_valid_username["nickname"]


@pytest.mark.asyncio
async def test_delete_user(async_client, admin_user, admin_token):
    headers = {"Authorization": f"Bearer {admin_token}"}
    delete_response = await async_client.delete(f"/users/{admin_user.id}", headers=headers)
    assert delete_response.status_code == 204
    # Verify the user is deleted
    fetch_response = await async_client.get(f"/users/{admin_user.id}", headers=headers)
    assert fetch_response.status_code == 404

@pytest.mark.asyncio
async def test_register_user_duplicate_email(async_client, verified_user):
    user_data = {
        "email": verified_user.email,
        "password": "AnotherPassword123!",
    }
    response = await async_client.post("/register/", json=user_data)
    assert response.status_code == 400
    assert "Email already exists" in response.json().get("detail", "")

@pytest.mark.asyncio
async def test_create_user_duplicate_email(async_client, verified_user, admin_token):
    user_data = {"nickname": "joe_cool_1234",
                 "email": verified_user.email,
                 "password": "sS#fdasrongPassword123!", 
    }
    headers = {"Authorization": f"Bearer {admin_token}"}
    response = await async_client.post("/users/", json=user_data, headers=headers)
    assert response.status_code == 400
    assert "Email already exists" in response.json().get("detail", "")

@pytest.mark.asyncio
async def test_update_user_duplicate_email(async_client, admin_user, admin_token, verified_user):
    user_data = {"email": verified_user.email}
    headers = {"Authorization": f"Bearer {admin_token}"}
    response = await async_client.put(f"/users/{admin_user.id}", json=user_data, headers=headers)
    assert response.status_code == 400
    assert "Email already exists" in response.json().get("detail", "")

@pytest.mark.asyncio
async def test_create_user_invalid_email(async_client):
    user_data = {
        "email": "notanemail",
        "password": "ValidPassword123!",
    }
    response = await async_client.post("/register/", json=user_data)
    assert response.status_code == 422

@pytest.mark.asyncio
async def test_register_user_invalid_nicknames(async_client, verified_user):
    unique_email = fake.email()
    user_data_too_short = {
        "email": unique_email,
        "password": "ValidPassword123!",
        "nickname": "short",
    }
    user_data_too_long = {
        "email": unique_email,
        "password": "ValidPassword123!",
        "nickname": "123456789012345678901",
    }
    user_data_invalid_character = {
        "email": unique_email,
        "password": "ValidPassword123!",
        "nickname": "nickname!",
    }
    user_data_duplicate_nickname = {
        "email": unique_email,
        "password": "ValidPassword123!",
        "nickname": verified_user.nickname,
    }
    response = await async_client.post("/register/", json=user_data_too_short)
    assert response.status_code == 422
    response = await async_client.post("/register/", json=user_data_too_long)
    assert response.status_code == 422
    response = await async_client.post("/register/", json=user_data_invalid_character)
    assert response.status_code == 422
    response = await async_client.post("/register/", json=user_data_duplicate_nickname)
    assert response.status_code == 400

@pytest.mark.asyncio
async def test_register_user_invalid_length_password(async_client, verified_user):
    user_data_too_short_password = {
        "email": fake.email(),
        "password": "pass",
        "nickname": "joe_cool_123",
    }
    response = await async_client.post("/register/", json=user_data_too_short_password)
    assert response.status_code == 422

@pytest.mark.asyncio
async def test_create_user_invalid_length_password(async_client, admin_token):
    user_data_too_short_password = {
        "nickname": "joe_cool_123",
        "email": "test@example.com",
        "password": "pass",
    }
    headers = {"Authorization": f"Bearer {admin_token}"}
    response = await async_client.post("/users/", json=user_data_too_short_password, headers=headers)
    assert response.status_code == 422

import pytest
from app.services.jwt_service import decode_token
from urllib.parse import urlencode

@pytest.mark.asyncio
async def test_login_success(async_client, verified_user):
    # Attempt to login with the test user
    form_data = {
        "username": verified_user.email,
        "password": "MySuperPassword$1234"
    }
    response = await async_client.post("/login/", data=urlencode(form_data), headers={"Content-Type": "application/x-www-form-urlencoded"})
    
    # Check for successful login response
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"

    # Use the decode_token method from jwt_service to decode the JWT
    decoded_token = decode_token(data["access_token"])
    assert decoded_token is not None, "Failed to decode token"
    assert decoded_token["role"] == "AUTHENTICATED", "The user role should be AUTHENTICATED"

@pytest.mark.asyncio
async def test_login_user_not_found(async_client):
    form_data = {
        "username": "nonexistentuser@here.edu",
        "password": "DoesNotMatter123!"
    }
    response = await async_client.post("/login/", data=urlencode(form_data), headers={"Content-Type": "application/x-www-form-urlencoded"})
    assert response.status_code == 401
    assert "Incorrect email or password." in response.json().get("detail", "")

@pytest.mark.asyncio
async def test_login_incorrect_password(async_client, verified_user):
    form_data = {
        "username": verified_user.email,
        "password": "IncorrectPassword123!"
    }
    response = await async_client.post("/login/", data=urlencode(form_data), headers={"Content-Type": "application/x-www-form-urlencoded"})
    assert response.status_code == 401
    assert "Incorrect email or password." in response.json().get("detail", "")

@pytest.mark.asyncio
async def test_login_unverified_user(async_client, unverified_user):
    form_data = {
        "username": unverified_user.email,
        "password": "MySuperPassword$1234"
    }
    response = await async_client.post("/login/", data=urlencode(form_data), headers={"Content-Type": "application/x-www-form-urlencoded"})
    assert response.status_code == 401

@pytest.mark.asyncio
async def test_login_locked_user(async_client, locked_user):
    form_data = {
        "username": locked_user.email,
        "password": "MySuperPassword$1234"
    }
    response = await async_client.post("/login/", data=urlencode(form_data), headers={"Content-Type": "application/x-www-form-urlencoded"})
    assert response.status_code == 400
    assert "Account locked due to too many failed login attempts." in response.json().get("detail", "")
@pytest.mark.asyncio
async def test_delete_user_does_not_exist(async_client, admin_token):
    non_existent_user_id = "00000000-0000-0000-0000-000000000000"  # Valid UUID format
    headers = {"Authorization": f"Bearer {admin_token}"}
    delete_response = await async_client.delete(f"/users/{non_existent_user_id}", headers=headers)
    assert delete_response.status_code == 404

@pytest.mark.asyncio
async def test_update_user_github(async_client, admin_user, admin_token):
    updated_data = {"github_profile_url": "http://www.github.com/kaw393939"}
    headers = {"Authorization": f"Bearer {admin_token}"}
    response = await async_client.put(f"/users/{admin_user.id}", json=updated_data, headers=headers)
    assert response.status_code == 200
    assert response.json()["github_profile_url"] == updated_data["github_profile_url"]

@pytest.mark.asyncio
async def test_update_user_linkedin(async_client, admin_user, admin_token):
    updated_data = {"linkedin_profile_url": "http://www.linkedin.com/kaw393939"}
    headers = {"Authorization": f"Bearer {admin_token}"}
    response = await async_client.put(f"/users/{admin_user.id}", json=updated_data, headers=headers)
    assert response.status_code == 200
    assert response.json()["linkedin_profile_url"] == updated_data["linkedin_profile_url"]

@pytest.mark.asyncio
async def test_list_users_as_admin(async_client, admin_token):
    response = await async_client.get(
        "/users/",
        headers={"Authorization": f"Bearer {admin_token}"}
    )
    assert response.status_code == 200
    assert 'items' in response.json()

@pytest.mark.asyncio
async def test_list_users_as_manager(async_client, manager_token):
    response = await async_client.get(
        "/users/",
        headers={"Authorization": f"Bearer {manager_token}"}
    )
    assert response.status_code == 200

@pytest.mark.asyncio
async def test_list_users_unauthorized(async_client, user_token):
    response = await async_client.get(
        "/users/",
        headers={"Authorization": f"Bearer {user_token}"}
    )
    assert response.status_code == 403  # Forbidden, as expected for regular user
