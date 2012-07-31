from labgeeksrpg.wiki.models import Page, RevisionHistory
from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect
from django.template import RequestContext
from django.core.context_processors import csrf
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from datetime import datetime


@login_required
def view_page(request, page_name):
    try:
        page = Page.objects.get(name=page_name)
    except Page.DoesNotExist:
        return render_to_response("create.html", {"page_name": page_name})
    content = page.content
    return render_to_response("view.html", {"page_name": page_name, "content": content})


@login_required
def edit_page(request, page_name):
    try:
        page = Page.objects.get(name=page_name)
        content = page.content
    except Page.DoesNotExist:
        content = ""
    user = request.user
    c = {}
    c.update(csrf(request))
    if request.method == "POST":
        content = request.POST["content"]
        if page:
            page = Page.objects.get(name=page_name)
            revision = RevisionHistory.objects.create(page=page, user=user, before=page.content, after=content, date=datetime.now())
            page.content = content
            revision.save()
        else:
            page = Page(name=page_name, content=content, date=datetime.now(), author=user)
        page.save()
        return HttpResponseRedirect("/wiki/" + page_name + "/")
    return render_to_response("edit.html", locals(), context_instance=RequestContext(request))


@login_required
def wiki_home(request):
    try:
        PAGES = Page.objects.all()
    except:
        PAGES = None
    return render_to_response('home.html', {'pages': PAGES})


@login_required
def revision_history(request, page_name):
    try:
        page = Page.objects.get(name=page_name)
    except Page.DoesNotExist:
        page = None
    revision_history = []
    if page:
        revisions = RevisionHistory.objects.filter(page=page).order_by('date').reverse()
        for revision in revisions:
            holder = {
                'date': revision.date,
                'user': revision.user,
                'original_text': revision.before,
                'revised_text': revision.after,
            }
            revision_history.append(holder)
    args = {
        'name': page_name,
        'revision_history': revision_history,
    }
    return render_to_response('revisions.html', args)
