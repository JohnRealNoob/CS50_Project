import os
import asyncio
from dotenv import load_dotenv
import discord  
from discord.ext import commands
from discord.ui import Button, View
import json
from functions import translate_text, search_language_code, list_all_languages, load_help_info
import websever

# Set up intents
intents = discord.Intents.default()
intents.message_content = True

# Initialize the bot
bot = commands.Bot(command_prefix='?', intents=intents)

# Load environment variables
# Using .env file
load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")  # Direct assignment

# Event: Bot is ready
@bot.event
async def on_ready():
    print(f'We have logged in as {bot.user}')

# Command: Search Language Code
@bot.command()
async def search(ctx, lang):
    lang_code = search_language_code(lang)
    await ctx.send(lang_code)

# Command: Translate Languages
@bot.command(aliases=['tr', 'trans'])
async def translate(ctx, lang_code: str, *, text: str):
    """
    Translates the given text into the specified language.

    Parameters:
    lang_code (str): The target language code (e.g., 'es' for Spanish, 'fr' for French).
    text (str): The sentence or text to translate.
    """
    # Call the translate_text function from the imported file
    result = translate_text(lang_code, text)

    # Send the result as a message
    await ctx.send(result)


# Command: List All Available Language
@bot.command(aliases=['lang'])
async def languages(ctx):
    """
    Sends a paginated, compact list of available languages and their codes in an embedded black box with buttons for navigation.
    """
    current_page = 0
    items_per_page = 10
    page_content, total_pages = list_all_languages(current_page, items_per_page)
    
    embed = discord.Embed(
        title="Available Languages",
        description=f"{page_content}",
        color=discord.Color.dark_gray()
    )
    embed.set_footer(text=f"Page {current_page + 1}/{total_pages}")
    
    # Define buttons for navigation
    prev_button = Button(label="Previous", style=discord.ButtonStyle.primary)
    next_button = Button(label="Next", style=discord.ButtonStyle.primary)
    
    # Define a callback for the "Previous" button
    async def prev_button_callback(interaction):
        nonlocal current_page
        if current_page > 0:
            current_page -= 1
            page_content, _ = list_all_languages(current_page, items_per_page)
            embed.description = f"{page_content}"
            embed.set_footer(text=f"Page {current_page + 1}/{total_pages}")
            await interaction.response.edit_message(embed=embed, view=view)

    # Define a callback for the "Next" button
    async def next_button_callback(interaction):
        nonlocal current_page
        if current_page < total_pages - 1:
            current_page += 1
            page_content, _ = list_all_languages(current_page, items_per_page)
            embed.description = f"{page_content}"
            embed.set_footer(text=f"Page {current_page + 1}/{total_pages}")
            await interaction.response.edit_message(embed=embed, view=view)
    
    # Attach callbacks to buttons
    prev_button.callback = prev_button_callback
    next_button.callback = next_button_callback
    
    # Create a view with the buttons
    view = View()
    view.add_item(prev_button)
    view.add_item(next_button)
    
    # Send the initial message with the embed and the view (buttons)
    await ctx.send(embed=embed, view=view)

# Command: Send all command list in DM

bot.remove_command('help')

@bot.command(name="help")
async def custom_help(ctx):
    """Sends a DM to the user with a list of all bot commands."""
    help_info = load_help_info('help.md') 

    embed = discord.Embed(
        title="", 
        description=help_info,
        color=discord.Color.blue()
    )

    # Set a footer to give context if needed
    embed.set_footer(text="For more information, visit our github.")

    try:
        await ctx.author.send(embed=embed)
        await ctx.send(f"Sent you a DM with the help information!")
    except discord.Forbidden:
        await ctx.send("I can't DM you. Please make sure your DMs are open.")
    except Exception as e:
        await ctx.send(f"An error occurred: {e}")

# Command: Send warning DM to user.
@bot.command()
@commands.has_permissions(administrator=True)  # Optional: restrict to admins
async def warn(ctx, user_id: int = None, *, warning_text: str = None):
    """
    Sends a warning message to the specified user via DM using their user ID.
    
    Parameters:
    user_id (int): The ID of the user to send the DM to. Defaults to None.
    warning_text (str): The warning message to send. Defaults to None.
    """

    usage_message = (
        "You must provide both the user ID and the warning message. "
        "Usage: `!warn <user_id> <warning_text>`"
    )
    
    # Check if any arguments are missing
    if not user_id or not warning_text:
        await ctx.send(usage_message)
        return

    try:
        # Try to fetch the member from the guild
        member = ctx.guild.get_member(user_id)
        
        if member is None:
            # If not found, try to fetch the user from cache
            member = bot.get_user(user_id)
        
        if member is None:
            # If the user is not in the cache, fetch them from Discord directly
            member = await bot.fetch_user(user_id)
        
        if member is None:
            await ctx.send(f"User with ID {user_id} not found.")
            return
        
        # Create an embed message
        embed = discord.Embed(
            title="Warning",
            description=warning_text,
            color=discord.Color.red()
        )

        # Send the DM
        await member.send(embed=embed)

        # Notify the command invoker
        await ctx.send(f"Warning message sent to {member.name}.")
    except discord.Forbidden:
        await ctx.send(f"Unable to send a DM to {member.name}. They might have DMs disabled.")
    except Exception as e:
        await ctx.send(f"An error occurred: {e}")

