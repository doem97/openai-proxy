#!/bin/bash

USER_ID="USER_ID"
OPENAI_API_KEY="YOUR_OPENAI_API_KEY"

gcloud functions deploy ${USER_ID} \
    --runtime python310 \
    --trigger-http \
    --allow-unauthenticated \
    --entry-point main \
    --set-env-vars OPENAI_API_KEY=${OPENAI_API_KEY} \
