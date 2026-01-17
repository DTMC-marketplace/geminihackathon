"""
FakeAI Sentiment Analysis API

A simple Flask API for sentiment analysis.
"""

from flask import Flask, request, jsonify
from model import SentimentModel
from utils import preprocess_text

app = Flask(__name__)
model = SentimentModel()

@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint."""
    return jsonify({"status": "healthy"})

@app.route('/analyze', methods=['POST'])
def analyze_sentiment():
    """
    Analyze the sentiment of input text.
    
    Request Body:
        {"text": "Your text here"}
    
    Response:
        {"sentiment": "positive", "confidence": 0.95}
    """
    data = request.get_json()
    if not data or 'text' not in data:
        return jsonify({"error": "Missing 'text' field"}), 400
    
    clean_text = preprocess_text(data['text'])
    sentiment, confidence = model.predict(clean_text)
    
    return jsonify({
        "sentiment": sentiment,
        "confidence": round(confidence, 2)
    })

if __name__ == '__main__':
    import os
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
