#!/usr/bin/env python3
"""Test script to debug the server registration directly"""

import asyncio
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__)))

from fastapi.testclient import TestClient
from src.main import app

def test_server_registration():
    client = TestClient(app)

    # Test registration
    response = client.post(
        "/api/auth/register",
        json={
            "email": "testserver@example.com",
            "password": "password123",
            "name": "Test Server User"
        },
        headers={"Content-Type": "application/json"}
    )

    print(f"Status Code: {response.status_code}")
    print(f"Response: {response.text}")

    if response.status_code != 200:
        print("Error occurred during registration")
        # Try to get more details if possible
        try:
            print(f"Response JSON: {response.json()}")
        except:
            print("Could not parse response as JSON")

if __name__ == "__main__":
    test_server_registration()