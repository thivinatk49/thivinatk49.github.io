from django.shortcuts import render, redirect
from . import util
from django.http import HttpResponse, HttpResponseRedirect
from django import forms
from django.urls import reverse
import random

class NewAddForm(forms.Form):
    title = forms.CharField(label="Enter the Title")
    content = forms.CharField(
        widget=forms.Textarea(attrs={'rows': 10, 'cols': 70}),
        label='Enter Markdown Content'
    )

def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def entry(request, title):
    page = util.get_entry(title)
    return render(request, "encyclopedia/content.html", {
        "page": page,
        "title": title.capitalize()
    })

def search(request):
    query = request.GET['q']
    page = util.get_entry(query)
    if page == None:
        return render(request, "encyclopedia/substring.html",{
            "entries": util.list_entries(),
            "query": query
        })
    else:
        return render(request, "encyclopedia/content.html", {
            "page": page,
            "title": query.capitalize()
        })
    
def new(request):
    if request.method=="POST":
        form = NewAddForm(request.POST)

        if form.is_valid():
            title = form.cleaned_data["title"]
            content = form.cleaned_data["content"]
            page = util.get_entry(title)

            if page == None:
                util.save_entry(title, content)
                return HttpResponseRedirect(reverse("entry", args=[title]))
            else:
                return HttpResponse("Error: Encyclopedia entry already exists")
            
        else:
            return render(request, "encyclopedia/newpage.html", {
                "form": form
            }) 
        
    return render(request, "encyclopedia/newpage.html", {
        "form": NewAddForm()
    })

def edit(request, title):
    if request.method=="POST":
        content_new = request.POST.get("content")
        util.save_entry(title, content_new)
        return HttpResponseRedirect(reverse("entry", args=[title]))

    content = util.get_entry(title)    
    return render(request, "encyclopedia/editpage.html", {
        "content_md": content,
        "title": title
    })

def random_page(request):
    entries = util.list_entries()
    random_title = random.choice(entries)
    page = util.get_entry(random_title)
    return render(request, "encyclopedia/content.html", {
        "page": page,
        "title": random_title.capitalize()
    })