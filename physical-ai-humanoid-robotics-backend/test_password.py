#!/usr/bin/env python3
"""Simple test to debug password hashing"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__)))

from src.utils.security import get_password_hash

def test_password():
    password = "password123"
    print(f"Password: {password}")
    print(f"Password length in bytes: {len(password.encode('utf-8'))}")

    try:
        hashed = get_password_hash(password)
        print(f"Password hashed successfully: {hashed[:20]}...")
    except Exception as e:
        print(f"Error hashing password: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_password()