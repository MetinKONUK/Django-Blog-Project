import article
from django.contrib.messages.api import info
from django.shortcuts import redirect, render, get_object_or_404
from .forms import ArticleForm
from .models import Article, Comment
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.urls import reverse
# Create your views here.

def articles(request):
    keyword = request.GET.get("keyword")
    if keyword:
        articles = Article.objects.filter(title__contains = keyword)
        return render(request, "articles.html", {"articles": articles})
    articles = Article.objects.all()
    return render(request, "articles.html", {"articles" : articles})

def index(request):
    return render(request, "index.html")


def about(request):
    return render(request, "about.html")

@login_required(login_url="user:login")
def dashboard(request):
    articles = Article.objects.filter(author = request.user)
    context = {
        "articles" : articles
    }
    return render(request, "dashboard.html", context = context)

@login_required(login_url="user:login")
def addarticle(request):
    form = ArticleForm(request.POST or None, request.FILES)
    if form.is_valid():
        article = form.save(commit=False)
        article.author = request.user
        print(request.FILES)
        article.save()
        messages.success(request, "Article saved")
        return redirect("article:dashboard")
    return render(request, "addarticle.html", {"form":form})
@login_required(login_url="user:login")
def detail(request, id):
    article = get_object_or_404(Article, id = id)
    comments = article.comments.all()
    return render(request, "detail.html", {"article" : article, "comments" : comments})

@login_required(login_url="user:login")
def updateArticle(request, id):
    article = get_object_or_404(Article, id = id)
    form = ArticleForm(request.POST or None, request.FILES or None, instance = article)
    if form.is_valid():
        article = form.save(commit=False)
        article.author = request.user
        article.save()
        messages.success(request, "Article updated")
        return redirect("article:dashboard")
    return render(request, "update.html", {"form":form})

@login_required(login_url="user:login")
def deleteArticle(request, id):
    article = get_object_or_404(Article, id = id)
    article.delete()
    messages.success(request, "Article deleted")
    return redirect("article:dashboard")

@login_required(login_url="user:login")
def addComment(request, id):
    article = get_object_or_404(Article, id = id)
    if request.method == "POST":
        comment_author = request.user
        comment_content = request.POST.get("comment_area")
        newComment = Comment(comment_author = comment_author, comment_content = comment_content)
        newComment.article = article
        newComment.save()
    return redirect(reverse("article:detail", args=[id]))