# Command: Set up reaction roles.
@bot.command()
@commands.has_permissions(administrator=True)
async def setup(ctx, channel: discord.TextChannel):
    await ctx.send(f"Setting up reaction roles in {channel.mention}...")

    questions = ["Enter Message: ", "Enter Emojis: ", "Enter Roles: "]
    answers = []

    def check(user):
        return user.author == ctx.author and user.channel == ctx.channel

    for question in questions:
        await ctx.send(question)

        try:
            msg = await bot.wait_for('message', timeout=240.0, check=check)
        except asyncio.TimeoutError:
            await ctx.send("Time Out")
            return
        else:
            answers.append(msg.content)

    # Split answers into emojis and roles
    emojis = answers[1].split(" ")
    roles = answers[2].split(" ")

    # Send message to set up reaction roles
    bot_msg = await channel.send(answers[0])

    # Open and load the role.json file
    with open("role.json", "r") as f:
        role_data = json.load(f)  # Changed variable name to avoid overwriting roles

    role_data[str(bot_msg.id)] = {"emojis": emojis, "roles": roles}

    # Write the updated data back to the role.json file
    with open("role.json", "w") as f:
        json.dump(role_data, f)

    # Add reactions to the message
    for emoji in emojis:
        try:
            # Add reaction with either Unicode or custom emoji
            custom_emoji = discord.utils.get(ctx.guild.emojis, name=emoji.strip(':'))
            if custom_emoji:
                await bot_msg.add_reaction(custom_emoji)
            else:
                await bot_msg.add_reaction(emoji)  # Unicode emoji
        except Exception as e:
            await ctx.send(f"Failed to add reaction for {emoji}: {str(e)}")

@bot.event
async def on_raw_reaction_add(payload):
    msg_id = payload.message_id

    # Load the roles and emojis from role.json
    with open("role.json", "r") as f:
        self_roles = json.load(f)
    
    # Ignore bot reactions
    if payload.member.bot:
        return
    
    # Check if the message ID is in the JSON data
    if str(msg_id) in self_roles:
        emojis = self_roles[str(msg_id)]['emojis']
        roles = self_roles[str(msg_id)]['roles']

        # Get the guild object
        guild = bot.get_guild(payload.guild_id)

        # Loop through emojis to match the reaction
        for i in range(len(emojis)):
            choosed_emoji = str(payload.emoji)
            expected_emoji = emojis[i]

            # Check for custom emoji or unicode emoji match
            if choosed_emoji == expected_emoji or (payload.emoji.id and f"<:{payload.emoji.name}:{payload.emoji.id}>" == expected_emoji):
                selected_role = roles[i]
                role = discord.utils.get(guild.roles, name=selected_role)

                # Assign the role to the member
                if role:
                    # Check if bot has permission and role hierarchy allows it
                    if guild.me.top_role <= role:
                        await payload.member.send(f"Cannot assign role {selected_role}: the role is higher than my highest role.")
                    elif not guild.me.guild_permissions.manage_roles:
                        await payload.member.send(f"I don't have permission to manage roles.")
                    else:
                        await payload.member.add_roles(role)
                        await payload.member.send(f"You have been assigned the {selected_role} role!")
                else:
                    await payload.member.send(f"Role '{selected_role}' not found.")
                break

@bot.event
async def on_raw_reaction_remove(payload):
    msg_id = payload.message_id

    # Load the roles and emojis from role.json
    with open("role.json", "r") as f:
        self_roles = json.load(f)

    # Get the guild object
    guild = bot.get_guild(payload.guild_id)
    
    if guild is None:
        return

    # Fetch the member from the guild using the user ID
    member = guild.get_member(payload.user_id)

    # If the member is not cached, fetch it
    if member is None:
        member = await guild.fetch_member(payload.user_id)

    # Ignore bot reactions
    if member.bot:
        return

    # Check if the message ID is in the JSON data
    if str(msg_id) in self_roles:
        emojis = self_roles[str(msg_id)]['emojis']
        roles = self_roles[str(msg_id)]['roles']

        # Loop through emojis to match the reaction
        for i in range(len(emojis)):
            choosed_emoji = str(payload.emoji)
            expected_emoji = emojis[i]

            # Check for custom emoji or unicode emoji match
            if choosed_emoji == expected_emoji or (payload.emoji.id and f"<:{payload.emoji.name}:{payload.emoji.id}>" == expected_emoji):
                selected_role = roles[i]
                role = discord.utils.get(guild.roles, name=selected_role)

                # Remove the role from the member
                if role:
                    if guild.me.top_role <= role:
                        await member.send(f"Cannot remove role {selected_role}: the role is higher than my highest role.")
                    elif not guild.me.guild_permissions.manage_roles:
                        await member.send(f"I don't have permission to manage roles.")
                    else:
                        await member.remove_roles(role)
                        await member.send(f"The {selected_role} role has been removed.")
                else:
                    await member.send(f"Role '{selected_role}' not found.")
                break

websever.keep_alive()

# Run the bot
bot.run(TOKEN)