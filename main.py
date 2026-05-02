from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, CommandHandler, filters, ContextTypes
import yt_dlp
import os

TOKEN = "8420933649:AAHg0wkIrcC-svuhHUEx3C0t5wbXRsCv8mI"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("✨ أهلاً بك! أرسل لي أي رابط وسأحمله لك.")

async def download(update: Update, context: ContextTypes.DEFAULT_TYPE):
    url = update.message.text
    if "http" not in url: return
    
    msg = await update.message.reply_text("⏳ جاري التحميل...")
    ydl_opts = {'format': 'best', 'outtmpl': 'video_%(id)s.%(ext)s', 'quiet': True}

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            filename = ydl.prepare_filename(info)
        
        with open(filename, 'rb') as f:
            await update.message.reply_video(video=f)
        
        os.remove(filename)
        await msg.delete()
    except Exception as e:
        await msg.edit_text(f"❌ حدث خطأ: تأكد من الرابط.")

if __name__ == '__main__':
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, download))
    app.run_polling()
