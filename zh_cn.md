# OpenAI GPT-4 API 分发工具

利用一个代理层，将你的 GPT-4 API 发放给多个人。它可以保护您的 API 密钥不泄漏，同时记录每个人的用量。

## 安装

此服务基于`Google Cloud Functions`或`AWS Lambda`构建。您可以将其部署到您自己的云提供商。以下是针对`Google Cloud Functions`的说明。

### 配置Google Cloud Functions

1. 如果您还没有，请设置一个Google Cloud项目：https://console.cloud.google.com/
2. 为您的项目启用Cloud Functions API：https://console.cloud.google.com/apis/library/cloudfunctions.googleapis.com
3. 在本地计算机上安装Google Cloud SDK：https://cloud.google.com/sdk/docs/install
4. 通过在终端运行`gcloud auth login`来验证您的帐户。

### 部署服务

1. 克隆此代码库。
```bash
git clone https://github.com/doem97/openai-proxy.git
cd openai-proxy
```

2. 将服务部署到Google Cloud Functions。请先编辑./deploy.sh并修改USER_ID和OPENAI_API_KEY，然后
```bash
bash ./deploy.sh
```
终端中的输出类似于这样：
```bash
...
url: https://ip-address-of-service.cloudfunctions.net/${USER_ID}
...
```
请复制粘贴此url以供后续使用：
```bash
export PROXY_URL="the_url_in_output" # 粘贴你获得的 url 在这里
```

## 使用
就像通常调用 OpenAI API 一样，但您需要将 API 地址更改为代理地址，并更改`Authorization: UserName`字段。
我在`request.sh`中给出了一个示例。像这样：
```bash
# 请注意 ${PROXY_URL} 为上一步获取的 url
curl ${PROXY_URL}/openai \
-H "Content-Type: application/json" \
-H "Authorization: UserName ${USER_ID}" \
-d '{
    "model": "gpt-4",
    "messages": [{"role": "user", "content": "Hello world!"}]
  }'
```
## 查看各用户用量
打开浏览器并导航到`${PROXY_URL}/log`。您将看到相应用户的使用情况。

**警告!!!** 尽管在OpenAI使用条款中没有明确提到，但使用此代理将您剩余的配额分享/分发给公众可能被认为是违反 OpenAI 规则的行为，将导致帐户受限/禁止。请不要尝试这样做！！请仅在您的团队内使用此系统来控制 API 访问。
