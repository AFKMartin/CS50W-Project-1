from django.shortcuts import render, redirect
from django.http import Http404, HttpResponseRedirect
from . import util
from .util import markdown_to_html
# import markdown2
import random
from django.urls import reverse

def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def entry(request, title):
    content = util.get_entry(title)
    if content:
        html_content = markdown_to_html(content) # this converts the MD to HTML
        return render(request, "encyclopedia/entry.html", {
            "title": title,       
            "content": html_content
        })
    else:
        raise Http404("Page not found") 

def search(request):
    query = request.GET.get("q", "").strip()  
    if not query:
        return redirect("index") 

    entries = util.list_entries()
    results = [entry for entry in entries if query.lower() in entry.lower()]

    if query.lower() in [entry.lower() for entry in entries]:
        return redirect("entry", title=query)

    return render(request, "encyclopedia/search.html", {
        "query": query,
        "results": results
    })

def new_page(request):
    if request.method == "POST":
        title = request.POST.get("title").strip()
        content = request.POST.get("content").strip()

        if util.get_entry(title):  # entry already exists
            return render(request, "encyclopedia/new.html", {
                "error": "An entry with this title already exists.",
                "title": title,
                "content": content
            })
        # formatted_content = f"# {title}\n\n{content}" yeah this is an issue

        util.save_entry(title, content)
        return redirect("entry", title=title)

    return render(request, "encyclopedia/new.html")

def edit_entry(request, title):
    # Catch the content by its title
    content = util.get_entry(title)

    # Just in case, dunno when this could happend but just in case
    if content is None:
        raise Http404("Page not found")
        
    if request.method == "POST":
        new_content = request.POST.get("content", "").strip()
        # full_content = f"# {title}\n{new_content}" yeah lets not do that for now
        util.save_entry(title, new_content)
        return redirect("entry", title=title)
    
    return render(request, "encyclopedia/edit.html", {
        "title": title,
        "content": content
    })

def random_page(request):
    entries = util.list_entries() 
    if not entries:
        raise Http404("No entries available") # In case there is no entries
    
    title = random.choice(entries) 

    return HttpResponseRedirect(reverse("entry", args=[title]))