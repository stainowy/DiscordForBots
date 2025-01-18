import discord
from discord.ext import commands
import asyncio
import json5
from art import text2art
import os
from colorama import init, Fore
from collections import deque
import asyncio
import time

init()

with open("config.json5", "r") as config_file:
    config = json5.load(config_file)

PREFIX = config.get("prefix")
PING = config.get("ping")

STATUS_MODE = config.get("status_mode")
STATUS_CONTENT = config.get("status_content")

LIBRUARY_PATH = config.get("libruary_path")
LIBRUARY_STATUS = config.get("libruary_status")

intents = discord.Intents.all()

if len(PREFIX) > 4:
    PREFIX = "dfb."

bot = commands.Bot(command_prefix=PREFIX, intents=intents)


class InfoButtom(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label="Discord For Bots", style=discord.ButtonStyle.gray)
    async def info(self, interaction: discord.Interaction, button: discord.ui.Button):
        embed = discord.Embed(description=f"Discord For Bots is an unofficial open source program that lets you run discord as your own app! Want to download it? You can find the exe file and the code on [github]( https://github.com/stainowy/DiscordForBots)!", color=0x0e3972) 
        await interaction.response.send_message(embed=embed, ephemeral=True)

def clear_console():
    command = 'cls' if os.name == 'nt' else 'clear'
    os.system(command)

def start_widget():
    title = text2art("Discord For Bots")
    print(f"{Fore.LIGHTBLUE_EX}{title}")
    print(f"{Fore.CYAN}GITHUB {Fore.WHITE} https://github.com/stainowy/DiscordForBots")
    print(f"{Fore.CYAN}AUTHOR {Fore.WHITE} https://stainowy.gihub.io")
    print("")


async def get_debug(content: str):
    STATUS = config.get("debug")
    if STATUS == "ON":
        print(f"{Fore.GREEN}DEBUG {Fore.WHITE} {content}")
    else:
        pass

async def get_error(content: str):
    print(f"{Fore.RED}ERROR {Fore.WHITE} {content}")

async def get_keypress():
    loop = asyncio.get_event_loop()
    return await loop.run_in_executor(None, input, "")

@bot.command(name="ping")
async def ping(ctx):
    start_time = time.time()
    COMMAND = config.get("commands")
    if COMMAND == "ON":
        try:
            await get_debug(f"User '{ctx.author.name}' used a command '{PREFIX}ping'")
            bot_ping = round(bot.latency * 1000)
            end_time = time.time()
            client_ping = round((end_time - start_time) * 1000)
            embed = discord.Embed(description=f"> Bot ping: ``{bot_ping}ms``\n> Client ping: ``{client_ping}ms``")
            await ctx.send(embed=embed, view=InfoButtom())
            
        except Exception as e:
            await get_error(e)
    else:
        await get_debug(f"User '{ctx.author.name}' tried to use the '{PREFIX}ping' command but it is disabled in the config")

@bot.event
async def on_message(message):
    if message.content.strip() == f'<@{bot.user.id}>' or message.content.strip() == f'<@!{bot.user.id}>':
        if PING == "ON":
            embed = discord.Embed(description=f"Hi, I'm {bot.user.name}. And I'm an application launched with DiscordForBots :)", color=0x0e3972) 
            await message.channel.send(f'{message.author.mention}', embed=embed, view=InfoButtom())
            await get_debug(f"User '{message.author.name}' used a command '@ping'")
        else:
            await get_debug(f"User '{message.author.name}' tried to use the '@ping' command but it is disabled in the config")
            pass

async def get_user_id_or_nick(input_value, bot):
    if input_value.startswith("@"):
        nick = input_value[1:]
        for guild in bot.guilds:
            member = discord.utils.get(guild.members, name=nick)
            if member:
                return member.id
        await get_error(f"User with nickname '{nick}' not found!")
        raise ValueError("User not found.")
    else:
        try:
            return int(input_value)
        except ValueError:
            await get_error("Invalid user ID format!")
            raise ValueError("Invalid ID.")


