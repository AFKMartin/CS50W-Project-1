from django.shortcuts import render, redirect
from django.http import Http404
from . import util
import markdown2

def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def entry(request, title):
    content = util.get_entry(title)
    if content:
        html_content = markdown2.markdown(content) # this converts the MD to HTML
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
        formatted_content = f"# {title}\n\n{content}"

        util.save_entry(title, formatted_content)
        return redirect("entry", title=title)

    return render(request, "encyclopedia/new.html")

def edit_entry(request, title):
    # Catch the content by its title
    content = util.get_entry(title)

    # Just in case, dunno when this could happend but just in case
    if content is None:
        raise Http404("Page not found")
    
    # Temporaly remove the title while editing
    
    if request.method == "POST":
        new_content = request.POST.get("content", "").strip()
        # Always prepend the md title
        full_content = f"# {title}\n{new_content}"
        util.save_entry(title, full_content)
        return redirect("entry", title=title)
    
    return render(request, "encyclopedia/edit.html", {
        "title": title,
        "content": content
    })
    
    












