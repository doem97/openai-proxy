#!/bin/bash

USER_ID="USER_ID"
PROXY_URL="PROXY_URL"

curl ${PROXY_URL}/openai \
-H "Content-Type: application/json" \
-H "Authorization: CloseAIUser ${USER_ID}" \
-d '{
    "model": "gpt-4",
    "messages": [{"role": "user", "content": "Hello world!"}]
  }'
