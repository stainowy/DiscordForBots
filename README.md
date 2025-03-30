# Discord For Bots

**Discord For Bots** is an unofficial open-source application.  
With **Discord For Bots**, you can use Discord just like an application!

---

## Getting Started

> It's very simple!  
> Follow these steps:
1. Create an application on the [Discord Developer Portal](https://discord.com/developers/applications).
2. Grant the bot all three required intents.
3. Generate a token and add the bot to a server with Administrator permissions.
4. Download the program files from this GitHub repository.
5. Paste the bot token into the configuration file.  
   That's it! Now you can run the program.

---

## How Does It Work?

> **Discord For Bots** allows you to interact with Discord as if it were an application.  
> Once you open the app and provide the token, you'll gain access to several features:  
> - Browsing servers
> - Sending DMs
> - Editing profiles
> - And much more!  
> Everything is preconfigured for you, so you don’t need to adjust anything further.  

> In every view, you can use the `!help` command to display available commands or `!back` to go back to the previous view.

---

## Configuration

> The program doesn’t require additional configuration beyond entering the bot token, but if you want to customize it, here's how:

**config.json5**:
```json5
{
  "token": "YourBotToken",
  
  // Token Library Config
  "library_status": "OFF", // ON or OFF
  "library_path": "tokenLibrary.json5", // This file, must be json5 file
  "library_preset": "token",

  // Optional settings, default is recommended settings
  "prefix": "dfb.", // Custom prefix, max 5 characters
  "debug": "ON", // ON or OFF
  "commands": "ON", // ON or OFF
  "ping": "ON", // ON or OFF

  "status_mode": "Play", // Play, Watch, Compete, Listen, Custom or None
  "status_content": "Discord For Bots"
}
```

- `token`: The bot's token.
- `library_status`: Enables or disables the token library.
- `library_path`: Path to the token library file.
- `library_preset`: Name of the token preset in the library.
- `prefix`: The bot's prefix (max 5 characters).
- `debug`: Enables or disables debugging.
- `commands`: Determines whether the bot responds to commands.
- `ping`: Determines whether the bot responds to pings.
- `status_mode`: The bot's default activity mode.
- `status_content`: The bot's default activity content.

---

## What Is TokensLibrary?

> The token library is where you can store tokens for bots you want to use in Discord For Bots.  
> Instead of pasting the token directly, you can refer to a preset name in the configuration file.

**tokenLibrary.json5**:
```json5
{
    "token": "YourToken",
    "token2": "YourToken2"
}

// ---------------------------------------------------------------------
// Token library is a place where you can store your tokens under some name, 
// and import them in config by that name, rather than pasting the token.
// Remember to copy the templates exactly: ' "name": "token", '
// ---------------------------------------------------------------------
```

To create a new preset, just add another line like `"name": "token"`.

---

## Acknowledgments

> - Special thanks to [@graynix](https://github.com/graynixx) for testing the program and reporting bugs.  
> - Special thanks to [@tomusiek](https://github.com/tomusiek) for the project idea.

❤ Made with love by [@stainowy](https://github.com/stainowy)
