#!/usr/bin/env python3
""" End-to-end integration test for user authentication service
"""
import requests


BASE_URL = "http://localhost:5000"


def register_user(email: str, password: str) -> None:
    """Test user registration"""
    url = f"{BASE_URL}/users"
    data = {
        'email': email,
        'password': password
    }
    response = requests.post(url, data=data)

    assert response.status_code == 200
    assert response.json() == {"email": email, "message": "user created"}


def log_in_wrong_password(email: str, password: str) -> None:
    """Test login with wrong password"""
    url = f"{BASE_URL}/sessions"
    data = {
        'email': email,
        'password': password
    }
    response = requests.post(url, data=data)

    assert response.status_code == 401


def log_in(email: str, password: str) -> str:
    """Test successful login and return session ID"""
    url = f"{BASE_URL}/sessions"
    data = {
        'email': email,
        'password': password
    }
    response = requests.post(url, data=data)

    assert response.status_code == 200
    assert response.json() == {"email": email, "message": "logged in"}

    # Extract session ID from cookies
    return response.cookies.get('session_id')


def profile_unlogged() -> None:
    """Test accessing profile without being logged in"""
    url = f"{BASE_URL}/profile"
    response = requests.get(url)

    assert response.status_code == 403


def profile_logged(session_id: str) -> None:
    """Test accessing profile while logged in"""
    url = f"{BASE_URL}/profile"
    cookies = {
        'session_id': session_id
    }
    response = requests.get(url, cookies=cookies)

    assert response.status_code == 200
    # Just check that we get an email field in response
    assert 'email' in response.json()


def log_out(session_id: str) -> None:
    """Test logout functionality"""
    url = f"{BASE_URL}/sessions"
    cookies = {
        'session_id': session_id
    }
    response = requests.delete(url, cookies=cookies)

    assert response.status_code == 200
    # Should redirect to home page
    assert response.url == f"{BASE_URL}/"


def reset_password_token(email: str) -> str:
    """Test reset password token generation"""
    url = f"{BASE_URL}/reset_password"
    data = {
        'email': email
    }
    response = requests.post(url, data=data)

    assert response.status_code == 200
    json_data = response.json()
    assert 'email' in json_data
    assert 'reset_token' in json_data
    assert json_data['email'] == email

    return json_data['reset_token']


def update_password(email: str, reset_token: str, new_password: str) -> None:
    """Test password update using reset token"""
    url = f"{BASE_URL}/reset_password"
    data = {
        'email': email,
        'reset_token': reset_token,
        'new_password': new_password
    }
    response = requests.put(url, data=data)

    assert response.status_code == 200
    assert response.json() == {"email": email, "message": "Password updated"}


EMAIL = "guillaume@holberton.io"
PASSWD = "b4l0u"
NEW_PASSWD = "t4rt1fl3tt3"


if __name__ == "__main__":
    # Make sure the Flask app is running on localhost:5000 before executing

    register_user(EMAIL, PASSWD)
    log_in_wrong_password(EMAIL, NEW_PASSWD)
    profile_unlogged()
    session_id = log_in(EMAIL, PASSWD)
    profile_logged(session_id)
    log_out(session_id)
    reset_token = reset_password_token(EMAIL)
    update_password(EMAIL, reset_token, NEW_PASSWD)
    log_in(EMAIL, NEW_PASSWD)
