from labgeeksrpg.wiki.models import Page
from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect
from django.template import RequestContext
from django.core.context_processors import csrf

def view_page(request, page_name):
    try:
        page = Page.objects.get(pk=page_name)
    except Page.DoesNotExist:
        return render_to_response("create.html", {"page_name": page_name})
    content = page.content
    return render_to_response("view.html", {"page_name": page_name, "content": content})

def edit_page(request, page_name):
    try:
	page = Page.objects.get(pk=page_name)
        content = page.content
    except Page.DoesNotExist:
	content = ""
    c = {}
    c.update(csrf(request))
    if request.method == "POST":
	content = request.POST["content"]
        try:
            page = Page.objects.get(pk=page_name)
	    page.content = content
        except Page.DoesNotExist:
            page = Page(name=page_name, content=content)
        page.save()
        return HttpResponseRedirect("/wiki/" + page_name +"/")
    return render_to_response("edit.html", locals(), context_instance=RequestContext(request))

def save_page(request, page_name):
    content = request.POST["content"]
    try:
	page = Page.objects.get(pk=page_name)
        page.content = content
    except Page.DoesNotExist:
	page = Page(name=page_name, content=content)
    page.save()
    return HttpResponseRedirect("/wiki/" + page_name +"/")