async def select_options():
    print(f" {Fore.CYAN}[1] {Fore.WHITE}Browse servers")
    print(f" {Fore.CYAN}[2] {Fore.WHITE}Send DM")
    print(f" {Fore.CYAN}[3] {Fore.WHITE}Edit Profile")
    while True:
        key = await get_keypress()
        if key == "1":
            clear_console()
            start_widget()
            await show_server_selection()
        elif key == "2":
            clear_console()
            start_widget()
            await select_user()
        elif key == "3":
            clear_console()
            start_widget()
            await select_action()
        else:
            await get_error("Invalid option!")

# - - - - - - - - - - - - - - - - - - - - - -  Profile  - - - - - - - - - - - - - - - - - - - - - - #

async def select_action():
    print(f" {Fore.CYAN}[1] {Fore.WHITE}Change Status")
    print(f" {Fore.CYAN}[2] {Fore.WHITE}Change Name")
    while True:
        key = await get_keypress()
        if key == "1":
            clear_console()
            start_widget()
            await change_status()
        elif key == "2":
            clear_console()
            start_widget()
            await change_name()
        elif key == "!back" or key == "!home":
            clear_console()
            start_widget()
            await select_options()
        else:
            await get_error("Invalid option!")

async def change_status():
    print(f"{Fore.CYAN}INFO {Fore.WHITE}Select your activity mode:")
    print(f"")
    print(f" {Fore.CYAN}[1] {Fore.WHITE}Playing")
    print(f" {Fore.CYAN}[2] {Fore.WHITE}Watching")
    print(f" {Fore.CYAN}[3] {Fore.WHITE}Competing")
    print(f" {Fore.CYAN}[4] {Fore.WHITE}Listening")
    print(f" {Fore.CYAN}[5] {Fore.WHITE}Custom")
    print(f" {Fore.CYAN}[6] {Fore.WHITE}Clear")
    tryb = input(f"")
    if tryb == "!back" or tryb == "!home":
        clear_console()
        start_widget()
        await select_options()
    clear_console()
    start_widget()
    print(f"{Fore.CYAN}INFO {Fore.WHITE} Enter a activity content")
    tresc = input(f"")
    if tresc == "!back" or tresc == "!home":
        clear_console()
        start_widget()
        await select_options()
    if tryb == "1":
        activity = discord.Game(name=tresc)
        await bot.change_presence(activity=activity)
    elif tryb == "2":
        activity = discord.Activity(type=discord.ActivityType.watching, name=tresc)
        await bot.change_presence(activity=activity)
    elif tryb == "3":
        activity = discord.Activity(type=discord.ActivityType.competing, name=tresc)
        await bot.change_presence(activity=activity)
    elif tryb == "4":
        activity = discord.Activity(type=discord.ActivityType.listening, name=tresc)
        await bot.change_presence(activity=activity)
    elif tryb == "5":
        activity = discord.CustomActivity(name=tresc)
        await bot.change_presence(activity=activity)
    elif tryb == "6":
        await bot.change_presence(status=discord.Status.online)
    clear_console()
    start_widget()
    await select_options()
    await get_debug("Status set successfully")

async def change_name():
    print(f"{Fore.CYAN}INFO {Fore.WHITE}You are in the edit view of your bot name")
    print(f"{Fore.CYAN}INFO {Fore.WHITE}Enter a new name for your bot")
    name = input(f"")
    clear_console()
    start_widget()
    print(f"{Fore.CYAN}INFO {Fore.WHITE}You are trying to change your bot's name")
    print(f"{Fore.RED}Old Name: {bot.user.name}")
    print(f"{Fore.GREEN}New Name: {name}")
    print(f"{Fore.CYAN}INFO{Fore.WHITE} Do you want to do this? To confirm, type {Fore.GREEN}O{Fore.WHITE}, to reject {Fore.RED}X{Fore.WHITE}")
    decision = input(f"")
    if decision == "O":
        await bot.user.edit(username=name)
        clear_console()
        start_widget()
        await get_debug(f"The bot name has been changed!")
        await select_options()
    else:
        clear_console()
        start_widget()
        select_action()


