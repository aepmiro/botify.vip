import discord
import asyncio
import os
import sys
import requests
from colorama import Fore, init

# Initialize colorama
init(autoreset=True)

# ── Auto-update Configuration ──
VERSION_URL = "https://raw.githubusercontent.com/aepmiro/botify.vip/main/version.txt"
SCRIPT_URL = "https://raw.githubusercontent.com/aepmiro/botify.vip/main/main.py"
LOCAL_VERSION = "1.0.0"  # Match this to your current version

def check_for_updates():
    try:
        res = requests.get(VERSION_URL)
        latest_version = res.text.strip()

        if latest_version != LOCAL_VERSION:
            print(Fore.YELLOW + f"\n🔄 Update available: {latest_version}")
            download_update()
        else:
            print(Fore.GREEN + f"\n✅ Running version {LOCAL_VERSION} — Up to date.")
    except Exception as e:
        print(Fore.RED + f"\n⚠️ Could not check for updates: {e}")

def download_update():
    try:
        res = requests.get(SCRIPT_URL)
        with open("main.py", "w", encoding="utf-8") as f:
            f.write(res.text)
        print(Fore.GREEN + "✅ Update downloaded. Restarting...")
        os.execv(sys.executable, ['python'] + sys.argv)
    except Exception as e:
        print(Fore.RED + f"❌ Update failed: {e}")

# ── Banner & Menu ──
def show_banner():
    os.system("cls" if os.name == "nt" else "clear")
    print(Fore.RED + r"""
 ________  ________  _________  ___  ________ ___    ___ 
|\   __  \|\   __  \|\___   ___\\  \|\  _____\\  \  /  /|
\ \  \|\ /\ \  \|\  \|___ \  \_\ \  \ \  \__/\ \  \/  / /
 \ \   __  \ \  \\\  \   \ \  \ \ \  \ \   __\\ \    / /  
  \ \  \|\  \ \  \\\  \   \ \  \ \ \  \ \  \_| \/  /  /   
   \ \_______\ \_______\   \ \__\ \ \__\ \__\__/  / /     
    \|_______|\|_______|    \|__|  \|__|\|__|\___/ /      
                                            \|___|/       
    """)
    print(Fore.RED + "[01] Send Messages")
    print(Fore.RED + "[02] Create Channels")
    print(Fore.RED + "[03] Delete Channels")
    print(Fore.RED + "[X] Exit")
    choice = input(Fore.RED + "\nChoose an option: ").lower()
    os.system("cls" if os.name == "nt" else "clear")
    return choice

# ── Core Features ──

async def send_messages(token, guild_id, message, count):
    intents = discord.Intents.default()
    client = discord.Client(intents=intents)

    @client.event
    async def on_ready():
        guild = client.get_guild(guild_id)
        if guild:
            tasks = [channel.send(message) for channel in guild.text_channels for _ in range(count)]
            try:
                await asyncio.gather(*tasks)
                print(Fore.GREEN + f"✅ Sent message to all channels in {guild.name} — Token: {token}")
            except Exception as e:
                print(Fore.RED + f"❌ Error sending messages — {e}")
        await client.close()

    await client.start(token)

async def create_channels(token, guild_id, name, count):
    intents = discord.Intents.default()
    client = discord.Client(intents=intents)

    @client.event
    async def on_ready():
        guild = client.get_guild(guild_id)
        if guild:
            for _ in range(count):
                try:
                    await guild.create_text_channel(name)
                    print(Fore.GREEN + f"✅ Created channel: {name} — Token: {token}")
                except Exception as e:
                    print(Fore.RED + f"❌ Could not create channel — {e}")
                await asyncio.sleep(0.2)
        await client.close()

    await client.start(token)

async def delete_channels(token, guild_id):
    intents = discord.Intents.default()
    client = discord.Client(intents=intents)

    @client.event
    async def on_ready():
        guild = client.get_guild(guild_id)
        if guild:
            tasks = [channel.delete() for channel in guild.text_channels]
            try:
                await asyncio.gather(*tasks)
                print(Fore.GREEN + f"✅ Deleted all text channels in {guild.name} — Token: {token}")
            except Exception as e:
                print(Fore.RED + f"❌ Error deleting channels — {e}")
        await client.close()

    await client.start(token)

# ── Main Loop ──

async def main():
    check_for_updates()

    while True:
        choice = show_banner()

        if choice == "1":
            with open("tokens.txt", "r") as f:
                tokens = [line.strip() for line in f]
            guild_id = int(input(Fore.RED + "Enter Server ID: "))
            message = input(Fore.RED + "Enter your message: ")
            count = int(input(Fore.RED + "Send how many times per channel? "))
            for token in tokens:
                await send_messages(token, guild_id, message, count)

        elif choice == "2":
            with open("tokens.txt", "r") as f:
                tokens = [line.strip() for line in f]
            guild_id = int(input(Fore.RED + "Enter Server ID: "))
            name = input(Fore.RED + "Enter channel name: ")
            count = int(input(Fore.RED + "How many channels to create? "))
            for token in tokens:
                await create_channels(token, guild_id, name, count)

        elif choice == "3":
            with open("tokens.txt", "r") as f:
                tokens = [line.strip() for line in f]
            guild_id = int(input(Fore.RED + "Enter Server ID: "))
            for token in tokens:
                await delete_channels(token, guild_id)

        elif choice == "x":
            print(Fore.RED + "Exiting...")
            break

        else:
            print(Fore.RED + "This is not a valid choice")

if __name__ == "__main__":
    asyncio.run(main())
