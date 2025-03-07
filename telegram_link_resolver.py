import os
import sys
import asyncio
import logging
from telethon import TelegramClient, functions
from dotenv import load_dotenv

# Configure logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
logger = logging.getLogger(__name__)

# Load environment variables from .env file
load_dotenv()

# ============================================================================
# TELEGRAM CREDENTIALS SETUP
# ============================================================================
# To use this script, you need to:
# 1. Visit https://my.telegram.org/apps and log in with your Telegram account
# 2. Create a new application if you don't have one already
# 3. You'll receive an API_ID (numbers) and API_HASH (alphanumeric string)
# 4. Create a .env file in the same directory as this script with:
#    API_ID=your_api_id_here
#    API_HASH=your_api_hash_here
#
# SECURITY NOTE: Never share your API credentials publicly or commit them to 
# version control. The .env file should be in your .gitignore.
# ============================================================================

API_ID = os.getenv('API_ID')
API_HASH = os.getenv('API_HASH')
SESSION_NAME = 'link_resolver_session'  # Local session file for authentication persistence

# Validate credentials are available
if not API_ID or not API_HASH:
    logger.error("API credentials not found. Please set API_ID and API_HASH in your .env file.")
    sys.exit(1)

async def resolve_invite_links(file_path):
    """
    Resolve Telegram t.me invite links to their corresponding channel IDs.
    
    This function:
    1. Connects to Telegram using your credentials
    2. Authenticates with your account (first-time use requires phone verification)
    3. Processes each invite link to extract the channel ID and title
    4. Outputs results to console in a formatted way
    
    Args:
        file_path (str): Path to a text file containing t.me links, one per line
    """
    
    # Create and start the Telegram client
    client = TelegramClient(SESSION_NAME, API_ID, API_HASH)
    await client.start()
    
    # Handle authentication if needed
    if not await client.is_user_authorized():
        logger.info("First-time authentication required. You'll only need to do this once.")
        logger.info("You need to authorize this script to access your Telegram account.")
        
        # Request and verify phone number
        try:
            phone = input("Enter your phone number with country code (e.g., +1234567890): ")
            await client.send_code_request(phone)
            code = input("Enter the verification code you received on Telegram: ")
            await client.sign_in(phone=phone, code=code)
        except Exception as e:
            logger.error(f"Authentication failed: {str(e)}")
            await client.disconnect()
            return
    
    logger.info("Successfully authenticated with Telegram.")
    
    # Read the invite links file
    try:
        with open(file_path, 'r') as file:
            links = [line.strip() for line in file.readlines() if line.strip()]
    except FileNotFoundError:
        logger.error(f"File not found: {file_path}")
        await client.disconnect()
        return
    except Exception as e:
        logger.error(f"Error reading file: {str(e)}")
        await client.disconnect()
        return
    
    if not links:
        logger.warning("No links found in the file. Please check the format.")
        await client.disconnect()
        return
        
    logger.info(f"Found {len(links)} links to resolve")
    
    # Process each link
    results = []
    
    for i, link in enumerate(links, 1):
        logger.info(f"Processing link {i}/{len(links)}: {link}")
        
        try:
            # Try to get the channel entity directly
            entity = await client.get_entity(link)
            channel_id = entity.id
            channel_title = getattr(entity, 'title', 'Unknown')
            results.append((link, f"{channel_id} (Title: {channel_title})"))
            logger.info(f"Resolved to channel ID: {channel_id}")
        except Exception as e:
            error_msg = str(e)
            logger.error(f"Error resolving {link}: {error_msg}")
            results.append((link, f"Error: {error_msg}"))
        
        # Add a small delay to avoid rate limiting
        await asyncio.sleep(1)
    
    # Display results
    print("\n" + "="*50)
    print("RESULTS (LINK → CHANNEL ID)")
    print("="*50)
    
    for link, result in results:
        print(f"{link} → {result}")
    
    print("\n" + "="*50)
    print("CHANNEL IDS FOR channels.txt")
    print("="*50)
    
    for link, result in results:
        if "Error" not in result:
            channel_id = result.split()[0]
            print(channel_id)
    
    await client.disconnect()

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python telegram_link_resolver.py <path_to_links_file>")
        print("Example: python telegram_link_resolver.py telegram_links.txt")
        print("\nThe links file should contain t.me URLs, one per line, such as:")
        print("https://t.me/channel_name")
        print("https://t.me/joinchat/INVITE_CODE")
        sys.exit(1)
    
    links_file = sys.argv[1]
    asyncio.run(resolve_invite_links(links_file)) 