# - - - - - - - - - - - - - - - - - - - - - -  DM  - - - - - - - - - - - - - - - - - - - - - - #

async def send_dm(user_id):
    recent_messages = deque(maxlen=10)
    user = await bot.fetch_user(int(user_id))

    async def display_recent_messages():
        clear_console()
        start_widget()
        print(f"{Fore.CYAN}---------------- ChatBox ----------------")
        print(f" {Fore.BLUE}INFO {Fore.WHITE}You chatting with: {user.name}")
        print(f"{Fore.CYAN}---------------- ChatBox ----------------")
        for msg in recent_messages:
            if msg.author.id == bot.user.id:
                print(f" {Fore.BLUE}You: {Fore.WHITE}{msg.content}")
            else:
                print(f" {Fore.BLUE}{msg.author.name}: {Fore.WHITE}{msg.content}")
        print(f"{Fore.CYAN}---------------- ChatBox ----------------")
        print("")
        print(f"{Fore.CYAN}INFO {Fore.WHITE}You are in the DM chatbox, here you can see the chat with the user and send messages.")
        print(f"{Fore.CYAN}INFO {Fore.WHITE}To undo your selection, use !back")

    if not user:
        print(f"{Fore.RED}ERROR {Fore.WHITE}User with ID {user_id} not found.")
        return

    async for message in user.history(limit=10, oldest_first=False):
        recent_messages.appendleft(message)

    await display_recent_messages()

    async def listen_for_new_messages():
        while True:
            await asyncio.sleep(0.5)
            async for message in user.history(limit=1, oldest_first=False):
                if message not in recent_messages:
                    recent_messages.append(message)
                    await display_recent_messages()
                break

    listener_task = asyncio.create_task(listen_for_new_messages())

    try:
        while True:
            message_content = await get_keypress()
            if message_content.lower() == "!back":
                listener_task.cancel()
                clear_console()
                start_widget() 
                await select_user()
            elif message_content.lower() == "!home":
                listener_task.cancel()
                clear_console()
                start_widget() 
                await select_options()
            elif message_content.lower() == "!refresh":
                await display_recent_messages()
            elif message_content.lower() == "!help":
                await display_recent_messages()
                print(" ")
                print(f"{Fore.YELLOW}MSG {Fore.WHITE}!help - View the help view (this view)")
                print(f"{Fore.YELLOW}MSG {Fore.WHITE}!back - Go back to previous view")
                print(f"{Fore.YELLOW}MSG {Fore.WHITE}!home - Go to the home view")
                print(f"{Fore.YELLOW}MSG {Fore.WHITE}!delete - Delete the last message you sent")
                print(f"{Fore.YELLOW}MSG {Fore.WHITE}!info - View information about last message")
                print(f"{Fore.YELLOW}MSG {Fore.WHITE}!refresh - Refresh the chatbox")
                print(f"{Fore.YELLOW}MSG {Fore.WHITE}!pin - Pin the last message")
                print(f"{Fore.YELLOW}MSG {Fore.WHITE}!unpin - Unpin the last pinned message")
                print(f"{Fore.YELLOW}MSG {Fore.WHITE}!reaction [emoji] - React to the last message with the specified emoji")
                print(f"{Fore.YELLOW}MSG {Fore.WHITE}!reply [messge_id] [message_content] - Reply to a message with the specified content")
            elif message_content.lower() == "!delete":
                print(" ")
                if recent_messages and recent_messages[-1].author.id == bot.user.id:
                    try:
                        await recent_messages[-1].delete()
                        recent_messages.pop()
                        print(f"{Fore.YELLOW}MSG {Fore.WHITE}Last message deleted successfully.")
                    except Exception as e:
                        print(f"{Fore.RED}ERROR {Fore.WHITE}Failed to delete the last message: {e}")
                else:
                    print(f"{Fore.RED}ERROR {Fore.WHITE}No message to delete or last message was not sent by you.")
            elif message_content.lower() == "!info":
                print(" ")
                if recent_messages:
                    last_message = recent_messages[-1]
                    print(f"{Fore.YELLOW}MSG {Fore.WHITE}Last message details:")
                    print(f"{Fore.YELLOW}MSG {Fore.WHITE}Author: {last_message.author.name}")
                    print(f"{Fore.YELLOW}MSG {Fore.WHITE}Content: {last_message.content}")
                    print(f"{Fore.YELLOW}MSG {Fore.WHITE}Sent at: {last_message.created_at}")
                    print(f"{Fore.YELLOW}MSG {Fore.WHITE}ID: {last_message.id}")
                    print(f"{Fore.YELLOW}MSG {Fore.WHITE}URL: {last_message.jump_url}")
                else:
                    print(f"{Fore.RED}ERROR {Fore.WHITE}No messages available.")
            elif message_content.lower() == "!pin":
                print(" ")
                if recent_messages:
                    try:
                        await recent_messages[-1].pin()
                        print(f"{Fore.YELLOW}MSG {Fore.WHITE}Message pinned successfully.")
                    except Exception as e:
                        print(f"{Fore.RED}ERROR {Fore.WHITE}Failed to pin the message: {e}")
                else:
                    print(f"{Fore.RED}ERROR {Fore.WHITE}No messages available to pin.")
            elif message_content.lower() == "!unpin":
                print(" ")
                try:
                    pinned_messages = await user.pins()
                    if pinned_messages:
                        await pinned_messages[-1].unpin()
                        print(f"{Fore.YELLOW}MSG {Fore.WHITE}Last pinned message unpinned successfully.")
                    else:
                        print(f"{Fore.RED}ERROR {Fore.WHITE}No pinned messages to unpin.")
                except Exception as e:
                    print(f"{Fore.RED}ERROR {Fore.WHITE}Failed to unpin the message: {e}")
            elif message_content.lower().startswith("!reaction"):
                print(" ")
                emoji = message_content.split(maxsplit=1)[1] if len(message_content.split()) > 1 else None
                if emoji and recent_messages:
                    try:
                        await recent_messages[-1].add_reaction(emoji)
                        print(f"{Fore.YELLOW}MSG {Fore.WHITE}Reaction {emoji} added successfully to the last message.")
                    except Exception as e:
                        print(f"{Fore.RED}ERROR {Fore.WHITE}Failed to add reaction: {e}")
                else:
                    print(f"{Fore.RED}ERROR {Fore.WHITE}Invalid command or no messages available to react to. Use !reaction emoji.")
            elif message_content.lower().startswith("!reply"):
                parts = message_content.split(maxsplit=2)
                if len(parts) == 3:
                    message_id, reply_content = parts[1], parts[2]
                    try:
                        message_to_reply = await user.fetch_message(int(message_id))
                        await message_to_reply.reply(reply_content)
                        print(f"{Fore.YELLOW}MSG {Fore.WHITE}Replied successfully to message {message_id}.")
                    except Exception as e:
                        print(f"{Fore.RED}ERROR {Fore.WHITE}Failed to reply: {e}")
                else:
                    print(f"{Fore.RED}ERROR {Fore.WHITE}Invalid command format. Use !reply id message.")
            else:
                try:
                    sent_message = await user.send(message_content, view=InfoButtom())
                    recent_messages.append(sent_message)
                    await display_recent_messages()
                except Exception as e:
                    print(f"{Fore.RED}ERROR {Fore.WHITE}Failed to send the message: {e}")
    except Exception as e:
        await get_error(e)
        listener_task.cancel()

