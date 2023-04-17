import os
import requests
from flask import Flask, request, Response
import time
import re

app = Flask(__name__)

OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")
#  = os.environ.get("OPENAI_API_KEY")
OPENAI_API_URL = "https://api.openai.com/v1/chat/completions"

# user_usage = {}


@app.route("/log", methods=["GET"])
def get_log():
    total_prompt_tokens = 0
    total_completion_tokens = 0

    with open("/tmp/usage_logs.txt", "r") as log_file:
        lines = log_file.readlines()

    for line in lines:
        prompt_tokens_match = re.search(r"Prompt Tokens: (\d+)", line)
        completion_tokens_match = re.search(r"Completion Tokens: (\d+)", line)

        if prompt_tokens_match:
            total_prompt_tokens += int(prompt_tokens_match.group(1))
        if completion_tokens_match:
            total_completion_tokens += int(completion_tokens_match.group(1))

    summary = f"Total Prompt Token Used: {total_prompt_tokens}<br>Total Completion Token Used: {total_completion_tokens}<br>Total Price: ${total_prompt_tokens/1000 * 0.06 + total_completion_tokens/1000 * 0.12}<br>"
    log_content = summary + "<br>".join(lines)

    return log_content


@app.route("/openai", methods=["POST"])
def openai_proxy():
    # Track token usage and any other required logic
    auth_header = request.headers.get("Authorization")
    user_name = auth_header.split(" ")[-1] if auth_header else None

    # Forward the request to OpenAI's API
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {OPENAI_API_KEY}",
    }
    data = request.get_json()

    if user_name:
        response = requests.post(OPENAI_API_URL, headers=headers, json=data)
        if response.status_code == 200:
            json_response = response.json()
            usage = json_response.get("usage", {})
            prompt_tokens = usage.get("prompt_tokens", 0)
            completion_tokens = usage.get("completion_tokens", 0)

            log_entry = f"{time.strftime('%Y-%m-%d %H:%M:%S')} | User: {user_name} | Prompt Tokens: {prompt_tokens} | Completion Tokens: {completion_tokens}\n"

            with open("/tmp/usage_logs.txt", "a") as log_file:
                log_file.write(log_entry)

            # Return the response from OpenAI's API
            return response.json()
        else:
            return response.text, response.status_code
    else:
        return "Unauthorized", 401

    # # Return the response from OpenAI's API

    # response_json = response.json()

    # # Update user usage
    # if user_name not in user_usage:
    #     user_usage[user_name] = {}
    # user_usage[user_name]["total_tokens"] += response_json["usage"]["total_tokens"]
    # user_usage[user_name]["prompts"] += response_json["usage"]["total_tokens"]
    # user_usage[user_name]["completions"] += response_json["usage"]["total_tokens"]

    # # Return the response from OpenAI's API
    # return response_json


def main(request):
    def start_response(status, headers):
        response = Response(status=status)
        for header_name, header_value in headers:
            response.headers[header_name] = header_value
        return response

    return app.__call__(request.environ, start_response)
