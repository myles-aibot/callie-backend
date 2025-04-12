import os
import smtplib
from flask import Flask, request, Response
from datetime import datetime
from email.mime.text import MIMEText
from twilio.twiml.voice_response import VoiceResponse

app = Flask(__name__)

@app.route("/voice", methods=["POST"])
def voice():
    response = VoiceResponse()
    response.start().stream(url="wss://callie-stream.onrender.com/media")
    response.say("You're now speaking with Callie. Please begin.", voice="Polly.Joanna")
    return Response(str(response), mimetype="text/xml")

@app.route("/transcription", methods=["POST"])
def transcription():
    try:
        transcript = request.form.get("TranscriptionText", "")
        recording_url = request.form.get("RecordingUrl", "")
        from_number = request.form.get("From", "")

        msg_text = f"""
📞 New Call Transcription — {datetime.now().strftime('%Y-%m-%d %I:%M %p')}

From: {from_number}

Transcript:
{transcript}

Recording:
{recording_url}
        """

        msg = MIMEText(msg_text)
        msg['Subject'] = "📞 New Call Received by Callie"
        msg['From'] = "callie@usecallie.com"
        msg['To'] = os.environ.get("NOTIFY_EMAIL")

        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
            smtp.login(os.environ.get("EMAIL_USER"), os.environ.get("EMAIL_PASS"))
            smtp.send_message(msg)

        print("✅ Email sent successfully.")
        return Response("OK")

    except Exception as e:
        print("🔥 ERROR in /transcription route:", e)
        return Response("FAIL", status=500)

@app.route("/")
def home():
    return "Callie backend is live!"
