# DISCORD ASSISTANCE BOT
#### Video Demo: https://youtu.be/WFYFUc28Sqw
#### Description: 

This is discord bot made to for general assitant for discord server design easy to use with multiple useful commands that many might have but might need different  bots so I made this bot to make everything in this bot as possible.

# Installation
discord>=2.3.2,<2.4.0  
https://github.com/Rapptz/discord.py
python-dotenv>=1.0.1,<1.1.0  
https://github.com/theskumar/python-dotenv
Languages>=1.4.0,<1.5.0  
https://github.com/aswanthabam/Language
Flask>=3.0.3,<3.1.0  
https://github.com/pallets/flask/
python-Levenshtein>=0.25.1,<0.26.0  
https://github.com/rapidfuzz/python-Levenshtein
pillow>=10.4.0,<10.5.0  
https://github.com/python-pillow/Pillow
requests>=2.32.3,<2.33.0  
https://github.com/psf/requests
deep-translator>=1.11.4,<1.12.0  
https://github.com/nidhaloff/deep_translator
PIL>=1.1.6,<1.2.0  
http://www.pythonware.com/products/pil

# Discord Bot Features

### 1. **Bot Initialization**
- **Environment Configuration**: The bot loads the `DISCORD_TOKEN` from a `.env` file to ensure sensitive information is protected. 
- **Command Prefix**: All commands are prefixed with `?` for simplicity.
- **Webserver**: This bot use Flask as a server which is not intend for the production and meant for development only
---

### 2. **Commands**

#### A. Search Language Code (`?search <language>`)
- Allows users to fetch the ISO language code for a given language.
- Example: `?search Spanish` returns `es`.
- Ideal for users looking to translate text into different languages.

#### B. Translate Text (`?translate <lang_code> <text>`)
- Translates a provided text snippet into the specified language.
- Supports aliases (`?tr` and `?trans`) to make the command more accessible.
- Example: `?translate es Hello, world!` translates "Hello, world!" into Spanish.

#### C. List All Languages (`?languages`)
- Displays a paginated list of all available languages and their codes.
- Supports aliases (`?lang`) to make the command more accessible.
- Uses interactive buttons for navigation, making it user-friendly and easy to browse.
- Supports dynamic page updates and ensures that users can navigate seamlessly.

#### D. Custom Help Command (`?help`)
- Sends a direct message to the user containing a list of all available commands.
- Loads help content from a markdown file (`help.md`), allowing for easy updates and detailed documentation.
- Notifies the user if direct messages are disabled, ensuring clear communication.

#### E. Send Warning (`?warn <user_id> <text>`)
- Sends a private warning message to a user via direct message.
- Designed for administrators to maintain community standards.
- Includes validation for user IDs and ensures that proper permissions are upheld.

#### F. Reaction Roles Setup (`?setup <channel>`)
- Guides administrators through a process to set up reaction roles in a specified channel.
- Prompts for the message content, emojis, and corresponding roles.
- Automatically updates a `role.json` file for role configurations.
- Simplifies the management of self-assigned roles within a server.

---

### 3. **Reaction Role Events**

#### A. Add Reaction (`on_raw_reaction_add`)
- Automatically assigns roles to users when they react to a specific message.
- Handles both Unicode and custom emojis for maximum flexibility.
- Verifies permissions and role hierarchy to ensure seamless role assignment.

#### B. Remove Reaction (`on_raw_reaction_remove`)
- Removes roles from users when they remove their reaction from a configured message.
- Maintains server organization by dynamically updating user roles based on their actions.

---



