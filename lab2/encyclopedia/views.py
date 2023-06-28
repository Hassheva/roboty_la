from django.shortcuts import render
from django import forms
from . import util
from  markdown2 import markdown
from django.urls import reverse
from django.http import HttpResponseRedirect
import random

def helper(request, list_entries):    
    return render(request, "encyclopedia/index.html", {
            "entries": list_entries
        })

def index(request):
    return helper(request, util.list_entries())

def wiki_page(request, title):
    article_md = util.get_entry(title)
    if article_md == None:
        return render(request, "encyclopedia/not_found_article.html", {
            "title": title
        })
    
    return render(request, "encyclopedia/wiki_page.html", {
        "article": markdown(article_md),
        "title": title
    })

def search_article(request):
    if request.method == "POST":
        article_name = request.POST['article_search']
        articles = []
        
        for entry in util.list_entries():
            if article_name == entry:
                return HttpResponseRedirect(reverse("articles:wiki_page", args=(article_name, )))
            elif article_name in entry:
                articles.append(entry)

        if len(articles) == 0:
            return HttpResponseRedirect(reverse("articles:wiki_page", args=(article_name, )))
        return helper(request, articles)
    
class NewArticleForm(forms.Form):
    title_article = forms.CharField(label="Title article", max_length=10)
    content = forms.CharField(widget=forms.Textarea(attrs={"rows":5, "cols":10}))

class EditContentForm(forms.Form):
    content = forms.CharField(widget=forms.Textarea(attrs={"rows":5, "cols":10}))

def create(request):
    if request.method == "POST":
        form = NewArticleForm(request.POST)
        if form.is_valid():
            article_title = form.cleaned_data["title_article"]
            article_content = form.cleaned_data["content"]
            util.save_entry(article_title, article_content)

            return HttpResponseRedirect(reverse("articles:index"))
        else:
            # Якщо форма недійсна, повторно візуалізуємо сторінку з наявною інформацією.
            return render(request, "encyclopedia/create.html", {
                "form": form
            })

    return render(request, "encyclopedia/create.html", {
        "form": NewArticleForm()
    })

def edit(request, title):
    if request.method == "GET":
        article_md = util.get_entry(title)
        form = EditContentForm({
                "content": article_md
            }
        )

        return render(request, "encyclopedia/edit_article.html", {
                    "title": title,
                    "form": form
                })
    else:
        form = EditContentForm(request.POST)
        if form.is_valid():
            article_content = form.cleaned_data["content"]
            util.save_entry(title, article_content)
            return HttpResponseRedirect(reverse("articles:index"))

def random_article(request):
    items = util.list_entries()
    random_item = random.choice(items)
    return HttpResponseRedirect(reverse("articles:wiki_page", args=(random_item, )))









