
import os
import httpx
from pydantic import Field, BaseModel
from mcp.server.fastmcp import FastMCP
from typing import List, Optional, Annotated, Literal, Union
import logging

VERSION = "v22.0"
PHONE_NUMBER_ID = os.environ["PHONE_NUMBER_ID"]
ACCESS_TOKEN = os.environ["ACCESS_TOKEN"]

headers = {
    "Authorization": f"Bearer {ACCESS_TOKEN}",
}

mcp = FastMCP("whatsapp-mcp")


# lark机器人发送单聊消息
@mcp.tool(description="send whatsapp text message")
async def send_text_message(
        to: Annotated[str, Field(description="Recipient's WhatsApp number in international format")],
        text: Annotated[str, Field(description="Text message content")],
) -> dict:
    url = f"https://graph.facebook.com/{VERSION}/{PHONE_NUMBER_ID}/messages"
    payload = {
        "messaging_product": "whatsapp",
        "to": to,
        "type": "text",
        "text": {"body": text},
    }
    async with httpx.AsyncClient() as client:
        response = await client.post(url, json=payload, headers=headers)
    return response.json()


@mcp.tool(description="send whatsapp template message")
async def send_template_message(
        to: Annotated[str, Field(description="Recipient's WhatsApp number in international format")],
        template_name: Annotated[str, Field(description="Template name")],
        language_code: Annotated[str, Field(description="Language code, e.g., en_US")] = "en_US",
        parameters: Annotated[Optional[List[str]], Field(description="List of template parameters")] = None,
) -> dict:
    url = f"https://graph.facebook.com/{VERSION}/{PHONE_NUMBER_ID}/messages"
    template_payload = {
        "name": template_name,
        "language": {"code": language_code},
    }
    if parameters:
        template_payload["components"] = [{
            "type": "body",
            "parameters": [{"type": "text", "text": param} for param in parameters]
        }]
    payload = {
        "messaging_product": "whatsapp",
        "to": to,
        "type": "template",
        "template": template_payload,
    }
    async with httpx.AsyncClient() as client:
        response = await client.post(url, json=payload, headers=headers)
    return response.json()


def main():
    mcp.run()


if __name__ == '__main__':
    main()
