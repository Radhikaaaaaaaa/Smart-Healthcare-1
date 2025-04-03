from flask import Flask, request, render_template
import sqlite3
import smtplib

app = Flask(__name__)

THRESHOLDS = {"acetone": 1000, "ethanol": 1500, "ammonia": 1300}
EMAIL_ALERTS = "sejalpatil003@gmail.com"

# Initialize Database
def init_db():
    conn = sqlite3.connect('health_data.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS sensor_data (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            acetone REAL,
            ethanol REAL,
            ammonia REAL,
            alert TEXT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.commit()
    conn.close()

init_db()

@app.route("/")
def index():
    conn = sqlite3.connect("health_data.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM sensor_data ORDER BY timestamp DESC LIMIT 10")
    data = cursor.fetchall()
    conn.close()
    return render_template("index.html", data=data)

@app.route("/update", methods=["POST"])
def update():
    try:
        acetone = float(request.form.get("acetone", 0))
        ethanol = float(request.form.get("ethanol", 0))
        ammonia = float(request.form.get("ammonia", 0))
        alert = "Normal"

        if acetone > THRESHOLDS["acetone"] or ethanol > THRESHOLDS["ethanol"] or ammonia > THRESHOLDS["ammonia"]:
            alert = "Alert! High VOC Levels"
            send_email_alert(acetone, ethanol, ammonia)
        
        conn = sqlite3.connect("health_data.db")
        cursor = conn.cursor()
        cursor.execute("INSERT INTO sensor_data (acetone, ethanol, ammonia, alert) VALUES (?, ?, ?, ?)", (acetone, ethanol, ammonia, alert))
        conn.commit()
        conn.close()

        print(f"Received Data - Acetone: {acetone} ppm, Ethanol: {ethanol} ppm, Ammonia: {ammonia} ppm")

        return "Data Received", 200
    except Exception as e:
        print(f"Error: {e}")
        return "Error Processing Data", 500

def send_email_alert(acetone, ethanol, ammonia):
    subject = "Health Alert: High VOC Levels"
    body = f"Acetone: {acetone} ppm, Ethanol: {ethanol} ppm, Ammonia: {ammonia} ppm\nPlease consult a doctor if needed."
    email_text = f"Subject: {subject}\n\n{body}"
    
    with smtplib.SMTP("smtp.gmail.com", 587) as server:
        server.starttls()
        server.login("your_email@gmail.com", "your_password")
        server.sendmail("your_email@gmail.com", EMAIL_ALERTS, email_text)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
