import discord
from discord.ext import commands, tasks
from datetime import datetime, timedelta
import os
import json
import requests
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Bot setup
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='!', intents=intents)

# Store tracked servers
TRACKED_SERVERS_FILE = 'tracked_servers.json'

def load_tracked_servers():
    if os.path.exists(TRACKED_SERVERS_FILE):
        with open(TRACKED_SERVERS_FILE, 'r') as f:
            return json.load(f)
    return {}

def save_tracked_servers(servers):
    with open(TRACKED_SERVERS_FILE, 'w') as f:
        json.dump(servers, f, indent=4)

# Initialize tracked servers
tracked_servers = load_tracked_servers()

def get_server_info(server_id):
    """Get server information from Battlemetrics"""
    url = f"https://api.battlemetrics.com/servers/{server_id}"
    headers = {
        "Authorization": f"Bearer {os.getenv('BATTLEMETRICS_TOKEN')}",
        "Accept": "application/json"
    }
    
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error fetching server info: {e}")
        return None

def get_next_wipe(server_info):
    """Get next wipe time from server info"""
    if not server_info or 'data' not in server_info:
        return None
    
    attributes = server_info['data']['attributes']
    if 'details' in attributes and 'rust_last_wipe' in attributes['details']:
        last_wipe = datetime.fromisoformat(attributes['details']['rust_last_wipe'].replace('Z', '+00:00'))
        # Assuming monthly wipes
        next_wipe = last_wipe + timedelta(days=30)
        return next_wipe
    return None

@bot.event
async def on_ready():
    print(f'{bot.user} has connected to Discord!')
    update_status.start()

@tasks.loop(minutes=60)
async def update_status():
    if not tracked_servers:
        await bot.change_presence(activity=None)
        return
    
    # Get the next wipe from any tracked server
    next_wipe = None
    next_server_name = None
    
    for guild_id, server_id in tracked_servers.items():
        server_info = get_server_info(server_id)
        if server_info:
            wipe_time = get_next_wipe(server_info)
            if wipe_time and (next_wipe is None or wipe_time < next_wipe):
                next_wipe = wipe_time
                next_server_name = server_info['data']['attributes']['name']
    
    if next_wipe:
        time_until = next_wipe - datetime.now(next_wipe.tzinfo)
        days = time_until.days
        hours = time_until.seconds // 3600
        
        await bot.change_presence(
            activity=discord.Activity(
                type=discord.ActivityType.watching,
                name=f"{next_server_name} wipe in {days}d {hours}h"
            )
        )
    else:
        await bot.change_presence(activity=None)

@bot.command(name='track')
async def track_server(ctx, server_id: str):
    """Track a Rust server using its Battlemetrics ID"""
    if not os.getenv('BATTLEMETRICS_TOKEN'):
        await ctx.send("❌ Battlemetrics API token not configured. Please set BATTLEMETRICS_TOKEN in .env file.")
        return
    
    server_info = get_server_info(server_id)
    if not server_info:
        await ctx.send("❌ Could not find server with that ID. Please check the Battlemetrics ID and try again.")
        return
    
    server_name = server_info['data']['attributes']['name']
    tracked_servers[str(ctx.guild.id)] = server_id
    save_tracked_servers(tracked_servers)
    
    embed = discord.Embed(
        title="Server Tracking Started",
        description=f"Now tracking wipe times for: {server_name}",
        color=discord.Color.green()
    )
    await ctx.send(embed=embed)

@bot.command(name='untrack')
async def untrack_server(ctx):
    """Stop tracking the current server"""
    if str(ctx.guild.id) in tracked_servers:
        del tracked_servers[str(ctx.guild.id)]
        save_tracked_servers(tracked_servers)
        await ctx.send("✅ Server tracking stopped.")
    else:
        await ctx.send("❌ No server is currently being tracked.")

@bot.command(name='wipe')
async def wipe_time(ctx):
    """Shows the time until the next wipe for the tracked server"""
    server_id = tracked_servers.get(str(ctx.guild.id))
    if not server_id:
        await ctx.send("❌ No server is currently being tracked. Use `!track <server_id>` to start tracking a server.")
        return
    
    server_info = get_server_info(server_id)
    if not server_info:
        await ctx.send("❌ Could not fetch server information. Please try again later.")
        return
    
    server_name = server_info['data']['attributes']['name']
    next_wipe = get_next_wipe(server_info)
    
    if not next_wipe:
        await ctx.send("❌ Could not determine next wipe time for this server.")
        return
    
    time_until = next_wipe - datetime.now(next_wipe.tzinfo)
    days = time_until.days
    hours = time_until.seconds // 3600
    minutes = (time_until.seconds % 3600) // 60
    
    embed = discord.Embed(
        title=f"Next Wipe for {server_name}",
        description=f"The next wipe will occur on {next_wipe.strftime('%B %d, %Y')} at {next_wipe.strftime('%H:%M')} UTC",
        color=discord.Color.orange()
    )
    embed.add_field(
        name="Time Remaining",
        value=f"{days} days, {hours} hours, and {minutes} minutes",
        inline=False
    )
    
    await ctx.send(embed=embed)

# Run the bot
bot.run(os.getenv('DISCORD_TOKEN')) 