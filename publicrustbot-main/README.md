# Rust Wipe Bot

A Discord bot that tracks and displays the time until the next wipe for specific Rust servers using Battlemetrics integration.

## Features

- Track specific Rust servers using their Battlemetrics ID
- Shows time until next wipe using the `!wipe` command
- Displays wipe countdown in the bot's status
- Updates status every hour
- Shows detailed wipe information in an embedded message

## Setup

1. Fork this repository
2. Go to your repository's Settings
3. Click "Secrets and variables" → "Actions"
4. Add two new secrets:
   - `DISCORD_TOKEN`: Your Discord bot token
   - `BATTLEMETRICS_TOKEN`: Your Battlemetrics token
5. Go to the "Actions" tab
6. Click "Keep Bot Alive"
7. Click "Run workflow"

## Commands

- `!track <server_id>` - Start tracking a Rust server using its Battlemetrics ID
- `!untrack` - Stop tracking the current server
- `!wipe` - Shows the time until the next wipe for the tracked server

## Getting Server IDs

To find a server's Battlemetrics ID:
1. Go to [Battlemetrics](https://www.battlemetrics.com/servers)
2. Search for your Rust server
3. Click on the server
4. The ID is in the URL (e.g., https://www.battlemetrics.com/servers/1234567)

## Getting a Battlemetrics Token

1. Go to [Battlemetrics](https://www.battlemetrics.com)
2. Create an account or log in
3. Go to your profile settings
4. Navigate to the API section
5. Create a new token with the "servers" scope

## Note

The bot assumes servers wipe monthly based on their last wipe date. If a server uses a different wipe schedule, the times shown may not be accurate. 