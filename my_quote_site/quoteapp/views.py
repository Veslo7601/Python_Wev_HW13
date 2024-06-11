from django.shortcuts import render, redirect, get_object_or_404
from .models import Quotes, Autors
from .forms import TagForm, AuthorForm, QuoteForm
from django.core.paginator import Paginator


# Create your views here.


def main(request):
    quotes_list = Quotes.objects.all()
    paginator = Paginator(quotes_list, 10)
    page_number = request.GET.get('page')
    quotes = paginator.get_page(page_number)
    return render(request, 'quoteapp/index.html', {'quotes': quotes})

def tag_create(request):
    if request.method == 'POST':
        form = TagForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect(to='quoteapp:main')
    else:
        form = TagForm()
    return render(request, 'quoteapp/tag_form.html', {'form': form})

def author_create(request):
    if request.method == 'POST':
        form = AuthorForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect(to='quoteapp:main')
    else:
        form = AuthorForm()
    return render(request, 'quoteapp/author_form.html', {'form': form})

def quote_create(request):
    if request.method == 'POST':
        form = QuoteForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect(to='quoteapp:main')
    else:
        form = QuoteForm()
    return render(request, 'quoteapp/quote_form.html', {'form': form})

def author_detail(request, author_id):
    author = get_object_or_404(Autors, pk=author_id)
    return render(request, 'quoteapp/author_detail.html', {"autors": author})
