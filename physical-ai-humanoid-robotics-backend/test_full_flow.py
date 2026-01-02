#!/usr/bin/env python3
"""Test script to debug the full auth and chat flow"""

import asyncio
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__)))

from fastapi.testclient import TestClient
from src.main import app

def test_full_flow():
    client = TestClient(app)

    print("Testing registration...")
    # Test registration
    response = client.post(
        "/api/auth/register",
        json={
            "email": "fullflow@example.com",
            "password": "password123",
            "name": "Full Flow User"
        },
        headers={"Content-Type": "application/json"}
    )

    print(f"Registration Status Code: {response.status_code}")
    if response.status_code == 200:
        user_data = response.json()
        print(f"Registration successful: {user_data}")
        user_id = user_data['id']
    else:
        print(f"Registration failed: {response.text}")
        return

    print("\nTesting login...")
    # Test login
    response = client.post(
        "/api/auth/login",
        json={
            "email": "fullflow@example.com",
            "password": "password123"
        },
        headers={"Content-Type": "application/json"}
    )

    print(f"Login Status Code: {response.status_code}")
    if response.status_code == 200:
        login_data = response.json()
        print(f"Login successful: {login_data}")
        access_token = login_data['access_token']
    else:
        print(f"Login failed: {response.text}")
        return

    print("\nTesting profile access...")
    # Test profile access with token
    response = client.get(
        "/api/auth/profile",
        headers={"Authorization": f"Bearer {access_token}"}
    )

    print(f"Profile Status Code: {response.status_code}")
    if response.status_code == 200:
        profile_data = response.json()
        print(f"Profile access successful: {profile_data}")
    else:
        print(f"Profile access failed: {response.text}")

    print("\nTesting chat session creation...")
    # Test chat session creation
    response = client.post(
        "/api/chatbot/sessions",
        json={
            "title": "Test Session",
            "context": {"initial": "Test context"}
        },
        headers={"Authorization": f"Bearer {access_token}", "Content-Type": "application/json"}
    )

    print(f"Chat session Status Code: {response.status_code}")
    if response.status_code == 200:
        session_data = response.json()
        print(f"Chat session created: {session_data}")
        session_id = session_data['id']
    else:
        print(f"Chat session failed: {response.text}")

    print("\nTesting chat query...")
    # Test chat query
    if 'session_id' in locals():
        response = client.post(
            f"/api/chatbot/sessions/{session_id}/query",
            json={
                "message": "Hello, what is robotics?"
            },
            headers={"Authorization": f"Bearer {access_token}", "Content-Type": "application/json"}
        )

        print(f"Chat query Status Code: {response.status_code}")
        if response.status_code == 200:
            chat_response = response.json()
            print(f"Chat response: {chat_response}")
        else:
            print(f"Chat query failed: {response.text}")

if __name__ == "__main__":
    test_full_flow()