async def select_user():
    print(f"{Fore.CYAN}INFO {Fore.WHITE}Enter the recipient ID or @nickname of the DM message.")
    print(f"{Fore.CYAN}INFO {Fore.WHITE}The user must share at least one server with the bot, or have started a conversation.")
    while True:
        input_value = await get_keypress()
        if input_value == "!back" or input_value == "!home":
            clear_console()
            start_widget()
            await select_options()
        try:
            user_id = await get_user_id_or_nick(input_value, bot)
            await send_dm(user_id)
        except ValueError:
            await get_error("Invalid input!")



# - - - - - - - - - - - - - - - - - - - - - -  Servers  - - - - - - - - - - - - - - - - - - - - - - #

async def show_server_selection():
    servers = list(bot.guilds)
    print(f"{Fore.CYAN}INFO {Fore.WHITE}Select the server you want to view")
    print(f"{Fore.CYAN}INFO {Fore.WHITE}To undo your selection, use !back")
    print("")

    for idx, guild in enumerate(servers):
        print(f" {Fore.CYAN}[{idx + 1}] {Fore.WHITE}{guild.name}")


    try:
        while True:
            key = await get_keypress()
            if key.isdigit() and 1 <= int(key) <= len(servers):
                selected_guild = servers[int(key) - 1]
                clear_console()
                start_widget()
                await show_channel_selection(selected_guild)
            else:
                if key == "!back" or key == "!home":
                    clear_console()
                    start_widget()
                    await select_options()

    except Exception as e:
        await get_error(e)

