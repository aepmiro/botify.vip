import discord
import asyncio
import os
from colorama import Fore, init

# Initialize colorama for Windows compatibility
init(autoreset=True)

# ASCII Banner and Menu
def show_banner():
    os.system("cls" if os.name == "nt" else "clear")  # Clears screen before displaying banner
    banner = """
 ________  ________  _________  ___  ________ ___    ___ 
|\   __  \|\   __  \|\___   ___\\  \|\  _____\\  \  /  /|
\ \  \|\ /\ \  \|\  \|___ \  \_\ \  \ \  \__/\ \  \/  / /
 \ \   __  \ \  \\\  \   \ \  \ \ \  \ \   __\\ \    / /  
  \ \  \|\  \ \  \\\  \   \ \  \ \ \  \ \  \_| \/  /  /   
   \ \_______\ \_______\   \ \__\ \ \__\ \__\__/  / /     
    \|_______|\|_______|    \|__|  \|__|\|__|\___/ /      
                                            \|___|/       
    """
    print(Fore.RED + banner)  
    print(Fore.RED + "[01] Send Messages")
    print(Fore.RED + "[02] Create Channels")
    print(Fore.RED + "[03] Delete Channels")
    print(Fore.RED + "[04] Create Roles")  # New feature
    print(Fore.RED + "[05] Delete Roles")  # New feature
    print(Fore.RED + "[X] Exit")
    
    choice = input(Fore.RED + "\nChoose an option: ").lower()
    os.system("cls" if os.name == "nt" else "clear")  
    return choice

async def send_messages(token, guild_id, message, spam, delay_ms, count):
    intents = discord.Intents.default()
    client = discord.Client(intents=intents)

    @client.event
    async def on_ready():
        guild = client.get_guild(guild_id)
        if guild:
            tasks = [channel.send(message) for channel in guild.text_channels for _ in range(count)]
            try:
                await asyncio.gather(*tasks)
                print(Fore.GREEN + f"Messages sent in {guild.name}. Token: {token}")
            except discord.errors.HTTPException as e:
                print(Fore.RED + f"Failed to send messages. Token: {token} - Error: {e}")

        await client.close()

    await client.start(token)

async def create_channels(token, guild_id, channel_name, count):
    intents = discord.Intents.default()
    client = discord.Client(intents=intents)

    @client.event
    async def on_ready():
        guild = client.get_guild(guild_id)
        if guild:
            for _ in range(count):
                try:
                    await guild.create_text_channel(channel_name)
                    print(Fore.GREEN + f"Created channel '{channel_name}'. Token: {token}")
                except discord.errors.Forbidden:
                    print(Fore.RED + f"Bot lacks permission to create channels. Token: {token}")
                except Exception as e:
                    print(Fore.RED + f"Failed to create channel. Token: {token} - Error: {e}")

                await asyncio.sleep(0.15)

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
                print(Fore.GREEN + f"All channels deleted in {guild.name}. Token: {token}")
            except discord.errors.Forbidden:
                print(Fore.RED + f"Bot lacks permission to delete channels. Token: {token}")
            except Exception as e:
                print(Fore.RED + f"Failed to delete channels. Token: {token} - Error: {e}")

        await client.close()

    await client.start(token)

async def create_roles(token, guild_id, role_name, count, delay):
    intents = discord.Intents.default()
    client = discord.Client(intents=intents)

    @client.event
    async def on_ready():
        guild = client.get_guild(guild_id)
        if guild:
            for _ in range(count):
                try:
                    await guild.create_role(name=role_name)
                    print(Fore.GREEN + f"Created role '{role_name}'. Token: {token}")
                    await asyncio.sleep(delay / 1000)
                except Exception as e:
                    print(Fore.RED + f"Failed to create role. Token: {token} - Error: {e}")

        await client.close()

    await client.start(token)

async def delete_roles(token, guild_id):
    intents = discord.Intents.default()
    client = discord.Client(intents=intents)

    @client.event
    async def on_ready():
        guild = client.get_guild(guild_id)
        if guild:
            for role in guild.roles:
                try:
                    if role.name != "@everyone" and not role.is_bot_managed():
                        await role.delete()
                        print(Fore.GREEN + f"Deleted role '{role.name}'. Token: {token}")
                except Exception as e:
                    print(Fore.RED + f"Failed to delete role. Token: {token} - Error: {e}")

        await client.close()

    await client.start(token)

async def main():
    while True:
        choice = show_banner()

        if choice == "1":
            with open("tokens.txt", "r") as f:
                tokens = [line.strip() for line in f.readlines()]

            guild_id = int(input(Fore.RED + "Enter Server ID: "))
            message = input(Fore.RED + "Enter message: ")
            spam = input(Fore.RED + "Spam messages? (y/n): ")
            count = 1 if spam.lower() != "y" else int(input(Fore.RED + "How many times? "))
            delay_ms = 1000 if spam.lower() != "y" else int(input(Fore.RED + "Delay (ms): "))

            for token in tokens:
                await send_messages(token, guild_id, message, spam, delay_ms, count)

        elif choice == "2":
            with open("tokens.txt", "r") as f:
                tokens = [line.strip() for line in f.readlines()]

            guild_id = int(input(Fore.RED + "Enter Server ID: "))
            channel_name = input(Fore.RED + "Enter channel name: ")
            count = int(input(Fore.RED + "Number of channels: "))

            for token in tokens:
                await create_channels(token, guild_id, channel_name, count)

        elif choice == "3":
            with open("tokens.txt", "r") as f:
                tokens = [line.strip() for line in f.readlines()]

            guild_id = int(input(Fore.RED + "Enter Server ID: "))

            for token in tokens:
                await delete_channels(token, guild_id)

        elif choice == "4":
            with open("tokens.txt", "r") as f:
                tokens = [line.strip() for line in f.readlines()]

            guild_id = int(input(Fore.RED + "Enter Server ID: "))
            role_name = input(Fore.RED + "Enter role name: ")
            count = int(input(Fore.RED + "Number of roles: "))
            delay = int(input(Fore.RED + "Delay (ms) between creations: "))

            for token in tokens:
                await create_roles(token, guild_id, role_name, count, delay)

        elif choice == "5":
            with open("tokens.txt", "r") as f:
                tokens = [line.strip() for line in f.readlines()]

            guild_id = int(input(Fore.RED + "Enter Server ID: "))

            for token in tokens:
                await delete_roles(token, guild_id)

        elif choice == "x":
            print(Fore.RED + "Exiting...")
            break

        else:
            print(Fore.RED + "Invalid choice.")

asyncio.run(main())
