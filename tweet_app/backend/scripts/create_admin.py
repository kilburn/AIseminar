#!/usr/bin/env python3
"""
Script to create an admin user for development
"""

import sys
import os
from getpass import getpass

# Add the parent directory to the path
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from app.core.database import SessionLocal, init_db
from app.core.security import get_password_hash
from app.models.user import User


def create_admin_user():
    """Create an admin user"""
    db = SessionLocal()

    try:
        # Check if admin user already exists
        existing_admin = db.query(User).filter(User.email == "admin@tweeteval.dev").first()
        if existing_admin:
            print("Admin user already exists!")
            return

        # Get admin user details
        print("Creating admin user for TweetEval NLP Platform")
        email = input("Enter admin email (default: admin@tweeteval.dev): ").strip()
        if not email:
            email = "admin@tweeteval.dev"

        username = input("Enter admin username (default: admin): ").strip()
        if not username:
            username = "admin"

        full_name = input("Enter admin full name (default: Admin User): ").strip()
        if not full_name:
            full_name = "Admin User"

        organization = input("Enter organization (optional): ").strip()

        password = getpass("Enter admin password: ")
        if not password:
            print("Password cannot be empty!")
            return

        confirm_password = getpass("Confirm password: ")
        if password != confirm_password:
            print("Passwords do not match!")
            return

        # Create admin user
        admin_user = User(
            username=username,
            email=email,
            full_name=full_name,
            organization=organization,
            password_hash=get_password_hash(password),
            is_active=True,
            is_verified=True
        )

        db.add(admin_user)
        db.commit()

        print(f"\nAdmin user created successfully!")
        print(f"Email: {email}")
        print(f"Username: {username}")
        print(f"Full Name: {full_name}")
        print(f"Organization: {organization or 'Not specified'}")

    except Exception as e:
        print(f"Error creating admin user: {e}")
        db.rollback()
    finally:
        db.close()


if __name__ == "__main__":
    # Initialize database
    init_db()

    # Create admin user
    create_admin_user()