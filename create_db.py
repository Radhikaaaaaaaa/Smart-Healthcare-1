import sqlite3

# Connect to SQLite database (or create it if it doesn't exist)
conn = sqlite3.connect("health_data.db")
cursor = conn.cursor()

# Create a table for sensor data
cursor.execute("""
CREATE TABLE IF NOT EXISTS sensor_readings (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
    acetone REAL,
    ethanol REAL,
    ammonia REAL
)
""")

print("Database and table created successfully.")

# Commit changes and close connection
conn.commit()
conn.close()
