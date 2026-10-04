```python
from flask import Flask, render_template, request, jsonify
from transformers import pipeline

app = Flask(__name__)

# AI sentiment model
sentiment_model = pipeline(
    "sentiment-analysis"
)


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/analyze", methods=["POST"])
def analyze():

    data = request.get_json()
    text = data.get("text", "").strip()

    if not text:
        return jsonify({
            "error": "Please enter some text"
        }), 400

    result = sentiment_model(text)[0]

    label = result["label"]
    score = round(result["score"] * 100, 2)

    if label == "POSITIVE":
        emotion = "Happy 😊"
    else:
        emotion = "Sad / Negative 😔"

    return jsonify({
        "sentiment": label,
        "confidence": score,
        "emotion": emotion,
        "word_count": len(text.split())
    })


if __name__ == "__main__":
    app.run(debug=True)
```