async def show_channel_selection(guild):
    channels = sorted(
        [channel for channel in guild.channels if isinstance(channel, discord.TextChannel)],
        key=lambda c: c.position
    )

    for idx, channel in enumerate(channels):
        print(f" {Fore.CYAN}[{idx + 1}] {Fore.WHITE}{channel.name}")

    print("")
    print(f"{Fore.CYAN}INFO {Fore.WHITE}Select the channel you want to view")
    print(f"{Fore.CYAN}INFO {Fore.WHITE}To undo your selection, use !back")
    print("")
    try:
        while True:
            key = await get_keypress()
            if key.isdigit() and 1 <= int(key) <= len(channels):
                selected_channel = channels[int(key) - 1]
                await send_message(selected_channel)
                break
            else:
                if key == "!back":
                    clear_console()
                    start_widget()
                    await show_server_selection()
                elif key == "!home":
                    clear_console()
                    start_widget()
                    await select_options()
                elif key == "!leave":
                    await guild.leave()
                    clear_console()
                    start_widget()
                    await show_server_selection()
                    



    except Exception as e:
        await get_error(e)

async def send_message(channel):
    recent_messages = deque(maxlen=10)

    async def display_recent_messages():
        clear_console()
        start_widget()
        print(f"{Fore.CYAN}---------------- ChatBox ----------------")
        for msg in recent_messages:
            if msg.author.name == bot.user.name:
                print(f" {Fore.BLUE}You: {Fore.WHITE}{msg.content}")
            else:
                print(f" {Fore.BLUE}{msg.author.name}: {Fore.WHITE}{msg.content}")
        print(f"{Fore.CYAN}---------------- ChatBox ----------------")
        print("")
        print(f"{Fore.CYAN}INFO {Fore.WHITE}You are in the chatbox, here you can see the chat from the selected channel and you can send messages.")
        print(f"{Fore.CYAN}INFO {Fore.WHITE}To undo your selection, use !back")

    async for message in channel.history(limit=10, oldest_first=False):
        recent_messages.appendleft(message)

    await display_recent_messages()

    async def listen_for_new_messages():
        while True:
            await asyncio.sleep(0.5)
            async for message in channel.history(limit=1, oldest_first=False):
                if message not in recent_messages:
                    recent_messages.append(message)
                    await display_recent_messages()
                break

    listener_task = asyncio.create_task(listen_for_new_messages())

    try:
        while True:
            message = await get_keypress()
            if message.lower() == "!back":
                listener_task.cancel()
                clear_console()
                start_widget()
                await show_channel_selection(channel.guild)
                break
            elif message.lower() == "!home":
                listener_task.cancel()
                clear_console()
                start_widget()
                await select_options()
                break
            elif message.lower() == "!refresh":
                await display_recent_messages()
            elif message.lower() == "!help":
                await display_recent_messages()
                print(" ")
                print(f"{Fore.YELLOW}MSG {Fore.WHITE}!help - View the help view (this view)")
                print(f"{Fore.YELLOW}MSG {Fore.WHITE}!back - Go back to previous view")
                print(f"{Fore.YELLOW}MSG {Fore.WHITE}!home - Go to the home view")
                print(f"{Fore.YELLOW}MSG {Fore.WHITE}!delete - Delete the last message you sent")
                print(f"{Fore.YELLOW}MSG {Fore.WHITE}!info - View information about last message")
                print(f"{Fore.YELLOW}MSG {Fore.WHITE}!refresh - Refresh the chatbox")
                print(f"{Fore.YELLOW}MSG {Fore.WHITE}!pin - Pin the last message")
                print(f"{Fore.YELLOW}MSG {Fore.WHITE}!unpin - Unpin the last pinned message")
                print(f"{Fore.YELLOW}MSG {Fore.WHITE}!reaction [emoji] - React to the last message with the specified emoji")
                print(f"{Fore.YELLOW}MSG {Fore.WHITE}!reply [message_id] [message_content] - Reply to a message with the specified content")
            elif message.lower() == "!delete":
                print(" ")
                if recent_messages and recent_messages[-1].author.id == bot.user.id:
                    try:
                        await recent_messages[-1].delete()
                        recent_messages.pop()
                        print(f"{Fore.YELLOW}MSG {Fore.WHITE}Last message deleted successfully.")
                    except Exception as e:
                        print(f"{Fore.RED}ERROR {Fore.WHITE}Failed to delete the last message: {e}")
                else:
                    print(f"{Fore.RED}ERROR {Fore.WHITE}No message to delete or last message was not sent by you.")
            elif message.lower() == "!info":
                print(" ")
                if recent_messages:
                    last_message = recent_messages[-1]
                    print(f"{Fore.YELLOW}MSG {Fore.WHITE}Last message details:")
                    print(f"{Fore.YELLOW}MSG {Fore.WHITE}Author: {last_message.author.name}")
                    print(f"{Fore.YELLOW}MSG {Fore.WHITE}Content: {last_message.content}")
                    print(f"{Fore.YELLOW}MSG {Fore.WHITE}Sent at: {last_message.created_at}")
                    print(f"{Fore.YELLOW}MSG {Fore.WHITE}ID: {last_message.id}")
                    print(f"{Fore.YELLOW}MSG {Fore.WHITE}URL: {last_message.jump_url}")
                else:
                    print(f"{Fore.RED}ERROR {Fore.WHITE}No messages available.")
            elif message.lower() == "!pin":
                print(" ")
                if recent_messages:
                    try:
                        await recent_messages[-1].pin()
                        print(f"{Fore.YELLOW}MSG {Fore.WHITE}Message pinned successfully.")
                    except Exception as e:
                        print(f"{Fore.RED}ERROR {Fore.WHITE}Failed to pin the message: {e}")
                else:
                    print(f"{Fore.RED}ERROR {Fore.WHITE}No messages available to pin.")
            elif message.lower() == "!unpin":
                print(" ")
                try:
                    pinned_messages = await channel.pins()
                    if pinned_messages:
                        await pinned_messages[-1].unpin()
                        print(f"{Fore.YELLOW}MSG {Fore.WHITE}Last pinned message unpinned successfully.")
                    else:
                        print(f"{Fore.RED}ERROR {Fore.WHITE}No pinned messages to unpin.")
                except Exception as e:
                    print(f"{Fore.RED}ERROR {Fore.WHITE}Failed to unpin the message: {e}")
            elif message.lower().startswith("!reaction"):
                print(" ")
                emoji = message.split(maxsplit=1)[1] if len(message.split()) > 1 else None
                if emoji and recent_messages:
                    try:
                        await recent_messages[-1].add_reaction(emoji)
                        print(f"{Fore.YELLOW}MSG {Fore.WHITE}Reaction {emoji} added successfully to the last message.")
                    except Exception as e:
                        print(f"{Fore.RED}ERROR {Fore.WHITE}Failed to add reaction: {e}")
                else:
                    print(f"{Fore.RED}ERROR {Fore.WHITE}Invalid command or no messages available to react to. Use !reaction emoji.")
            elif message.lower().startswith("!reply"):
                print(" ")
                parts = message.split(maxsplit=2)
                if len(parts) == 3:
                    message_id, reply_content = parts[1], parts[2]
                    try:
                        message_to_reply = await channel.fetch_message(int(message_id))
                        await message_to_reply.reply(reply_content)
                        print(f"{Fore.YELLOW}MSG {Fore.WHITE}Replied successfully to message {message_id}.")
                    except Exception as e:
                        print(f"{Fore.RED}ERROR {Fore.WHITE}Failed to reply: {e}")
                else:
                    print(f"{Fore.RED}ERROR {Fore.WHITE}Invalid command format. Use !reply id message.")
            else:
                try:
                    sent_message = await channel.send(message, view=InfoButtom())
                    recent_messages.append(sent_message)
                    await display_recent_messages()
                except Exception as e:
                    print(f"{Fore.RED}ERROR {Fore.WHITE}Failed to send the message: {e}")
    except Exception as e:
        await get_error(e)
        listener_task.cancel()

