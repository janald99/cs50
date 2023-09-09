from django import forms
from django.shortcuts import render, redirect
from django.http import Http404
from django.urls import reverse

import markdown2
import random

from . import util

class NewPageForm(forms.Form):
    title = forms.CharField(label="Title", max_length=50)
    content = forms.CharField(widget=forms.Textarea, label="Content")

class EditPageForm(forms.Form):
    content = forms.CharField(widget=forms.Textarea, label="Content")

def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })


def entry(request, title):
    content = util.get_entry(title)
    if content is not None:
        # Convert MD to HTML using markdown2
        content_html = markdown2.markdown(content)
        return render(request, "encyclopedia/entry.html", {
            "title": title,
            "content": content_html
        })
    else:
        raise Http404("Page not found")


def search(request):
    query = request.GET.get("q")
    if query:
        exact_entry = util.get_entry(query)
        if exact_entry:
            return redirect(reverse("entry", args=[query]))
        else:
            matching_entries = [
                entry for entry in util.list_entries() if query.lower() in entry.lower()]
            return render(request, "encyclopedia/search_results.html", {
                "search_results": matching_entries
            })
    else:
        return redirect("index")
    
def new_page(request):
    if request.method == "POST":
        form = NewPageForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data["title"]
            content = form.cleaned_data["content"]
            #if entry exist, show error.
            if util.get_entry(title):
                form.add_error("title", "Entry with this title already exists.")
            else:
                util.save_entry(title, content)
                return redirect(reverse("entry", args=[title]))
    else:
        form = NewPageForm()
    return render(request, "encyclopedia/new_page.html", {
        "form": form
    })

def edit_page(request, title):
    content = util.get_entry(title)
    if request.method == "POST":
        form = EditPageForm(request.POST)
        if form.is_valid():
            content = form.cleaned_data["content"]
            util.save_entry(title, content)
            return redirect("entry", title=title)
    else:
        form = EditPageForm(initial={
            "content": content
        })
    
    return render(request, "encyclopedia/edit_page.html", {
        "title": title,
        "form": form
    })

def random_page(request):
    entries = util.list_entries()
    random_entry = random.choice(entries)
    return redirect("entry", title=random_entry)
