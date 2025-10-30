"""
Quick Start Script for Unified Resume Platform
This script checks dependencies and starts the application
"""
import sys
import os

def check_mysql_connector():
    """Check if mysql-connector-python is installed"""
    try:
        import mysql.connector
        print("✓ MySQL connector installed")
        return True
    except ImportError:
        print("✗ MySQL connector not installed")
        print("\nInstalling mysql-connector-python...")
        os.system("python -m pip install mysql-connector-python")
        return True

def check_database_config():
    """Check if database is configured"""
    try:
        from unified_resume_platform.backend.db_config import DB_CONFIG
        if DB_CONFIG['password'] == 'your_password':
            print("\n" + "="*60)
            print("⚠ DATABASE NOT CONFIGURED")
            print("="*60)
            print("\nTo enable database:")
            print("1. Update password in: unified_resume_platform/backend/db_config.py")
            print("2. Run: python init_database.py")
            print("\nOr continue without database (data won't be saved)")
            print("="*60 + "\n")
            
            response = input("Continue without database? (y/n): ").lower()
            if response != 'y':
                print("\nPlease configure database first. See DATABASE_SETUP.txt")
                return False
        else:
            print("✓ Database configured")
    except Exception as e:
        print(f"⚠ Warning: {e}")
    return True

def start_app():
    """Start the Flask application"""
    print("\n" + "="*60)
    print("Starting Unified Resume Platform")
    print("="*60)
    print("\nServer will start at: http://localhost:5000")
    print("Press CTRL+C to stop\n")
    print("="*60 + "\n")
    
    try:
        from app import app
        app.run(debug=True, host='0.0.0.0', port=5000)
    except KeyboardInterrupt:
        print("\n\nServer stopped by user")
    except Exception as e:
        print(f"\n✗ Error starting application: {e}")
        return False
    return True

if __name__ == '__main__':
    print("="*60)
    print("Unified Resume Platform - Quick Start")
    print("="*60 + "\n")
    
    if check_mysql_connector():
        if check_database_config():
            start_app()
        else:
            print("\nSetup cancelled. Please configure database first.")
    else:
        print("\n✗ Failed to install dependencies")
