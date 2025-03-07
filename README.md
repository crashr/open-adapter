# Open-Adapter

Open-Adapter equips Flowise with a rudimentary OpenAI comaptible API.


## Overview
Open-Adapter is a reverse proxy that adds an OpenAI-compatible API to Flowise. This allows you to use Flowise's capabilities through a familiar OpenAI API interface, making integration and usage more straightforward.


## Features
OpenAI-Compatible API: Enables the use of Flowise through an API that mirrors the OpenAI API.
Chat Completions: Supports sending and receiving chat messages.
Chat ID Management: Allows setting and generating chat IDs programmatically.


## Installation
### Prerequisites
Python 3.8 or higher

Flowise instance running

### Steps
Clone the Repository

```
git clone https://github.com/crashr/open-adapter.git
cd open-adapter
```
Install Dependencies (A python venv is recommended)
```
pip install -r requirements.txt
```

## Configuration

Create a configuration file (e.g., config.yaml) with the necessary settings:
```
backend_url: http://your.flowise:3000/api/v1/prediction/abcdefgh-1234-abcd-wxyz-aa1234567890
host: 0.0.0.0
port: 5000
```

Adjust the backend_url to point to your Flowise instance.


## Run the Proxy
```
python app.py --config config.yaml
```
Alternatively, you can specify all options via command-line arguments:
```
python app.py \
--host 0.0.0.0 \
--port 5000 \
--backend_url http://your.flowise:3000/api/v1/prediction/abcdefgh-1234-abcd-wxyz-aa1234567890
```


## Usage

### Chat Completions
Send a POST request to /v1/chat/completions with the following JSON payload:
```
{
  "messages": [
    {"role": "system", "content": "You are a helpful assistant."},
    {"role": "user", "content": "Hello!"}
  ]
}
```
### Set Chat ID
Send a POST request to /v1/set_chat_id with the following JSON payload:
```
{
  "chat_id": "my-custom-chat-id"
}
```
## Caveats

1. It is possiblbe to use this for example with Open-WebUI. When you create a new chat, a new chat ID will be generated and used. But if you switch back to a previous chat, the new chat ID is still valid. This is due to the architecture of how Flowise works. A solution for this doesn't exist yet.
2. No multi user.
3. No security.
4. No authentication.
