import os
import sys
import discord
from discord.ext import commands

bot = commands.Bot(command_prefix=">", intents=discord.Intents.default())

#Get MainRGB.py for pulling function.
funcPath = os.path.abspath(os.path.join(os.path.dirname(__file__), '../..', 'Name_To_RGB'))
sys.path.append(funcPath)
from mainRGB import textToRGB

class RGBCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # Slash command example
    @commands.Cog.listener()
    async def on_ready(self):
        print("RGB Cog is ready!")

    @commands.Cog.listener()
    async def on_guild_available(self, guild):
            print(f"Guild available: {guild.name} ({guild.id}) - Syncing commands...")
            await self.bot.tree.sync(guild=guild)
            print("Commands synced for this guild.")

    @bot.tree.command(name="testing", description="A simple plain boring command meant only for testing.")
    async def testing(self, interaction: discord.Interaction):
        await interaction.response.send_message("This is a command for testing!(updated YET again)")

    @bot.tree.command(name="name2rgb", description="Converts a name to RGB values.")
    async def name2rgb(self, interaction: discord.Interaction, name: str):
        RGB = textToRGB(name)
        await interaction.response.send_message(RGB)
        #await interaction.response.send_embed(title="Test", description="More Testing")


# Sets up the bot
async def setup(bot):
    await bot.add_cog(RGBCog(bot))
    print("RGB Cog loaded!")