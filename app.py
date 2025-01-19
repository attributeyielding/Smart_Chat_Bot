from flask import Flask, request, jsonify
import os
import torch
from transformers import BloomForCausalLM, BloomTokenizerFast
import logging
from flask_cors import CORS  # Import the CORS library

# Initialize Flask app
app = Flask(__name__)


# Enable CORS for all routes
CORS(app, origins="http://127.0.0.1:5500", supports_credentials=True)

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Define paths
MODEL_NAME = "bigscience/bloom-1b7"
MODEL_PATH = os.path.join("data", "bloom-1b7")

# Check if the model exists, otherwise download it
if not os.path.exists(MODEL_PATH):
    logger.info(f"Downloading {MODEL_NAME} model...")
    os.makedirs(MODEL_PATH, exist_ok=True)
    try:
        tokenizer = BloomTokenizerFast.from_pretrained(MODEL_NAME)
        model = BloomForCausalLM.from_pretrained(MODEL_NAME)
        tokenizer.save_pretrained(MODEL_PATH)
        model.save_pretrained(MODEL_PATH)
    except Exception as e:
        logger.error(f"Failed to download or save the model: {e}")
        raise
else:
    logger.info("Loading Bloom-1b7 model from local storage...")
    try:
        tokenizer = BloomTokenizerFast.from_pretrained(MODEL_PATH)
        model = BloomForCausalLM.from_pretrained(MODEL_PATH)
    except Exception as e:
        logger.error(f"Failed to load the model: {e}")
        raise

# Set device (GPU if available, otherwise CPU)
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model.to(device)

@app.route("/chat", methods=["POST"])
def chat():
    if request.headers.get("Content-Type") != "application/json":
        return jsonify({"error": "Unsupported Media Type: Content-Type must be application/json"}), 415

    data = request.json
    if not data:
        return jsonify({"error": "No JSON data provided"}), 400

    user_input = data.get("message", "")
    if not user_input:
        return jsonify({"error": "No message provided"}), 400

    try:
        inputs = tokenizer.encode(user_input, return_tensors="pt").to(device)
        outputs = model.generate(inputs, max_length=50, num_return_sequences=1, no_repeat_ngram_size=5)
        response = tokenizer.decode(outputs[0], skip_special_tokens=True)
        return jsonify({"response": response})
    except Exception as e:
        logger.error(f"Error during model inference: {e}")
        return jsonify({"error": "An error occurred while generating the response"}), 500

# Health check endpoint
@app.route("/", methods=["GET"])
def health_check():
    return "Chatbot is running!"

# Run the Flask app
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)