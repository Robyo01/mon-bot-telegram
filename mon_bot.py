import logging
import google.generativeai as genai
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

# ==== Bdel had lma3loumat b les keys dyalk ====
TELEGRAM_BOT_TOKEN ='7308187857:AAHBeO47t-4o3lE8fy6dg3gkd_RjDTsmymI'
GEMINI_API_KEY ='AIzaSyD67LIdW6NGLxkr7l_3DtFzVQX9oSwLVdQ'
# ============================================

# Tconfiguri Gemini API
genai.configure(api_key=GEMINI_API_KEY)

# Lmodel dyal Gemini li ghadi nkhdmo bih
gemini_model = genai.GenerativeModel('gemini-1.5-flash')

# Had lvariable bach n7afdo 3la lhistorique dyal lmo7adatats
chats_history = {}

# Had la fonction katbda mni lmostakhdim kaydir /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Katjawb mni lmostakhdim kaydir /start"""
    user_name = update.effective_user.first_name
    chat_id = update.effective_chat.id
    # Kanms7o lhistorique l9dim ila bda من جديد
    if chat_id in chats_history:
        del chats_history[chat_id]
        
    await update.message.reply_html(
        f"Ahlan {user_name}!\n\nAna bot marbot b Gemini AI. Sift liya ay so2al o ana njawbk.",
    )

# Had la fonction katjawb 3la ay message kaysift lmostakhdim (machí command)
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Katjawb 3la ay message men ghir les commands"""
    chat_id = update.effective_chat.id
    user_message = update.message.text

    # Kanbda chat jdid m3a Gemini ila kan hada awel message
    if chat_id not in chats_history:
        chats_history[chat_id] = gemini_model.start_chat(history=[])

    # Kanbano l'utilisateur bli rah kansaybo ljawab
    await context.bot.send_chat_action(chat_id=chat_id, action='typing')

    try:
        # Kansifto lmessage l Gemini o ntsenaw ljawab
        response = chats_history[chat_id].send_message(user_message)
        gemini_response = response.text
        
        # Kansifto ljawab lmostakhdim f Telegram
        await update.message.reply_text(gemini_response)

    except Exception as e:
        # Ila w9e3 chi mochkil, kanjawbo b message dyal lkhata2
        print(f"Error: {e}")
        await update.message.reply_text("3afwan, w9e3 chi khata2. 7awel mra khra.")


def main() -> None:
    """Hadi hiya li katbda lbot o katخليه khdam"""
    print("Lbot bda kaykhdem...")
    
    # Kanbniw l'application dyal lbot
    application = Application.builder().token(TELEGRAM_BOT_TOKEN).build()

    # Kanzido les handlers (li kaytsento l les commands o les messages)
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    # Kanbda lbot
    application.run_polling()


if __name__ == '__main__':
    main()

