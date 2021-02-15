[![Build Status](https://travis-ci.com/Squishy123/cps847-assignment-1.svg?branch=main)](https://travis-ci.com/Squishy123/cps847-assignment-1)

## Getting Started

```
pip install -r requirements.txt
cp .env.example .env
```

## Setup NGROK
```
ngrok http http://127.0.0.1:5000 80
```

Setup slack event subscription: https://api.slack.com/apps/A01N5EF242E/event-subscriptions?

request link is: NGROK_URL/slack/events

## Setup Slack

Features -> Incoming Webhooks -> Activate this

Scope permissions:

- app_mentions:read
- channels:history
- channels:read
- chat:write
- chat:write.public
- im:history
- incoming-webhook

Features -> Event Subscriptions:

Subscribe to bot events:

- app_mention
- message.channels
- message.im

**MAKE SURE TO INVITE THE BOT MANUALLY IN THE SLACK CHANNEL ON THE SLACK APP!**