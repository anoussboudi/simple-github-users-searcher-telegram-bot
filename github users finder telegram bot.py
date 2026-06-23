from telegram import Update
from telegram.ext import CommandHandler , Application , ContextTypes
import os 
import requests

from dotenv import load_dotenv
token= "your token here"
pausing_message= "bot is paused type /on"
bot_paused= False
async def start(update:Update , context:ContextTypes.DEFAULT_TYPE):
    global bot_paused
    if bot_paused:
        await update.message.reply_text(pausing_message)
    else:
        await update.message.reply_text("bot is up")
async def pause(update:Update , context:ContextTypes.DEFAULT_TYPE):
    global bot_paused
    bot_paused= True
    await update.message.reply_text("bot is paused now type /on to turn it on")
async def on(update:Update , context:ContextTypes.DEFAULT_TYPE):
    global bot_paused
    bot_paused = False
    await update.message.reply_text("bot is on to pause it type /pause")
async def help(update:Update , context:ContextTypes.DEFAULT_TYPE):
    global bot_paused
    if bot_paused:
        await update.message.reply_text(pausing_message)
    else:
        await update.message.reply_text("available commands /start /on /pause /github (user) /weather (city) /joke")
async def gituser(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global bot_paused
    if bot_paused:
        await update.message.reply_text(pausing_message)
        return
    
    if not context.args:
        await update.message.reply_text("Usage: /github username")
        return
    
    try:
        username = context.args[0]
        response = requests.get(f"https://api.github.com/users/{username}", timeout=5)
        
        if response.status_code == 200:
            data = response.json()
            
            # Build ONE complete message
            message = f"=== GitHub User: {username} ===\n"
            for key, value in data.items():
                message += f"{key}: {value}\n"
            
            # Send ONCE, not multiple times
            await update.message.reply_text(message)
        else:
            await update.message.reply_text("user not found")
    
    except Exception as e:
        await update.message.reply_text(f"error: {e}")
async def weather(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global bot_paused
    if bot_paused:
        await update.message.reply_text(pausing_message)
        return
    
    if not context.args:
        await update.message.reply_text("Usage: /weather city")
        return
    
    try:
        api_key = os.getenv('weather')
        
        if not api_key:
            await update.message.reply_text("API key not configured")
            return
        
        city = context.args[0]
        url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
        
        response = requests.get(url, timeout=5)
        
        # DEBUG - Show the status code
        await update.message.reply_text(f"Status: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            message = f"=== Weather in {city} ===\n"
            for key, value in data.items():
                message += f"{key}: {value}\n"
            await update.message.reply_text(message)
        else:
            # DEBUG - Show what error the API returned
            await update.message.reply_text(f"Error: {response.status_code}\nResponse: {response.text}")
    
    except Exception as e:
        await update.message.reply_text(f"error: {e}")
async def joke(update:Update , context:ContextTypes.DEFAULT_TYPE):
    global bot_paused
    if bot_paused :
        await update.message.reply_text(pausing_message)
    else:
        try:
            response= requests.get("https://official-joke-api.appspot.com/random_joke")
            if response.status_code == 200 :
                data= response.json()
                
                joke_text = f"{data['setup']}\n\n{data['punchline']}"
                await update.message.reply_text(joke_text)
            else :
                await update.message.reply_text("no joke today unfotunately :(")
        except Exception as e:
            await update.message.reply_text(f"error{e}")
def main():
    app = Application.builder().token(token).build()
    app.add_handler(CommandHandler("start",start))
    app.add_handler(CommandHandler("help",help))
    app.add_handler(CommandHandler("pause",pause))
    app.add_handler(CommandHandler("on",on))
    app.add_handler(CommandHandler("github",gituser))
    app.add_handler(CommandHandler("weather",weather))
    app.add_handler(CommandHandler("joke",joke))
    app.run_polling()
if __name__ == '__main__':
    main()

        
                



