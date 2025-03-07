# Telegram Link Resolver

A Python script to resolve Telegram invite links (t.me URLs) to their corresponding channel IDs. This is useful for collecting channel IDs for further analysis or monitoring.

## Requirements

- Python 3.7+
- A Telegram account
- Telegram API credentials (instructions below)

## Setup Instructions

1. **Install required packages**:

   ```bash
   pip install telethon python-dotenv
   ```

2. **Get Telegram API Credentials**:

   - Visit [https://my.telegram.org/apps](https://my.telegram.org/apps) and log in with your Telegram account
   - Create a new application if you don't have one already
   - You'll receive an `API_ID` (numbers) and `API_HASH` (alphanumeric string)
   - Keep these credentials secure and never share them publicly!

3. **Create a .env file**:

   Create a file named `.env` in the same directory as the script with the following content:

   ```
   API_ID=your_api_id_here
   API_HASH=your_api_hash_here
   ```

   Replace `your_api_id_here` and `your_api_hash_here` with the credentials you obtained in step 2.

4. **Create a links file**:

   Create a text file containing the Telegram invite links you want to resolve, one per line. For example:
   
   ```
   https://t.me/channel_name
   https://t.me/joinchat/INVITE_CODE
   ```

## Usage

Run the script using Python:

```bash
python telegram_link_resolver.py path_to_links_file.txt
```

## First Run Authentication

The first time you run the script, you'll need to authenticate with your Telegram account:

1. The script will prompt you to enter your phone number with country code (e.g., +1234567890)
2. Telegram will send a verification code to your Telegram app
3. Enter this code when prompted by the script

After successful authentication, a session file will be created, and you won't need to authenticate again unless you delete the session file or run the script from a different location.

## Output

The script provides two types of output:

1. Detailed results showing each link and its corresponding channel ID and title
2. A list of just the channel IDs, which can be redirected to a file if needed

## Security Notes

- The session file contains sensitive information. Keep it secure.
- Never share your API credentials or session file with others.
- Consider adding `.env` and `*.session` to your `.gitignore` if using version control.

## Troubleshooting

- If you encounter rate limiting errors, increase the delay between requests by modifying the `await asyncio.sleep(1)` line.
- Some invite links may be expired or invalid, which will result in error messages.
- If you're unable to authenticate, make sure your phone number is entered correctly and that your Telegram account is active. 