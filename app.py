from flask import Flask, request, jsonify
from twilio.rest import Client
import socket

app = Flask(__name__)

# Twilio credentials (replace with actual values)
TWILIO_ACCOUNT_SID = 'xxxxxxxxxxxxxxxxxxxxx'
TWILIO_AUTH_TOKEN = 'xxxxxxxxxxxxxxxxxxxxx'
TWILIO_PHONE_NUMBER = 'xxxxxxxxxxx'
RECIPIENT_PHONE_NUMBER = 'xxxxxxxxxxxx'

def send_alert(message):
    try:
        client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)
        client.messages.create(
            body=message,
            from_=TWILIO_PHONE_NUMBER,
            to=RECIPIENT_PHONE_NUMBER
        )
        print("Alert sent successfully!")
    except Exception as e:
        print(f"Failed to send alert: {e}")

@app.route('/data', methods=['POST'])
def get_data():
    try:
        data = request.json
        heart_rate = data.get('heart_rate')
        spo2 = data.get('spo2')
        temperature = data.get('temperature')

        print(f"Received Data - Heart Rate: {heart_rate} bpm, SpO2: {spo2}%, Temperature: {temperature}°C")

        alert_message = ""

        # Check for heart attack threat
        if (heart_rate > 100 or heart_rate < 50) and spo2 < 90 and temperature > 38:
            alert_message = "THREAT OF HEART ATTACK! Immediate medical attention required.\n"
        else:
            # Check abnormal conditions
            if heart_rate > 100 or heart_rate < 50:
                alert_message += f"Abnormal Heart Rate: {heart_rate} bpm\n"
            if spo2 < 90:
                alert_message += f"Low SpO2: {spo2}%\n"
            if temperature > 37.5:
                alert_message += f"High Temperature: {temperature}°C\n"

            if alert_message:
                alert_message = f"ALERT: Abnormal Vitals Detected!\n{alert_message}"

        # Send alert if any condition is met
        if alert_message:
            print(alert_message)
            send_alert(alert_message)

        return jsonify({"status": "success", "data": data})

    except Exception as e:
        print(f"Error: {e}")
        return jsonify({"status": "error", "message": str(e)}), 500

if __name__ == '__main__':
    # Automatically get local IP address
    hostname = socket.gethostname()
    local_ip = socket.gethostbyname(hostname)
    print(f"Backend running on http://{local_ip}:5000")
    app.run(host='0.0.0.0', port=5000, debug=True)