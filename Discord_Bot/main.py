import os
import sys
from dotenv import load_dotenv
import time
import discord
import importlib
from discord.ext import commands
load_dotenv()



#Import Commands From Other Files
commands_dir = os.path.join(os.path.dirname(__file__), "botCommands")
import botCommands.rgb

token = os.getenv('DISC_TOKEN')


intents = discord.Intents.all()
intents.message_content = True
bot = commands.Bot(command_prefix='>', intents=intents)


@bot.tree.command(name="ping", description="Get bot response time.")
async def ping(interaction: discord.Interaction):
    latency = bot.latency * 1000  # Convert to milliseconds
    await interaction.response.send_message(f"Pong! Latency is {latency:.2f}ms.")

    
@bot.tree.command(name="reload", description="Reloads the commands for a specific server.")
@app_commands.default_permissions(administrator=True)
async def reload(interaction: discord.Interaction):
    begin = time.time()
    await interaction.response.defer(thinking=True)
    try:
        # Define the path to the botCommands directory
        commands_dir = os.path.join(os.path.dirname(__file__), "botCommands")
        # Import and reload the 'botCommands.rgb' module (adjust if needed)
        import botCommands.rgb       
                # Ensure the cog is loaded before reloading
        if "botCommands.rgb" not in sys.modules:
            await bot.load_extension("botCommands.rgb")  # Load first
            print("Cog was not loaded, now loaded.")
        else:
            print("Cog was already loaded.")
        # First, ensure the extension is loaded
        await bot.reload_extension("botCommands.rgb")  # Load it if not already loaded
    except Exception as e:
        await interaction.followup.send(f"An error occurred while reloading commands: {str(e)}")
    # Reload the extension to pick up changes
    try:
        await bot.tree.sync()
        end = time.time() 
        cmd_resp = await interaction.followup.send(f"Reloaded Commands in {round(end - begin)} seconds!", ephemeral=True)
        await cmd_resp.delete(delay=2)
        print(f"Total runtime for reload was {end - begin}")
    except Exception as e:
        await interaction.followup.send(f"Error syncing: {e}")


reload_command = "1341582119113064501"
guild_id = "1341546870740095006"
admin_role_id = "1341575018865492111"
everyone_role_id = "1341546870740095006"

#When Bot Is Ready Run
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

bot.run(str(token))