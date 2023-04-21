# OpenAI-Proxy

Distribute API access to your team members or applications while keep your api key protected, and control the usage for each access end.

**WARNING!!!** Although not explicitly mentioned in [OpenAI term of usage](https://openai.com/policies/terms-of-use), using this proxy to share/distribute your remaining quota to public would be considered violation to OpenAI rules, and will cause account limitation/ban. PLEASE DON'T TRY TO DO SO!!

**PLEASE only use this system to control the api access WITHIN your team.**

# Installation

This service is built on Google Cloud Functions or AWS Lambda. You can deploy it to your own cloud provider. Here is the instruction for Google Cloud Functions.

### Configure Google Cloud Functions

1. Set up a Google Cloud project if you don't already have one: https://console.cloud.google.com/
2. Enable the Cloud Functions API for your project: https://console.cloud.google.com/apis/library/cloudfunctions.googleapis.com
3. Install Google Cloud SDK on your local machine: https://cloud.google.com/sdk/docs/install
4. Authenticate your account by running `gcloud auth login` in the terminal.

### Deploy the Service

1. Clone this repository.
```bash
git clone https://github.com/doem97/openai-proxy.git
cd openai-proxy
```

2. Deploy the service to Google Cloud Functions. Please first edit `./deploy.sh` and modify USER_ID and OPENAI_API_KEY, and then
```bash
bash ./deploy.sh
```
You will got output in the terminal like this:
```bash
...
url: https://ip-address-of-service.cloudfunctions.net/${USER_ID}
...
```
Please copy-paste this url for later use:
```bash
export PROXY_URL="the_url_in_output"
```

### Make Request via Proxy
Just like regular calling OpenAI API, but you need to change the API addr as proxy addr, and change `Authorization: UserName` field.
I gave an example in `request.sh`. Like this:
```bash
curl ${PROXY_URL}/openai \
-H "Content-Type: application/json" \
-H "Authorization: UserName ${USER_ID}" \
-d '{
    "model": "gpt-4",
    "messages": [{"role": "user", "content": "Hello world!"}]
  }'
```

### Track Request Log For Each User
Open browser and navigate to `${PROXY_URL}/log`. You will see the usage of corresponding user.