@bot.event
async def on_guild_join(guild):
    bot_member = guild.get_member(bot.user.id)
    if bot_member and bot_member.guild_permissions.administrator:
        await get_debug(f"Joined new server: {guild.name} - Bot has admin rights.")
    else:
        clear_console()
        start_widget()
        await get_error(f"Joined new server: {guild.name} - Bot does NOT have admin rights.")
        

@bot.event
async def on_ready():
        try:
            clear_console()
            start_widget()
            await get_debug(f"Logged in as {bot.user}")
            required_intents = ["messages", "guilds", "members"]
            missing_intents = [intent for intent in required_intents if not getattr(intents, intent, False)]
            if missing_intents:
                await get_debug(f"Missing intents: {', '.join(missing_intents)}")
                pass

            for guild in bot.guilds:
                bot_member = guild.get_member(bot.user.id)
                if bot_member.guild_permissions.administrator:
                    continue
                else:
                    await get_error(f"Bot does NOT have admin rights on server: {guild.name}")
                    pass
            try:
                if STATUS_MODE == "Play":
                    activity = discord.Game(name=STATUS_CONTENT)
                    await bot.change_presence(activity=activity)
                elif STATUS_MODE == "Watch":
                    activity = discord.Activity(type=discord.ActivityType.watching, name=STATUS_CONTENT)
                    await bot.change_presence(activity=activity)
                elif STATUS_MODE == "Compet":
                    activity = discord.Activity(type=discord.ActivityType.competing, name=STATUS_CONTENT)
                    await bot.change_presence(activity=activity)
                elif STATUS_MODE == "Listen":
                    activity = discord.Activity(type=discord.ActivityType.listening, name=STATUS_CONTENT)
                    await bot.change_presence(activity=activity)
                elif STATUS_MODE == "Custom":
                    activity = discord.CustomActivity(name=STATUS_CONTENT)
                    await bot.change_presence(activity=activity)
                elif STATUS_MODE == "None":
                    await bot.change_presence(status=discord.Status.online)
                else:
                    pass
                await get_debug(f"Status has been setted")
            except Exception as e:
                await get_error("Problem with set a activity!")
            await select_options()
        except Exception as e:
            await get_error(f"{str(e)}")

if LIBRUARY_STATUS == "ON":
    with open(LIBRUARY_PATH, "r") as config_file:
        preset = json5.load(config_file)
    try:
        LIBRUARY_PRESET = config.get("libruary_preset")
        TOKEN = preset.get(LIBRUARY_PRESET)
    except Exception as e:
        clear_console()
        start_widget()
        print(f"{Fore.RED}ERROR{Fore.WHITE} Problem with import a token from TokenLibruary")
else:
    TOKEN = config.get("token")

try:
    if TOKEN == "Your Token":
        start_widget()
        print(f"{Fore.YELLOW} WARN{Fore.WHITE} You forgot to configure the program in the config.json5 file! If you don't know how to do this, read the documentation available on our github!")
    else:
        bot.run(TOKEN)
except Exception as e:
    start_widget()
    print(f"{Fore.RED}ERROR {Fore.WHITE} There was a problem starting the bot. Check the correctness of the token in the config!")
    print(f"{Fore.YELLOW}TIP{Fore.WHITE} Check if the template was created correctly in the library and imported correctly in the config")
