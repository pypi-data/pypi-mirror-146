import json
import httpx
import asyncio


async def send_slack_channel_notification():
    message = {
        "blocks": [
            {
                "type": "divider"
            },
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": 'test'
                }
            }
        ]
    }

    slack_payload = json.dumps(message).encode("utf-8")
    slack_headers = [(b"content-type", b"application/json")]

    slack_url = "https://hooks.slack.com/services/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"


    async with httpx.AsyncClient() as client:
        await client.post(
                slack_url, headers=slack_headers, data=slack_payload
            )


asyncio.run(send_slack_channel_notification())

