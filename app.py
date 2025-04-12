import os
import openai
from flask import Flask, request, Response
from twilio.twiml.voice_response import VoiceResponse, Say, Record

app = Flask(__name__)

# Set your OpenAI API Key from environment variable
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

@app.route("/transcription", methods=["POST"])
def transcription():
    """Handles the transcription once it's ready (Twilio sends it via webhook)"""
    transcript = request.form.get("TranscriptionText", "")
    recording_url = request.form.get("RecordingUrl", "")
    print("📞 Transcription received:")
    print("Text:", transcript)
    print("Recording:", recording_url)
    return Response("OK")

@app.route("/process_recording", methods=["POST"])
def process_recording():
    """Once recording is done, respond with a GPT-generated message"""
    transcript = request.form.get("TranscriptionText", "")
    if not transcript:
        return "<Response><Say>Sorry, I didn't catch that.</Say></Response>"

    # Send transcript to GPT-4o
    gpt_response = openai.ChatCompletion.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": "You are a friendly AI receptionist named Callie who takes phone messages for small businesses."},
            {"role": "user", "content": f"Caller said: {transcript}"}
        ]
    )

    reply = gpt_response.choices[0].message.content.strip()

    # Say the response back to the caller
    response = VoiceResponse()
    response.say(reply, voice='Polly.Joanna')
    return Response(str(response), mimetype="text/xml")

@app.route("/")
def home():
    return "Callie backend is live!"
