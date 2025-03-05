import os
import sys
from dotenv import load_dotenv
from flask import Flask, request, redirect, render_template
import requests
import json

load_dotenv()

SECRET = os.getenv("DISC_SECRET")
BOT_TOKEN = os.getenv("DISC_TOKEN")

app = Flask(__name__)

CLIENT_ID = "1341545136110305310"
CLIENT_SECRET = SECRET
REDIRECT_URI = "https://8080-zayzayinthelibrary-onlin-9p19d5303m.app.codeanywhere.com/callback"
TOKEN_REDIRECT_URI = "https://8080-zayzayinthelibrary-onlin-9p19d5303m.app.codeanywhere.com/get_token"


#Generate a OAuth2 URL from Discord Developer Portal using client ID, Redirecting to the callback URL.
DISCORD_OAUTH2_URL = "https://discord.com/oauth2/authorize?client_id=1341545136110305310&permissions=0&response_type=code&redirect_uri=https%3A%2F%2F8080-zayzayinthelibrary-onlin-9p19d5303m.app.codeanywhere.com%2Fcallback&integration_type=0&scope=identify+bot+applications.commands.permissions.update+applications.commands"

@app.route("/")
def home():
    return render_template("home.html")

@app.route("/perms")
def perms():
    return render_template("perms.html")


@app.route("/get_token")
def getToken():
    token_url = "https://discord.com/api/oauth2/token"
        # Get the 'code' sent by Discord
    code = request.args.get("code")
    if not code:
        return "Error: No code provided.", 400
    data = {
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET,
        "grant_type": "authorization_code",
        "code": code,
        "redirect_uri": TOKEN_REDIRECT_URI
    }
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded'
    }
    response = requests.post(token_url, data=data, headers=headers)
    token_info = response.json()

    # Check for access token in the response
    if "access_token" not in token_info:
        return f"Error: {token_info}", 400

    access_token = token_info["access_token"]

    # Use the access token to get user info
    user_info_url = "https://discord.com/api/users/@me"
    headers = {"Authorization": f"Bearer {access_token}"}
    user_info = requests.get(user_info_url, headers=headers).json()

    # Use the access token to get application info
    application_headers = {"Authorization": f"Bot {BOT_TOKEN}"}
    application_info_url = "https://discord.com/api/oauth2/applications/@me"
    application_info = requests.get(application_info_url, headers=application_headers).json()

    # Display user info
    #return f"Logged in as {user_info['username']}#{user_info['discriminator']}"
    token_write_data = {
        "application_info": application_info,
        "user_info": user_info
    }

    with open("token_data.json", "w") as file:
        json.dump(token_write_data, file, indent=4)
    return f"Logged in as {user_info['username']}\nBot Owner:{application_info['owner']['username']}"



@app.route("/add_bot")
def login():
    return redirect(DISCORD_OAUTH2_URL)


@app.route("/callback")
def callback():
    # Get the 'code' sent by Discord
    code = request.args.get("code")
    if not code:
        return "Error: No code provided.", 400

    # Exchange authorization code for an access token
    token_url = "https://discord.com/api/oauth2/token"
    data = {
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET,
        "grant_type": "authorization_code",
        "code": code,
        "redirect_uri": REDIRECT_URI
    }
    headers = {"Content-Type": "application/x-www-form-urlencoded"}

    # Send a POST request to get the access token
    response = requests.post(token_url, data=data, headers=headers)
    token_info = response.json()

    # Check for access token in the response
    if "access_token" not in token_info:
        return f"Error: {token_info}", 400

    access_token = token_info["access_token"]

    # Use the access token to get user info
    user_info_url = "https://discord.com/api/users/@me"
    headers = {"Authorization": f"Bearer {access_token}"}
    user_info = requests.get(user_info_url, headers=headers).json()

    write_data = {
        "access_token": access_token,
        "user_info": user_info
    }

    with open("data.json", "w") as file:
        json.dump(write_data, file, indent=4)

    # Display user info
    return f"Logged in as {user_info['username']}#{user_info['discriminator']}"

if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True, port=8080)