from django.shortcuts import render
from django import forms
from . import util

class SearchForm(forms.Form):
    search_entry = forms.CharField(label='Search Encyclopedia')

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
    search_entry = request.GET.get("q")
    if util.get_entry(search_entry):
        return render(request, "encyclopedia/full_entry.html", {
            "entry": util.get_entry(search_entry),
            "entry_name": search_entry
        })
    else:
        return render(request, "encyclopedia/apology.html", {
            "entry_name": search_entry
        })
    
    

    

