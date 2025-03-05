import os
import sys
from dotenv import load_dotenv
import time
import discord
import importlib
from discord.ext import commands
import threading
import time
import asyncio
from botFlask import app, run_flask
from flask import Flask, request, redirect, url_for, render_template, jsonify
load_dotenv()

GUILD_ID = "1341546870740095006"

## Sets up to send messages ##
# Sets up for Guilds #
async def send_message_to_guild(guild_id, message):
    guild = bot.get_guild(int(guild_id))
    if guild and guild.text_channels:
        # Here we select the first text channel; adjust logic as needed
        channel = guild.text_channels[0]
        await channel.send(message)
        print("Message sent to guild!")
    else:
        print("Guild or text channel not found.")


# Sets up for Channels #
async def send_message_to_channel(guild_id, channel_id, text, bot):
    """Sends a message to the specified channel in a given guild."""
    guild = bot.get_guild(int(guild_id))
    if not guild:
        print(f"Guild {guild_id} not found.")
        return
    
    channel = guild.get_channel(int(channel_id))
    if not channel:
        print(f"Channel {channel_id} not found in guild {guild_id}.")
        return
    
    await channel.send(text)


## Flask Server ##
@app.route('/trigger')
def trigger():
    # Get text and guild_id from the URL query parameters
    text = request.args.get('text')
    guild_id = GUILD_ID
    print("Trigger received:", text, "for guild", guild_id)
    
    if not text or not guild_id:
        return "Missing 'text' or 'guild_id' parameter!", 400
    
    # Use asyncio.run_coroutine_threadsafe to schedule the coroutine in the bot's event loop
    future = asyncio.run_coroutine_threadsafe(send_message_to_guild(guild_id, text), bot.loop)
    try:
        # Wait for the coroutine to complete
        future.result(timeout=10)
    except Exception as e:
        return f"Error sending message: {e}", 500
    return redirect(url_for('index'))


@app.route('/trigger_dream')
def trigger_dream():
    # Get text and guild_id from the URL query parameters
    text = request.args.get('text')
    guild_id = 1324513122698133565
    print("Trigger received:", text, "for guild", guild_id)
    
    if not text or not guild_id:
        return "Missing 'text' or 'guild_id' parameter!", 400
    channel_id = 1344463837721792613
    # Use asyncio.run_coroutine_threadsafe to schedule the coroutine in the bot's event loop
    future = asyncio.run_coroutine_threadsafe(send_message_to_channel(guild_id, channel_id, text, bot), bot.loop)
    try:
        # Wait for the coroutine to complete
        future.result(timeout=10)
    except Exception as e:
        return f"Error sending message: {e}", 500
    return redirect(url_for('index'))

## Import Commands From Other Files ##
commands_dir = os.path.join(os.path.dirname(__file__), "botCommands")
import botCommands.rgb

token = os.getenv('DISC_TOKEN')


intents = discord.Intents.all()
intents.message_content = True
bot = commands.Bot(command_prefix='>', intents=intents)

## Simple Ping Command ##
@bot.tree.command(name="ping", description="Get bot response time.")
async def ping(interaction: discord.Interaction):
    latency = bot.latency * 1000  # Convert to milliseconds
    await interaction.response.send_message(f"Pong! Latency is {latency:.2f}ms.")

## Reload Commands In Cogs ##
@bot.tree.command(name="reload", description="Reloads the commands for a specific server.")
async def reload(interaction: discord.Interaction):
    # Check if the user has administrator permissions
    if not interaction.user.guild_permissions.administrator:
        await interaction.response.send_message("You do not have permission to use this command!", ephemeral=True)
        return

    begin = time.time()
    await interaction.response.defer(thinking=True)
    try:
        ## Define the path to the botCommands directory ##
        commands_dir = os.path.join(os.path.dirname(__file__), "botCommands")

        ## Import and reload the 'botCommands.rgb' module (adjust if needed) ##
        import botCommands.rgb       

        ## Ensure the cog is loaded before reloading ##
        if "botCommands.rgb" not in sys.modules:
            await bot.load_extension("botCommands.rgb")  # Load first
            print("Cog was not loaded, now loaded.")
        else:
            print("Cog was already loaded.")

        ## Ensures the extension is loaded ##
        await bot.reload_extension("botCommands.rgb")  # Reload the extension
    except Exception as e:
        await interaction.followup.send(f"An error occurred while reloading commands: {str(e)}")
        return

    ## Sync the command tree ##
    try:
        await bot.tree.sync()
        end = time.time() 
        cmd_resp = await interaction.followup.send(f"Reloaded Commands in {round(end - begin)} seconds!", ephemeral=True)
        await cmd_resp.delete(delay=2)
        print(f"Total runtime for reload was {end - begin}")
    except Exception as e:
        await interaction.followup.send(f"Error syncing: {e}")


## When Bot Is Ready##
@bot.event
async def on_ready():
    commands_dir = os.path.join(os.path.dirname(__file__), "botCommands")
    import botCommands.rgb
    print(f"Logged in as {bot.user}!")
    # Sync the slash commands with the Discord API
    guild = discord.Object(id="1341546870740095006")
    try:
        await bot.load_extension("botCommands.rgb")  # Load the cog
        print("Cog loaded successfully!")
    except Exception as e:
        print(f"Error loading cog: {e}")
    await bot.tree.sync(guild=guild)
    await bot.tree.sync()



## Runs Flask Server ##
flask_thread = threading.Thread(target=run_flask, daemon=True)
flask_thread.start()

## Runs the bot##
bot.run(str(token))