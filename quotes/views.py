import random
from django.shortcuts import render, redirect, get_object_or_404
from .models import Quote, TOPIC_CHOICES
from .forms import QuoteForm
from django.db.models import Count

def random_quote(request):
    quotes = Quote.objects.all()
    selected_topics = request.GET.getlist("topics")
    if selected_topics:
        quotes = quotes.filter(topic__in=selected_topics)
    if not quotes:
        return render(request, 'quotes/random_quote.html', {'quote': None})

    # Вес
    population = [q for q in list(quotes) for _ in range(q.weight)]
    quote = random.choice(population)

    # Увеличиваем просмотры
    quote.views += 1
    quote.save()

    return render(request, 'quotes/random_quote.html', {
        'quote': quote,
        'selected_topics': selected_topics,
        'all_topics': TOPIC_CHOICES
    })

def add_quote(request):
    if request.method == 'POST':
        form = QuoteForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('random_quote')
        else:
            return render(request, "quotes/add_quote.html", {"form": form})
    else:
        form = QuoteForm()
    return render(request, 'quotes/add_quote.html', {'form': form})

def show_quote(request, pk):
    quote = get_object_or_404(Quote, pk=pk)

    # Увеличиваем просмотры только если GET-запрос (а не при лайке/дизлайке)
    if request.method == "GET":
        quote.views += 1
        quote.save()

    return render(request, 'quotes/random_quote.html', {'quote': quote})

def vote(request, quote_id, action):
    quote = get_object_or_404(Quote, id=quote_id)
    if action == "like":
        quote.likes += 1
    elif action == "dislike":
        quote.dislikes += 1
    quote.save()
    return redirect('show_quote', pk=quote.id)

def top_quotes(request):
    sort = request.GET.get('sort', 'likes')  # по умолчанию лайки
    if sort == "likes":
        quotes = Quote.objects.order_by('-likes')[:10]
    elif sort == "dislikes":
        quotes = Quote.objects.order_by('-dislikes')[:10]
    elif sort == "views":
        quotes = Quote.objects.order_by('-views')[:10]
    else:
        quotes = Quote.objects.order_by('-likes')[:10]  # fallback

    return render(request, 'quotes/top_quotes.html', {'quotes': quotes, 'active_page': 'top_quotes', 'sort':sort})

def topics(request):
    stats = Quote.objects.values('topic').annotate(count=Count('id'))
    topics = [dict(Quote._meta.get_field('topic').choices)[s['topic']] for s in stats]
    counts = [s['count'] for s in stats]

    return render(request, 'quotes/topics_chart.html', {
        'topics': topics,
        'counts': counts,
        'active_page': 'topics'
    })

