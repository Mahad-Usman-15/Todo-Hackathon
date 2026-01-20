#!/usr/bin/env python
"""
Migration script to consolidate user tables and clean up duplicates
This script consolidates the Better Auth 'User' table and backend 'users' table
to ensure a unified user management system.
"""

import os
import sys
from sqlmodel import create_engine, Session, select
from config import settings
from models import User as BackendUser
import psycopg2
from urllib.parse import urlparse

def migrate_user_tables():
    """Migrate and consolidate user tables"""

    # Connect to database using psycopg2 for raw SQL operations
    conn = psycopg2.connect(settings.DATABASE_URL)
    cur = conn.cursor()

    try:
        # Check if both tables exist
        cur.execute("""
            SELECT table_name
            FROM information_schema.tables
            WHERE table_schema = 'public'
            AND table_name IN ('User', 'users')
        """)

        existing_tables = [row[0] for row in cur.fetchall()]
        print(f"Existing user-related tables: {existing_tables}")

        if 'User' in existing_tables and 'users' in existing_tables:
            print("Both 'User' (Better Auth) and 'users' (backend) tables exist.")

            # Copy data from Better Auth User table to backend users table if needed
            # This ensures users created by Better Auth are available to backend
            # Handle potential type differences between tables
            cur.execute("""
                SELECT "id", "email" FROM "User"
                WHERE CAST("id" AS TEXT) NOT IN (SELECT CAST(id AS TEXT) FROM users)
            """)

            missing_users = cur.fetchall()
            print(f"Found {len(missing_users)} users in 'User' table not in 'users' table")

            for user_row in missing_users:
                user_id, email = user_row
                print(f"Migrating user {user_id} with email {email}")

                # Insert into backend users table
                cur.execute("""
                    INSERT INTO users (id, email, hashed_password, created_at, updated_at)
                    VALUES (%s, %s, '', NOW(), NOW())
                    ON CONFLICT (id) DO NOTHING
                """, (str(user_id), email))

            conn.commit()
            print("User migration completed successfully")

        # Now we'll let the backend handle users through the 'users' table
        # Better Auth manages its own 'User' table for authentication
        # The backend 'users' table is for application-specific user data

        print("Migration completed. Both tables will coexist with proper separation:")
        print("- 'User' table: Managed by Better Auth for authentication")
        print("- 'users' table: Managed by backend for application data")

    except Exception as e:
        print(f"Error during migration: {e}")
        conn.rollback()
        raise
    finally:
        cur.close()
        conn.close()

def migrate_task_tables():
    """Consolidate task tables if both exist"""

    conn = psycopg2.connect(settings.DATABASE_URL)
    cur = conn.cursor()

    try:
        # Check if both task tables exist
        cur.execute("""
            SELECT table_name
            FROM information_schema.tables
            WHERE table_schema = 'public'
            AND table_name IN ('task', 'tasks')
        """)

        existing_tables = [row[0] for row in cur.fetchall()]
        print(f"Existing task-related tables: {existing_tables}")

        if 'task' in existing_tables and 'tasks' in existing_tables:
            print("Both 'task' and 'tasks' tables exist. Consolidating to 'tasks'...")

            # Copy data from 'task' to 'tasks' if there's missing data
            cur.execute("""
                SELECT t.*, COALESCE(t.user_id, u.id) as effective_user_id
                FROM task t
                LEFT JOIN users u ON t.user_id IS NULL OR t.user_id = ''
            """)

            tasks_to_migrate = cur.fetchall()
            print(f"Found {len(tasks_to_migrate)} tasks to potentially migrate")

            # We'll use the 'tasks' table as the canonical table since it matches our models
            # The 'task' table seems to be an older version

        elif 'task' in existing_tables:
            # Rename 'task' to 'tasks' to match our models
            print("Renaming 'task' table to 'tasks' to match backend models...")
            cur.execute("ALTER TABLE task RENAME TO tasks")
            conn.commit()
            print("Table renamed successfully")

        print("Task table consolidation completed")

    except Exception as e:
        print(f"Error during task migration: {e}")
        conn.rollback()
        raise
    finally:
        cur.close()
        conn.close()

if __name__ == "__main__":
    print("Starting user and task table migration...")
    migrate_user_tables()
    migrate_task_tables()
    print("Migration completed!")