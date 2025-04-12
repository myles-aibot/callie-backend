import os
import openai
import smtplib
from flask import Flask, request, Response
from datetime import datetime
from email.mime.text import MIMEText
from twilio.twiml.voice_response import VoiceResponse, Say, Record

app = Flask(__name__)

# 🔐 OpenAI API key from environment
openai.api_key = os.environ.get("OPENAI_API_KEY")

@app.route("/voice", methods=["POST"])
def voice():
    """Initial call handler – prompt the caller and record their message"""
    response = VoiceResponse()
    response.say("Hi, this is Callie. Please tell me your name and why you're calling. I'll take a message for the business.", voice='Polly.Joanna')
    response.record(
        action="/process_recording",
        method="POST",
        maxLength=10,
        transcribe=True,
        transcribeCallback="/transcription"
    )
    return Response(str(response), mimetype="text/xml")

@app.route("/process_recording", methods=["POST"])
def process_recording():
    """TEMP FIX: Acknowledge the caller after recording ends"""
    response = VoiceResponse()
    response.say("Thanks, I’ve saved your message. Someone will get back to you shortly.", voice='Polly.Joanna')
    response.hangup()
    return Response(str(response), mimetype="text/xml")

@app.route("/transcription", methods=["POST"])
def transcription():
    """Handle the finished transcript and email it"""
    transcript = request.form.get("TranscriptionText", "")
    recording_url = request.form.get("RecordingUrl", "")
    from_number = request.form.get("From", "")

    # Format email
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

    # Send email
    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
        smtp.login(os.environ.get("EMAIL_USER"), os.environ.get("EMAIL_PASS"))
        smtp.send_message(msg)

    return Response("OK")

@app.route("/")
def home():
    return "Callie backend is live!"
