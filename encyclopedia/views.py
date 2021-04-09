from django.shortcuts import render
from markdown2 import Markdown

import random
from . import util


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })


def get_entry(request, title):
    if util.get_entry(title) is None:
        return render(request, "encyclopedia/no_entry.html", {
            "title": title,
        })
    else:
        entry = util.get_entry(title)
        markdowner = Markdown()
        entry_html = markdowner.convert(entry)
        return render(request, "encyclopedia/entry.html", {
            "title": title,
            "body": entry_html,
        })


def search(request):
    query = request.GET['q']
    possible_entry = util.get_entry(query)

    if possible_entry:
        markdowner = Markdown()
        entry_html = markdowner.convert(possible_entry)
        return render(request, "encyclopedia/entry.html", {
            "title": query,
            "body": entry_html,
        })

    else:
        stored_entries = util.list_entries()
        suggested_entries = []

        print(stored_entries)
        for entry in stored_entries:
            if query.lower() in entry.lower():
                suggested_entries.append(entry)
        print(suggested_entries)
        return render(request, "encyclopedia/index.html", {
            "entries": suggested_entries,
            "query": query,
        })


def random_search(request):
    entries = util.list_entries()
    random_entry_title = random.choice(entries)
    random_entry = util.get_entry(random_entry_title)
    markdowner = Markdown()
    entry_html = markdowner.convert(random_entry)
    return render(request, "encyclopedia/entry.html", {
        "title": random_entry_title,
        "body": entry_html,
    })


def create_entry(request):
    if request.method == 'GET':
        return render(request, "encyclopedia/create_entry.html")
    if request.method == 'POST':
        title = request.POST['title']
        body = request.POST['body']
        entries = util.list_entries()

        if title not in entries:
            util.save_entry(title, body)
            markdowner = Markdown()
            entry_html = markdowner.convert(body)
            return render(request, "encyclopedia/entry.html", {
                "title": title,
                "body": entry_html,
            })
        else:
            return render(request, "encyclopedia/already_exists.html", {
                "title": title,
            })


def edit(request, title):
    if request.method == 'GET':
        entry = util.get_entry(title)
        return render(request, "encyclopedia/edit.html", {
            "title": title,
            "body": entry,
        })
    if request.method == 'POST':
        body = request.POST['post_body']
        util.save_entry(title, body)
        markdowner = Markdown()
        entry_html = markdowner.convert(body)
        return render(request, "encyclopedia/entry.html", {
            "title": title,
            "body": entry_html,
        })
