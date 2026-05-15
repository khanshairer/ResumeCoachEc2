from flask import Flask, request, jsonify, send_from_directory
import boto3

app = Flask(__name__)

# =========================
# BEDROCK CLIENT
# =========================

bedrock = boto3.client(
    "bedrock-runtime",
    region_name="us-east-1",
    aws_access_key_id="YOUR_ACCESS_KEY",
    aws_secret_access_key="YOUR_SECRET_KEY"
)

# =========================
# HOME PAGE
# =========================

@app.route("/")
def home():
    return send_from_directory(".", "index.html")

# =========================
# CHAT ENDPOINT
# =========================

@app.route("/chat", methods=["POST"])
def chat():

    try:
        data = request.get_json()

        if not data or "message" not in data:
            return jsonify({
                "error": "Message is required"
            }), 400

        user_input = data["message"]

        prompt = f"""
You are a professional AI Resume Coach.

Help users improve:
- Resume quality
- Technical resume writing
- Software engineering resumes
- ATS optimization
- Interview preparation
- Career advice

User Question:
{user_input}
"""

        response = bedrock.converse(
            modelId="amazon.nova-micro-v1:0",

            messages=[
                {
                    "role": "user",
                    "content": [
                        {
                            "text": prompt
                        }
                    ]
                }
            ],

            inferenceConfig={
                "maxTokens": 500,
                "temperature": 0.5,
                "topP": 0.9
            }
        )

        reply = response["output"]["message"]["content"][0]["text"]

        return jsonify({
            "reply": reply
        })

    except Exception as e:

        return jsonify({
            "error": str(e)
        }), 500

# =========================
# RUN APP
# =========================

if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=5000,
        debug=True
    )
