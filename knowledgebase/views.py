from labgeeksrpg.knowledgebase.models import Issue, Resolution
from labgeeksrpg.knowledgebase.forms import *
from django.shortcuts import render_to_response
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from datetime import datetime
from django.http import HttpResponseRedirect
from django.template import RequestContext
from django.core.context_processors import csrf


def view_issue(request, issue_name):
    try:
        issue = Issue.objects.get(name=issue_name)
    except Issue.DoesNotExist:
        args = {
            'issue_name': issue_name,
            'request': request,
        }
        return HttpResponseRedirect('/knowledgebase/' + issue_name + '/create/')
    chosen_resolution = issue.chosen_resolution
    try:
        resolutions = Resolution.objects.filter(issue=issue)
        if chosen_resolution:
            resolutions.remove(chosen_resolution)
    except Resolution.DoesNotExist:
        resolutions = None
    args = {
        'issue_name': issue.name,
        'content': issue.content,
        'chosen_resolution': chosen_resolution,
        'resolutions': resolutions,
        'date': issue.date,
        'author': issue.user,
        'request': request,
    }
    return render_to_response('view_issue.html', args)


def create_issue(request, issue_name):
    try:
        issue = Issue.objects.get(name=issue_name)
        return HttpResponseRedirect('/knowledgebase/' + issue_name + '/')
    except Issue.DoesNotExist:
        c = {}
        c.update(csrf(request))
        if request.method == 'POST':
            form = CreateIssueForm(request.POST)
            if form.is_valid():
                issue = form.save(commit=False)
                issue.user = request.user
                issue.date = datetime.now().date()
                issue.name = issue_name
                issue.save()
            return HttpResponseRedirect('/knowledgebase/' + issue_name + '/')
        else:
            form = CreateIssueForm()
            form_fields = []
            for field in form.visible_fields():
                field_info = {
                    'help_text': field.help_text,
                    'label_tag': field.label_tag,
                    'field': field,
                }
                form_fields.append(field_info)
            args = {
                'issue_name': issue_name,
                'form_fields': form_fields,
                'user': request.user,
                'request': request,
            }
            return render_to_response('create_issue.html', args, context_instance=RequestContext(request))
