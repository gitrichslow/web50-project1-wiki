from django.shortcuts import render
from django import forms
from django.http import HttpResponseRedirect
from django.urls import reverse
import os

from . import util

class NewEntryForm(forms.Form):
    title = forms.CharField(label='Entry Title', max_length=80)
    text = forms.CharField(label='Full Entry', widget=forms.Textarea)


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def full_entry(request, entry):
    if util.get_entry(entry):
        return render(request, "encyclopedia/full_entry.html", {
            "entry": util.get_entry(entry),
            "entry_name": entry
        })
    else:
        return render(request, "encyclopedia/apology.html", {
            "entry_name": entry
        })

def search_entry(request):
    search = request.GET.get("q")
    #print("entry")
    if util.get_entry(search):
        return HttpResponseRedirect(reverse('full_entry', args=(search,)))
    else:
        return render(request, "encyclopedia/matches.html", {
            "search": search,
            "entries": util.list_entries()
        })

def new_entry(request):
    if request.method == 'POST':
        form = NewEntryForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data['title']
            text = form.cleaned_data['text']
            entry = title.replace(' ', '-')
            filename = title.replace(' ', '-') + '.md'
            BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            MARKDOWN_DIR = os.path.join(BASE_DIR, 'entries')
            filepath = os.path.join(MARKDOWN_DIR, filename)
            if not os.path.isfile(filepath):
                with open(filepath, 'w') as f:
                    f.write('# {}\n\n{}'.format(title, text))
                    return HttpResponseRedirect(reverse('full_entry', args=(entry,)))
            else:
                return render(request, "encyclopedia/entry_apology.html", {
                    "filename": filename
            })

    if request.method == 'GET':
        form = NewEntryForm()
        return render(request, 'encyclopedia/new_entry.html', {'form': form})
