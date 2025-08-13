from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Q
import re

from .forms import RatingForm, CommentForm
from .models import Anime, Category

def anime_list(request):
    query = request.GET.get('q', '')
    category_id = request.GET.get('category', '')

    animes = Anime.objects.all()
    categories = Category.objects.all()

    if query:
        animes = animes.filter(Q(title__icontains=query))

    if category_id.isdigit():
        animes = animes.filter(category_id=int(category_id))

    return render(request, 'anime/anime_list.html', {
        'animes': animes,
        'categories': categories,
    })

def anime_detail(request, pk):
    anime = get_object_or_404(Anime, pk=pk)

    ratings = anime.rating.all()
    comments = anime.comment.all().order_by('-created_at')

    average_rating = round(sum(r.value for r in ratings) / ratings.count(), 1) if ratings else 'Нет оценок'

    rating_form = RatingForm()
    comment_form = CommentForm()

    if request.method == 'POST':
        if 'rating_submit' in request.POST:
            rating_form = RatingForm(request.POST)
            if rating_form.is_valid():
                rating = rating_form.save(commit=False)
                rating.anime = anime
                rating.save()
                return redirect('anime_detail', pk=anime.pk)
        elif 'comment_submit' in request.POST:
            comment_form = CommentForm(request.POST)
            if comment_form.is_valid():
                comment = comment_form.save(commit=False)
                comment.anime = anime
                comment.save()
                return redirect('anime_detail', pk=anime.pk)

    embed_url = None
    if anime.youtube_url:
        youtube_id_match = re.search(r'(?:v=|youtu\.be/)([\w-]+)', anime.youtube_url)
        if youtube_id_match:
            youtube_id = youtube_id_match.group(1)
            embed_url = f"https://www.youtube.com/embed/{youtube_id}"

    return render(request, 'anime/anime_detail.html', {
        'anime': anime,
        'embed_url': embed_url,
        'rating_form': rating_form,
        'average_rating': average_rating,
        'comments': comments,
        'comment_form': comment_form,
    })