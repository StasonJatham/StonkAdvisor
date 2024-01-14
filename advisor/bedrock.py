import re
import json
import boto3


class Bedrock:
    def __init__(
        self, model="anthropic.claude-instant-v1", service_name="bedrock-runtime"
    ):
        self.model = model
        self.service_name = service_name

    def learn(
        self,
        description,
        style,
        command="",
        output_format="",
        max_tokens_to_sample=2048,
        temperature=0,
        top_p=0,
        top_k=250,
    ):
        brt = boto3.client(service_name=self.service_name)

        output_style = ""
        if style == "dumb":
            output_style = "Explain it in very simple terms even someone with no finance knowledge could understand"
        if style == "wsb":
            output_style = 'Explain it in popular subreddit "WallStreet Bets" language'

        if not command:
            command = (
                "Provide financial advice based on the news article. "
                + output_style
                + "You should write a list of some of your key points and summarize below."
            )

        if not output_format:
            output_format = ""

        body = {
            "prompt": f"\n\nHuman: <article>{description}</article>\n\n{command}\n{output_format}\n\nAssistant:",
            "max_tokens_to_sample": max_tokens_to_sample,
            "temperature": temperature,
            "top_p": top_p,
            "top_k": top_k,
        }

        accept = "application/json"
        contentType = "application/json"

        response = brt.invoke_model(
            body=json.dumps(body),
            modelId=self.model,
            accept=accept,
            contentType=contentType,
        )

        response_body = json.loads(response.get("body").read())

        return {
            "ai_response": response_body.get("completion"),
            "char_count": len(body["prompt"]),
        }

    def article(self, content):
        heading_pattern = re.compile(r"<heading>(.*?)</heading>", re.DOTALL)
        body_pattern = re.compile(r"<blogpost>(.*?)</blogpost>", re.DOTALL)

        heading_matches = heading_pattern.findall(content)
        body_matches = body_pattern.findall(content)

        if heading_matches and body_matches:
            return {
                "heading": heading_matches[0].strip(),
                "body": body_matches[0].strip(),
            }

        return None
