# Bot Command List

## `?translate <lang_code> <text>`
Translates the provided text into the specified language.

- **`<lang_code>`**: The language code for the target language. For example, `es` for Spanish, `fr` for French. See the [Supported Languages](#supported-languages) section for a list of valid language codes.
- **`<text>`**: The text you want to translate.

### Example:
`?translate es Hello, how are you?`  
*Translates "Hello, how are you?" into Spanish.*

---

## `?search <lang>`
Find the language code for a specified language.

- **`<lang>`**: The language you want to find its code.

### Example:
`?search Spanish`  
*Returns the language code for Spanish.*

---

## `?languages`
Lists all available languages with their corresponding language codes.

### Example:
`?languages`  
*Displays a paginated list of supported languages.*

---

## `?warn <user_id> <warning_message>`
Sends a warning message to the specified user via DM.

- **`<@user>`**: The user you want to send a warning to.
- **`<warning_message>`**: The message content of the warning.

### Example:
`?warn @JohnDoe Please follow the server rules!`  
*Sends a warning to John Doe with the message: "Please follow the server rules!"*

---

## `?setup`
Sets up reaction roles in a specified channel. You will be prompted to provide the message, emojis, and roles for the reaction system.

### Example:
`?setup #roles-channel`  
*Initiates the reaction role setup in the specified channel.*

---

## `?help`
Sends this list of commands to the user.

### Example:
`?help`  
*Sends a DM with a list of all available commands.*
