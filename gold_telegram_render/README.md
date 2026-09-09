# 24K Gold Telegram Monitor

## What it does
- Uses Goodreturns India 24K published rate.
- You manually set reference date, reference price, and threshold in the dashboard.
- Render cron checks every 15 minutes.
- Sends Telegram alert when current price is at or beyond the threshold below/above the manual reference.

## Telegram setup
1. Open Telegram and search for @BotFather.
2. Send /newbot and follow the instructions.
3. BotFather gives you a bot token. Keep it secret.
4. Open your new bot and press Start (or send /start).
5. Get your numeric chat ID using an approved Telegram bot/API method.
6. In Render add:
   TELEGRAM_BOT_TOKEN = your bot token
   TELEGRAM_CHAT_IDS = your numeric chat ID
   Multiple IDs can be comma-separated.

## Deploy
Push the project to GitHub, then create a Render Blueprint from render.yaml.
