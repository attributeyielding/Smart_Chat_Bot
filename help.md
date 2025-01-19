# Bloom Chatbot with Flask

This project implements a chatbot using the **Bloom-1.7B** language
model from Hugging Face\'s `transformers` library. The chatbot is served
via a **Flask** web application, allowing users to interact with the
model through a simple API endpoint. The application supports CORS
(Cross-Origin Resource Sharing) for seamless integration with frontend
applications.


## Features

-   **Bloom-1.7B Model**: Utilizes the powerful Bloom-1.7B causal
    language model for generating human-like responses.
-   **Flask API**: Provides a RESTful API endpoint (`/chat`) for sending
    user messages and receiving model-generated responses.
-   **CORS Support**: Enables cross-origin requests from a specified
    frontend origin (e.g., `http://127.0.0.1:5500`).
-   **Health Check**: Includes a health check endpoint (`/`) to verify
    that the chatbot is running.
-   **Error Handling**: Robust error handling for invalid requests,
    model loading issues, and inference errors.
-   **Device Optimization**: Automatically uses GPU if available,
    otherwise falls back to CPU.

## Prerequisites

Before running the application, ensure you have the following installed:

-   Python 3.8 or higher
-   `pip` (Python package manager)

## Installation

1.  **Clone the repository**:

        git clone https://github.com/attributeyielding/Smart_Chat_Bot.git
        cd bloom-chatbot

2.  **Create a virtual environment** (optional but recommended):

        python -m venv venv
        source venv/bin/activate  # On Windows, use `venv\Scripts\activate`

3.  **Install dependencies**:

        pip install -r requirements.txt

    The `requirements.txt` file should include:

        flask
        torch
        transformers
        flask-cors

4.  **Download the Bloom-1.7B model**:
    -   The application will automatically download the model if it is
        not already present in the `data/bloom-1b7` directory.
    -   Ensure you have sufficient disk space (approximately 5-10 GB)
        for the model.

## Running the Application

1.  **Start the Flask server**:

        python app.py

2.  The application will run on `http://0.0.0.0:5000` by default. You
    can access the health check endpoint at:

        http://127.0.0.1:5000/

3.  **Interact with the chatbot**:

    Send a POST request to the `/chat` endpoint with a JSON payload
    containing the user\'s message:

        {
            "message": "Hello, how are you?"
        }

    Example using `curl`:

        curl -X POST http://127.0.0.1:5000/chat \
        -H "Content-Type: application/json" \
        -d '{"message": "Hello, how are you?"}'

    The response will be in JSON format:

        {
            "response": "I am doing well, thank you! How can I assist you today?"
        }

## Configuration

-   **CORS Origins**: By default, the application allows requests from
    `http://127.0.0.1:5500`. To modify this, update the `origins`
    parameter in the `CORS` initialization:

        CORS(app, origins="http://your-frontend-url.com", supports_credentials=True)

-   **Model Path**: The model is saved and loaded from the
    `data/bloom-1b7` directory. You can change this by modifying the
    `MODEL_PATH` variable in the code.

-   **Device**: The application automatically detects and uses a GPU if
    available. To force CPU usage, modify the `device` variable:

        device = torch.device("cpu")

## API Endpoints

### 1. Health Check

-   **Endpoint**: `GET /`
-   **Description**: Verifies that the chatbot is running.
-   **Response**: Plain text string: `"Chatbot is running!"`

### 2. Chat

-   **Endpoint**: `POST /chat`

-   **Description**: Accepts a user message and returns a
    model-generated response.

-   **Request Body**:

        {
            "message": "Your input message here"
        }

-   **Response**:

        {
            "response": "Model-generated response here"
        }

-   **Error Responses**:
    -   `400 Bad Request`: If no message is provided.
    -   `415 Unsupported Media Type`: If the `Content-Type` header is
        not `application/json`.
    -   `500 Internal Server Error`: If an error occurs during model
        inference.

## Troubleshooting

-   **Model Download Issues**: Ensure you have a stable internet
    connection and sufficient disk space. If the download fails,
    manually download the model using:

        tokenizer = BloomTokenizerFast.from_pretrained("bigscience/bloom-1b7")
        model = BloomForCausalLM.from_pretrained("bigscience/bloom-1b7")
        tokenizer.save_pretrained("data/bloom-1b7")
        model.save_pretrained("data/bloom-1b7")

-   **GPU Not Detected**: If you have a GPU but it is not being used,
    ensure that `torch` is installed with CUDA support:

        pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118

-   **CORS Errors**: Ensure the frontend URL is correctly specified in
    the `CORS` configuration.



## License

This project is licensed under the MIT License.


## Acknowledgments

-   [Hugging Face](https://huggingface.co/) for the `transformers`
    library and the Bloom model.
-   [Flask](https://flask.palletsprojects.com/) for the web framework.
-   [PyTorch](https://pytorch.org/) for the deep learning framework.

