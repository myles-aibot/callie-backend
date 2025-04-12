from flask import Flask, Response
from twilio.twiml.voice_response import VoiceResponse

app = Flask(__name__)

@app.route("/voice", methods=["POST"])
def voice():
    response = VoiceResponse()
    response.start().stream(url="wss://callie-stream.onrender.com/media")
    response.say("You're now speaking with Callie. Please begin.", voice="Polly.Joanna")
    return Response(str(response), mimetype="text/xml")

@app.route("/")
def home():
    return "Callie webhook is live"
