from django.shortcuts import render
from django import forms
from django.http import HttpResponseRedirect
from django.urls import reverse
import os
import random
from markdown2 import Markdown

from . import util

class EditEntryForm(forms.Form):
                start_entry = forms.CharField(widget=forms.Textarea(attrs={'rows':10, 'cols':60}), label='Edit entry')
                title = forms.CharField(widget=forms.HiddenInput())

class NewEntryForm(forms.Form):
    title = forms.CharField(label='Entry Title', max_length=80)
    text = forms.CharField(label='Full Entry', widget=forms.Textarea(attrs={'rows':10, 'cols':60}))


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def full_entry(request, entry):
    if util.get_entry(entry):
                    markdowner = Markdown()
                    entry_name = entry
                    full_entry = markdowner.convert(util.get_entry(entry))
                    entry = util.get_entry(entry)
                    return render(request, "encyclopedia/full_entry.html", {
                                "entry": entry,
                                "full_entry": full_entry,
                                "entry_name": entry_name
                    })
    else:
                    entry_name = entry
                    return render(request, "encyclopedia/apology.html", {
                "entry": entry
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

def edit_entry(request):
    if request.method == 'POST':

        if 'full_entry_form' in request.POST:
            start_entry = request.POST.get('full_entry_form')
            title = request.POST.get('entry_name')


            #form = EditEntryForm(initial=request.POST)
            form = EditEntryForm(initial={'start_entry': start_entry, 'title': title})

            return render(request, 'encyclopedia/edit_entry.html', {
                            'form': form,
                            'title': title
            })
        if 'start_entry' in request.POST and 'title' in request.POST:
            form = EditEntryForm(request.POST)
            if form.is_valid():
                text = form.cleaned_data['start_entry']
                title = form.cleaned_data['title']
                filename = title.replace(' ', '-') + '.md'
                #entry = title.replace(' ', '-')
                BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
                MARKDOWN_DIR = os.path.join(BASE_DIR, 'entries')
                filepath = os.path.join(MARKDOWN_DIR, filename)
                with open(filepath, 'w') as f:
                    f.write('{}'.format(text))
                return HttpResponseRedirect(reverse('full_entry', args=(title,)))
        return HttpResponseRedirect(reverse('index'))

def random_entry(request):
    entries = util.list_entries()
    random_num = random.randrange(0, len(entries))
    return HttpResponseRedirect(reverse('full_entry', args=(entries[random_num],)))
