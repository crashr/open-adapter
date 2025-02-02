from flask import Flask, request, jsonify
import requests
import time
import argparse
import yaml
import os
import uuid

app = Flask(__name__)


backend_url = ""
chat_id = ""  # "00000000-0000-0000-0000-000000000000"


def load_config(config_path):
    if os.path.exists(config_path):
        with open(config_path, "r") as file:
            return yaml.safe_load(file)
    return {}


@app.route("/")
def home():
    return "Open-Adapter is running!"


@app.route("/v1/chat/completions", methods=["POST"])
def chat_completions():
    print(request.json)

    user_message = request.json.get("messages", [{}])[-1].get("content", "")

    # new_data = {"question": user_message}
    new_data = {
        "question": user_message,
        "chatId": chat_id,
    }

    print("new_data")
    print(new_data)

    response = requests.post(backend_url, json=new_data)

    print(response)
    print(response.text)
    response_json = response.json()

    print("response_json")
    print(response_json)

    formatted_response = {
        "id": response_json.get("chat_id", ""),
        "object": "chat.completion",
        "created": int(time.time()),
        "model": "open-adapter",
        "usage": {
            "prompt_tokens": 13,  # TODO
            "completion_tokens": 7,  # TODO
            "total_tokens": 20,  # TODO
            "completion_tokens_details": {
                "reasoning_tokens": 0,  # TODO
                "accepted_prediction_tokens": 0,  # TODO
                "rejected_prediction_tokens": 0,  # TODO
            },
        },
        "choices": [
            {
                "message": {
                    "role": "assistant",
                    "content": response_json.get("text", ""),
                },
                "logprobs": None,
                "finish_reason": "stop",
                "index": 0,
            }
        ],
    }

    print(formatted_response)
    return jsonify(formatted_response)


@app.route("/v1/embeddings", methods=["POST"])
def embeddings():
    return forward_request(request, "v1/embeddings")


@app.route("/v1/models", methods=["GET"])
def list_models():
    return jsonify(
        {
            "object": "list",
            "data": [
                {
                    "id": "open-adapter",
                    "object": "model",
                    "created": 1686666666,
                    "owned_by": "organization-owner",
                },
            ],
            "object": "list",
        }
    )


@app.route("/v1/set_chat_id", methods=["POST"])
def set_chat_id():
    global chat_id
    new_chat_id = request.json.get("chat_id")
    if new_chat_id:
        chat_id = new_chat_id
        return (
            jsonify({"message": "Chat ID updated successfully", "chat_id": chat_id}),
            200,
        )
    else:
        return jsonify({"error": "No new chat_id provided"}), 400


@app.route("/v1/set_random_chat_id", methods=["POST"])
def set_random_chat_id():
    global chat_id
    new_chat_id = str(uuid.uuid4())
    chat_id = new_chat_id
    return (
        jsonify({"message": "Chat ID updated successfully", "chat_id": chat_id}),
        200,
    )


@app.errorhandler(404)
def page_not_found(e):
    return jsonify({"error": "Endpoint not found"}), 404


@app.errorhandler(500)
def internal_server_error(e):
    return jsonify({"error": "Internal server error"}), 500


def main():
    global backend_url
    global chat_id

    parser = argparse.ArgumentParser(description="Set backend_url and chatId.")
    parser.add_argument(
        "--config",
        type=str,
        default="config.yaml",
        help="Path to the configuration file.",
    )
    parser.add_argument("--host", type=str, help="Host.")
    parser.add_argument("--port", type=str, help="Port.")
    parser.add_argument("--backend_url", type=str, help="Backend URL.")
    parser.add_argument("--chat_id", type=str, help="Chat ID.")

    args = parser.parse_args()

    config = load_config(args.config)

    backend_url = args.backend_url if args.backend_url else config.get("backend_url")
    chat_id = args.chat_id if args.chat_id else config.get("chat_id")
    host = args.host if args.host else config.get("host")
    port = args.port if args.port else config.get("port")

    app.run(debug=True, host=host, port=port)


if __name__ == "__main__":
    main()
