import os
from telebot import TeleBot
import instaloader

TOKEN = os.environ.get("TOKEN")
bot = TeleBot(TOKEN)

loader = instaloader.Instaloader(
    download_videos=True,
    download_pictures=True,
    save_metadata=False,
    quiet=True
)

@bot.message_handler(func=lambda m: True)
def handle(m):
    url = m.text.strip()

    if "instagram.com" not in url:
        bot.send_message(m.chat.id, "❌ Send a valid Instagram link")
        return

    try:
        shortcode = url.split("/")[-2]
        post = instaloader.Post.from_shortcode(loader.context, shortcode)
        loader.download_post(post, shortcode)

        for f in os.listdir(shortcode):
            if f.endswith(".mp4"):
                with open(f"{shortcode}/{f}", "rb") as v:
                    bot.send_video(m.chat.id, v)
                break

        os.system(f"rm -rf {shortcode}")

    except:
        bot.send_message(m.chat.id, "⚠️ Failed. Post must be public.")

bot.infinity_polling()
