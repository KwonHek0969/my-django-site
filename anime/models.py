from django.db import models
from django.contrib.auth.models import User


class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Anime(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    release_year = models.PositiveIntegerField()
    poster = models.ImageField(upload_to='posters/', blank=True, null=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='animes', null=True, blank=True)
    youtube_url = models.URLField(blank=True, null=True)
    video = models.FileField(upload_to='videos/', blank=True, null=True)


def __str__(self):
        return self.title



class Rating(models.Model):
    anime = models.ForeignKey(Anime,on_delete=models.CASCADE,related_name='rating')
    value = models.IntegerField(choices=[(i ,str(i)) for i in range(1,6)])
    created_at = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return f'{self.anime.title} - {self.value}'


class Comment(models.Model):
    anime = models.ForeignKey(Anime, on_delete=models.CASCADE, related_name='comment')
    name = models.CharField(max_length=300)
    text = models.TextField()
    created_at =models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Комментарий от {self.name} к {self.title}'
