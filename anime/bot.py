from asgiref.sync import sync_to_async
from telegram import Update
from telegram.ext import Application, CommandHandler, CallbackContext
import os
import sys

sys.path.append('/Users/mukhammedbahythan/PycharmProjects/anime_site')

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'anime_project.settings')
import django
django.setup()


from anime.models import Anime




TOKEN = '7782675314:AAGOjJFDzbGYsPCvR1My9puGs4-nGvnIC_U'

@sync_to_async
def get_top_5_animes():
    animes = Anime.objects.all()

    anime_ratings = []
    for anime in animes:
        # Замени в зависимости от твоей модели:
        ratings = anime.rating.all()  # или anime.rating_set.all()

        if ratings.exists():
            average_rating = sum(r.value for r in ratings) / ratings.count()
            anime_ratings.append((anime.title, average_rating))

    if not anime_ratings:
        return "Нет аниме с рейтингами 😢"

    anime_ratings.sort(key=lambda x: x[1], reverse=True)
    top_5_animes = anime_ratings[:5]

    top_5_message = "🏆 Топ-5 аниме:\n"
    for idx, (title, rating) in enumerate(top_5_animes, 1):
        top_5_message += f"{idx}. {title} — {rating:.2f} / 5\n"

    return top_5_message



async def start(update: Update , CallbackContext):
    await update.message.reply_text("Привет! Я помогу тебе найти топ-5 аниме. Введи команду /top для получения списка.")



async def top(update: Update , CallbackContext):
    top_5_message = await get_top_5_animes()
    await update.message.reply_text(top_5_message)



def main():
    application = Application.builder().token(TOKEN).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("top", top))

    application.run_polling()


if __name__ == "__main__":
    main()
