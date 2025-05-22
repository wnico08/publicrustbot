# Simple Hosting Guide for Rust Wipe Bot

This guide will help you host your Discord bot for free using Replit and UptimeRobot - super easy setup!

## Step 1: Set Up Replit
1. Go to [Replit](https://replit.com)
2. Sign up for a free account
3. Click "Create Repl"
4. Choose:
   - Name: rust-wipe-bot
   - Language: Python
   - Template: Python

## Step 2: Add Your Files
1. Upload these files to your Repl:
   - rust_wipe_bot.py
   - requirements.txt

2. Create a new file called `.env` and add your tokens:
```
DISCORD_TOKEN=your_discord_token
BATTLEMETRICS_TOKEN=your_battlemetrics_token
```

## Step 3: Set Up UptimeRobot
1. Go to [UptimeRobot](https://uptimerobot.com)
2. Sign up for a free account
3. Click "Add New Monitor"
4. Choose:
   - Monitor Type: HTTP(s)
   - Friendly Name: Rust Wipe Bot
   - URL: Your Repl's URL (ends with .repl.co)
   - Monitoring Interval: 5 minutes

## Step 4: Run the Bot
1. In Replit, click the "Run" button
2. Your bot is now running and will stay online!

## Important Notes
- Replit's free tier includes:
  - Always-on repls (with UptimeRobot)
  - Automatic restarts
  - Easy code editing
- UptimeRobot's free tier includes:
  - 50 monitors
  - 5-minute check intervals
  - Email notifications if your bot goes down

## Troubleshooting
If the bot stops working:
1. Check the Replit console for error messages
2. Make sure your tokens are correct in the .env file
3. Click the "Run" button to restart the bot
4. Check UptimeRobot to see if your bot is responding 