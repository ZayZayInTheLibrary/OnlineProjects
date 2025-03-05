import os
import sys
import discord
import json
import requests
from discord.ext import commands
from PIL import Image

bot = commands.Bot(command_prefix=">", intents=discord.Intents.default())
colorAPI = " https://www.thecolorapi.com/id"

def generate_color_image(color, width=200, height=200):
    # Create a new image with the specified color
    img = Image.new("RGB", (width, height), color)
    filename = f"color_{color}.png"
    # Save the image
    img.save(filename) 
    return(f'color_{color}.png')


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
        hexd = '#%02x%02x%02x' % RGB
        hexdInt = hexd.replace("#", "")
        hexdInt = int(hexdInt, 16)
        # Sets up for The Color API to retrieve name Color #
        rgb_ = str(RGB).replace(" ", "")
        params = {"rgb": rgb_, "format": "json"}
        colorResponse = requests.get(colorAPI, params=params)

        if colorResponse.status_code == 200:
            colorData = colorResponse.json()
            colorName = colorData.get("name", {}).get("value", "Unknown Color")
        else:
            print(f"Error: {colorResponse.status_code}")
        img = generate_color_image(hexd)
        file = discord.File(img, filename=f"color.png")
        embed = discord.Embed(title=f"{name}: <:gun:1343745716673314856>", description=f"{name}'s color is {colorName}\nRGB: {RGB}\nHEX: {hexd}",color=hexdInt)
        embed.set_thumbnail(url="attachment://color.png")
        await interaction.response.send_message(embed=embed, file=file)
        os.remove(img)


# Sets up the bot
async def setup(bot):
    await bot.add_cog(RGBCog(bot))
    print("RGB Cog Loaded/Updated!")