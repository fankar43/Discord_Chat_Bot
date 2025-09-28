# chatbot_gemini_fixed.py
import discord
from discord.ext import commands
from discord import Intents
import google.generativeai as genai

# -------------------------------
# Apni keys yahan dalo
TOKEN = "YOUR_BOT_TOKEN_ADD_HERE"
GEMINI_API_KEY = "YOU_GIMINI_API_KEY_ADD_HERE"
# -------------------------------

# Gemini configuration
genai.configure(api_key=GEMINI_API_KEY)

# Use one of the available models
model = genai.GenerativeModel("gemini-flash-latest")  # ✅ Ye model available hai
# OR model = genai.GenerativeModel("gemini-pro-latest")

print("✅ Gemini model loaded successfully!")

# Discord bot setup
PREFIX = "!"
intents = Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix=PREFIX, intents=intents)

@bot.event
async def on_ready():
    print(f"✅ Bot logged in as {bot.user}")
    print(f"✅ Model: gemini-flash-latest")

@bot.event
async def on_message(message: discord.Message):
    if message.author == bot.user:
        return

    # Only respond to messages that don't start with prefix
    if not message.content.startswith(PREFIX):
        user_msg = message.content.strip()
        
        # Ignore empty messages
        if not user_msg:
            return

        try:
            print(f"📨 User message: {user_msg}")
            
            # Gemini se response lo
            response = model.generate_content(
                user_msg,
                generation_config=genai.types.GenerationConfig(
                    temperature=0.7,
                    max_output_tokens=1000,
                )
            )
            
            if response.text:
                bot_reply = response.text
                print(f"🤖 Bot reply: {bot_reply[:100]}...")
                
                # Discord character limit (2000 characters)
                if len(bot_reply) > 2000:
                    bot_reply = bot_reply[:1990] + "\n... (message truncated)"
                
                await message.reply(bot_reply, mention_author=False)
            else:
                await message.reply("🤖 Sorry, mujhe koi response nahi mila.", mention_author=False)

        except Exception as e:
            error_msg = f"❌ Error: {str(e)}"
            print(error_msg)
            await message.reply("❌ Temporary error. Please try again.", mention_author=False)

    await bot.process_commands(message)

# Error handling
@bot.event
async def on_command_error(ctx, error):
    print(f"Command Error: {error}")

if __name__ == "__main__":
    try:
        print("🚀 Starting bot...")
        bot.run(TOKEN)
    except discord.LoginFailure:
        print("❌ Invalid Discord token")
    except Exception as e:
        print(f"❌ Bot startup error: {e}")