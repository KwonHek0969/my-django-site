from django.contrib import admin
from .models import Anime, Category, Rating, Comment

# Регистрация моделей
admin.site.register(Anime)
admin.site.register(Category)
admin.site.register(Rating)
admin.site.register(Comment)
