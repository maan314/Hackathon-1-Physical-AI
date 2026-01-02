#!/usr/bin/env python3
"""Test script to verify anonymous chatbot functionality works"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__)))

from fastapi.testclient import TestClient
from src.main import app

def test_anonymous_chatbot():
    client = TestClient(app)

    print("Testing anonymous chat session creation...")
    # Test creating a chat session without authentication
    response = client.post(
        "/api/chatbot/sessions",
        json={
            "title": "Anonymous Session",
            "context": {"topic": "robotics"}
        },
        headers={"Content-Type": "application/json"}
    )

    print(f"Session creation Status Code: {response.status_code}")
    if response.status_code == 200:
        session_data = response.json()
        print(f"Anonymous session created: {session_data}")
        session_id = session_data['id']

        print("\nTesting chat query without authentication...")
        # Test sending a query to the session
        response = client.post(
            f"/api/chatbot/sessions/{session_id}/query",
            params={"query": "What is humanoid robotics?"},
            headers={"Content-Type": "application/json"}
        )

        print(f"Query Status Code: {response.status_code}")
        if response.status_code == 200:
            query_response = response.json()
            print(f"Query response received: {query_response['message'][:100]}...")
            print("✅ Anonymous RAG chatbot functionality is working!")
        else:
            print(f"Query failed: {response.text}")
            return False
    else:
        print(f"Session creation failed: {response.text}")
        return False

    return True

if __name__ == "__main__":
    success = test_anonymous_chatbot()
    if success:
        print("\n🎉 All anonymous chatbot tests passed!")
    else:
        print("\n❌ Some tests failed.")