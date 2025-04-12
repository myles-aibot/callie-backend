from flask import Flask, request, Response

app = Flask(__name__)

@app.route("/voice", methods=["POST"])
def voice():
    # This is the simple TwiML response we'll start with
    twiml = """<?xml version="1.0" encoding="UTF-8"?>
    <Response>
        <Say voice="Polly.Joanna">Hi! This is Callie. We'll be ready to take your call very soon.</Say>
    </Response>"""
    return Response(twiml, mimetype="text/xml")

@app.route("/")
def home():
    return "Callie backend is live!"

if __name__ == "__main__":
    app.run(debug=True)
