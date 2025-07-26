# load_data.py - Database Setup and Data Ingestion Script (Milestone 2)

import sqlite3
from datetime import datetime
import uuid
import os
import csv

def create_database():
    """Create SQLite database and tables"""
    conn = sqlite3.connect('conversational_ai.db')
    cursor = conn.cursor()
    
    # Create users table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS user (
            id TEXT PRIMARY KEY,
            username TEXT UNIQUE NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Create conversations table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS conversation (
            id TEXT PRIMARY KEY,
            user_id TEXT NOT NULL,
            title TEXT DEFAULT 'New Conversation',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES user (id)
        )
    ''')
    
    # Create messages table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS message (
            id TEXT PRIMARY KEY,
            conversation_id TEXT NOT NULL,
            content TEXT NOT NULL,
            role TEXT NOT NULL,
            timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (conversation_id) REFERENCES conversation (id)
        )
    ''')
    
    # Create products table for e-commerce data
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS product (
            id TEXT PRIMARY KEY,
            name TEXT NOT NULL,
            description TEXT,
            price DECIMAL(10,2),
            category TEXT,
            stock_quantity INTEGER,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    conn.commit()
    conn.close()
    print("Database tables created successfully!")

def load_csv_data(csv_file_path):
    """Parse CSV files and populate the database using built-in csv module"""
    if not os.path.exists(csv_file_path):
        print(f"CSV file not found: {csv_file_path}")
        return False
    
    try:
        conn = sqlite3.connect('conversational_ai.db')
        cursor = conn.cursor()
        
        with open(csv_file_path, 'r', newline='', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            
            records_inserted = 0
            for row in reader:
                # Assuming CSV has columns: name, description, price, category, stock_quantity
                product_id = str(uuid.uuid4())
                cursor.execute('''
                    INSERT INTO product (id, name, description, price, category, stock_quantity, created_at)
                    VALUES (?, ?, ?, ?, ?, ?, ?)
                ''', (
                    product_id,
                    row.get('name', ''),
                    row.get('description', ''),
                    float(row.get('price', 0)),
                    row.get('category', ''),
                    int(row.get('stock_quantity', 0)),
                    datetime.utcnow()
                ))
                records_inserted += 1
        
        conn.commit()
        conn.close()
        print(f"Successfully inserted {records_inserted} records from CSV")
        return True
        
    except Exception as e:
        print(f"Error loading CSV data: {str(e)}")
        return False

def create_sample_data():
    """Create sample data for testing"""
    conn = sqlite3.connect('conversational_ai.db')
    cursor = conn.cursor()
    
    # Create sample user
    user_id = str(uuid.uuid4())
    cursor.execute('''
        INSERT OR IGNORE INTO user (id, username, created_at)
        VALUES (?, ?, ?)
    ''', (user_id, 'test_user', datetime.utcnow()))
    
    # Create sample products
    sample_products = [
        {
            'id': str(uuid.uuid4()),
            'name': 'Wireless Headphones',
            'description': 'High-quality wireless Bluetooth headphones',
            'price': 99.99,
            'category': 'Electronics',
            'stock_quantity': 50
        },
        {
            'id': str(uuid.uuid4()),
            'name': 'Smartphone Case',
            'description': 'Protective case for smartphones',
            'price': 19.99,
            'category': 'Accessories',
            'stock_quantity': 100
        },
        {
            'id': str(uuid.uuid4()),
            'name': 'USB Cable',
            'description': 'High-speed USB-C charging cable',
            'price': 12.99,
            'category': 'Accessories',
            'stock_quantity': 200
        }
    ]
    
    for product in sample_products:
        cursor.execute('''
            INSERT OR IGNORE INTO product 
            (id, name, description, price, category, stock_quantity, created_at)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (
            product['id'], product['name'], product['description'],
            product['price'], product['category'], product['stock_quantity'],
            datetime.utcnow()
        ))
    
    conn.commit()
    conn.close()
    print("Sample data created successfully!")

if __name__ == '__main__':
    print("Starting database setup...")
    
    # Initialize database
    create_database()
    
    # Create sample data
    create_sample_data()
    
    # Uncomment the line below if you have a CSV file to load:
    # load_csv_data('products.csv')
    
    print("Database setup completed!")