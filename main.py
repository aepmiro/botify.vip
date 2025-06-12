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
    print(Fore.RED + banner)  # Menu is now fully red
    print(Fore.RED + "[01] Send Messages")
    print(Fore.RED + "[02] Create Channels")
    print(Fore.RED + "[03] Delete Channels")
    print(Fore.RED + "[X] Exit")
    
    choice = input(Fore.RED + "\nChoose an option: ").lower()  # Simple prompt without listing inputs
    
    os.system("cls" if os.name == "nt" else "clear")  # Clears screen AFTER selection
    return choice

async def send_messages(token, guild_id, message, spam, delay_ms, count):
    intents = discord.Intents.default()
    client = discord.Client(intents=intents)

    @client.event
    async def on_ready():
        os.system("cls" if os.name == "nt" else "clear")  # Clears screen before first log
        guild = client.get_guild(guild_id)

        if guild:
            tasks = []  # Store async tasks for simultaneous execution
            for channel in guild.text_channels:  # Get all text channels
                for _ in range(count):
                    tasks.append(channel.send(message))  # Queue message sends
            
            try:
                await asyncio.gather(*tasks)  # Execute all sends simultaneously
                print(Fore.GREEN + f"Messages sent across all channels in {guild.name}! {token}")
            except discord.errors.HTTPException as e:
                if "rate-limited" in str(e).lower():
                    print(Fore.RED + f"You are being rate-limited. {token}")
                else:
                    print(Fore.RED + f"Message failed! {token} - Error: {e}")

        await client.close()

    await client.start(token)

async def create_channels(token, guild_id, channel_name, count):
    intents = discord.Intents.default()
    client = discord.Client(intents=intents)

    @client.event
    async def on_ready():
        os.system("cls" if os.name == "nt" else "clear")  # Clears screen before first log
        guild = client.get_guild(guild_id)

        if guild:
            for _ in range(count):
                try:
                    await guild.create_text_channel(channel_name)
                    print(Fore.GREEN + f"Channel '{channel_name}' created successfully! {token}")
                except discord.errors.Forbidden:
                    print(Fore.RED + f"Bot lacks permission to create channels in the server. {token}")
                except Exception as e:
                    print(Fore.RED + f"Failed to create channel! {token} - Error: {e}")

                await asyncio.sleep(0.15)  # 150 milliseconds delay

        await client.close()

    await client.start(token)

async def delete_channels(token, guild_id):
    intents = discord.Intents.default()
    client = discord.Client(intents=intents)

    @client.event
    async def on_ready():
        os.system("cls" if os.name == "nt" else "clear")  # Clears screen before first log
        guild = client.get_guild(guild_id)

        if guild:
            tasks = []  # Store tasks to delete channels simultaneously
            for channel in guild.text_channels:  # Get all text channels
                tasks.append(channel.delete())

            try:
                await asyncio.gather(*tasks)  # Execute all deletions at once
                print(Fore.GREEN + f"All channels deleted in {guild.name}! {token}")
            except discord.errors.Forbidden:
                print(Fore.RED + f"Bot lacks permission to delete channels in the server. {token}")
            except Exception as e:
                print(Fore.RED + f"Failed to delete channels! {token} - Error: {e}")

        await client.close()

    await client.start(token)

async def main():
    while True:
        choice = show_banner()  # Display menu

        if choice == "1":  # Send Messages
            with open("tokens.txt", "r") as f:
                tokens = [line.strip() for line in f.readlines()]

            guild_id = int(input(Fore.RED + "Enter the Server (Guild) ID: "))  # Only server ID is needed!
            message = input(Fore.RED + "Enter your message: ")
            spam = input(Fore.RED + "Do you want to spam the message? (y/n): ")

            delay_ms = 1000  # Default delay in milliseconds
            count = 1  # Default message count

            if spam.lower() == "y":
                count = int(input(Fore.RED + "How many times should the message be sent? "))
                delay_ms = int(input(Fore.RED + "Enter delay between messages (in milliseconds): "))

            for token in tokens:
                try:
                    await send_messages(token, guild_id, message, spam, delay_ms, count)
                except Exception as e:
                    print(f"Error with token {token}: {e}")

        elif choice == "2":  # Create Channels
            with open("tokens.txt", "r") as f:
                tokens = [line.strip() for line in f.readlines()]

            guild_id = int(input(Fore.RED + "Enter the Server (Guild) ID: "))
            channel_name = input(Fore.RED + "Enter the channel name: ")
            count = int(input(Fore.RED + "How many channels should be created? "))

            for token in tokens:
                try:
                    await create_channels(token, guild_id, channel_name, count)
                except Exception as e:
                    print(f"Error with token {token}: {e}")

        elif choice == "3":  # Delete Channels
            with open("tokens.txt", "r") as f:
                tokens = [line.strip() for line in f.readlines()]

            guild_id = int(input(Fore.RED + "Enter the Server (Guild) ID: "))

            for token in tokens:
                try:
                    await delete_channels(token, guild_id)
                except Exception as e:
                    print(f"Error with token {token}: {e}")

        elif choice == "x":  # Exit program
            print(Fore.RED + "Exiting program...")
            break  # Stop the loop

        else:
            print(Fore.RED + "This is not a valid choice")  # Error message for invalid input

asyncio.run(main())