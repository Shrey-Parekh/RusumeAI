import mysql.connector
from mysql.connector import Error

def create_database():
    """Create the database if it doesn't exist"""
    try:
        connection = mysql.connector.connect(
            host='localhost',
            user='root',
            password='your_password'  # Change this to your MySQL password
        )
        
        if connection.is_connected():
            cursor = connection.cursor()
            cursor.execute("CREATE DATABASE IF NOT EXISTS unified_resume_platform")
            print("✓ Database 'unified_resume_platform' created successfully")
            cursor.close()
            connection.close()
            return True
    except Error as e:
        print(f"✗ Error creating database: {e}")
        return False

def test_connection():
    """Test database connection"""
    try:
        connection = mysql.connector.connect(
            host='localhost',
            user='root',
            password='your_password',  # Change this to your MySQL password
            database='unified_resume_platform'
        )
        
        if connection.is_connected():
            db_info = connection.get_server_info()
            print(f"✓ Successfully connected to MySQL Server version {db_info}")
            
            cursor = connection.cursor()
            cursor.execute("SELECT DATABASE();")
            record = cursor.fetchone()
            print(f"✓ Connected to database: {record[0]}")
            
            cursor.close()
            connection.close()
            return True
    except Error as e:
        print(f"✗ Error connecting to database: {e}")
        print("\nPlease make sure:")
        print("1. MySQL is running")
        print("2. Update password in unified_resume_platform/backend/db_config.py")
        print("3. Update password in this file (init_database.py)")
        return False

def run_schema():
    """Execute the database schema"""
    try:
        connection = mysql.connector.connect(
            host='localhost',
            user='root',
            password='your_password',  # Change this to your MySQL password
            database='unified_resume_platform'
        )
        
        if connection.is_connected():
            cursor = connection.cursor()
            
            # Read and execute schema file
            with open('resume.sql', 'r', encoding='utf-8') as file:
                sql_script = file.read()
                
                # Split by semicolon and execute each statement
                statements = sql_script.split(';')
                for statement in statements:
                    statement = statement.strip()
                    if statement and not statement.startswith('--'):
                        try:
                            cursor.execute(statement)
                        except Error as e:
                            if 'already exists' not in str(e).lower():
                                print(f"Warning: {e}")
            
            connection.commit()
            print("✓ Database schema executed successfully")
            
            # Verify tables
            cursor.execute("SHOW TABLES")
            tables = cursor.fetchall()
            print(f"\n✓ Created {len(tables)} tables:")
            for table in tables:
                print(f"  - {table[0]}")
            
            cursor.close()
            connection.close()
            return True
    except Error as e:
        print(f"✗ Error executing schema: {e}")
        return False
    except FileNotFoundError:
        print("✗ resume.sql file not found")
        return False

if __name__ == '__main__':
    print("="*60)
    print("Database Initialization Script")
    print("="*60)
    print("\nStep 1: Creating database...")
    if create_database():
        print("\nStep 2: Testing connection...")
        if test_connection():
            print("\nStep 3: Running schema...")
            if run_schema():
                print("\n" + "="*60)
                print("✓ Database setup completed successfully!")
                print("="*60)
                print("\nYou can now run: python app.py")
            else:
                print("\n✗ Schema execution failed")
        else:
            print("\n✗ Connection test failed")
    else:
        print("\n✗ Database creation failed")
