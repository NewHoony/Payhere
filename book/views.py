from django.shortcuts import get_object_or_404,render,redirect
from django.utils import timezone
from django.urls import reverse
from decimal import Decimal
from .models import Book
from .forms import BookForm
import datetime
import pyshorteners

def index(request):
    books = Book.objects.all().order_by('-date')
    return render(request,"book/index.html", {'books': books})

def create(request):
    if request.method == "POST":
        form = BookForm(request.POST, request.FILES)
        if form.is_valid():
            books = form.save(commit=False)
            books.date = timezone.now()
            books.save()
            return redirect('book:index')
    else:
        form = BookForm()
    return render(request, 'book/create.html', {'form': form})

def detail(request, pk):
    books= Book.objects.get(pk=pk)
    url = request.build_absolute_uri(reverse('book:detail', args=[books.pk]))
    s = pyshorteners.Shortener()
    short_url = s.tinyurl.short(url)
    return render(request, 'book/detail.html', {'books': books, 'short_url': short_url})




def update(request, pk):
    books = get_object_or_404(Book, pk=pk)
    if request.method == 'POST':
        form = BookForm(request.POST, request.FILES, instance=books)
        if form.is_valid():
            books = form.save(commit=False)
            books.date = timezone.now()
            books.save()
            return redirect('book:index')
    else:
        form = BookForm(instance=books)
    return render(request, 'book/update.html', {'form': form})

def delete(request, pk):
    books = Book.objects.get(pk=pk)
    books.delete()
    return redirect('book:index')

def duplicate(request, pk):
    books = Book.objects.get(pk=pk)
    books.pk = None
    books.date = timezone.now()
    books.save()
    return redirect('book:index')



# Create your views here.
