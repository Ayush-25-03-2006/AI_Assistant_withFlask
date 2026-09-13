from flask import Flask, render_template, request, jsonify
import os
from groq import Groq

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

app = Flask(
    __name__,
    template_folder=os.path.join(BASE_DIR, "templates"),
    static_folder=os.path.join(BASE_DIR, "static")
)

api_key = os.getenv("GROQ_API_KEY")

if not api_key:
    raise Exception("GROQ_API_KEY is not configured in Vercel")

client = Groq(api_key=api_key)


@app.route("/")
def hello_world():
    return render_template("index.html")


@app.route("/ask", methods=["POST"])
def ask():
    question = request.form.get("question")

    if not question:
        return jsonify({"error": "Question is required"}), 400

    response = client.chat.completions.create(
        model="openai/gpt-oss-20b",
        messages=[
            {
                "role": "system",
                "content": "Act like a helpful personal assistant"
            },
            {
                "role": "user",
                "content": question
            }
        ],
        temperature=0.7,
        max_tokens=512
    )

    answer = response.choices[0].message.content

    return jsonify({"response": answer}), 200


@app.route("/summarize", methods=["POST"])
def summarize():
    email_text = request.form.get("email")

    if not email_text:
        return jsonify({"error": "Email text is required"}), 400

    prompt = f"""
    Summarize the following in 2-3 sentences:

    {email_text}
    """

    response = client.chat.completions.create(
        model="openai/gpt-oss-20b",
        messages=[
            {
                "role": "system",
                "content": "Act like an expert summarizer assistant that can be understood by all"
            },
            {
                "role": "user",
                "content": prompt
            }
        ],
        temperature=0.3,
        max_tokens=512
    )

    summary = response.choices[0].message.content

    return jsonify({"response": summary}), 200