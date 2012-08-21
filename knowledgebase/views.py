from labgeeksrpg.knowledgebase.models import *
from labgeeksrpg.knowledgebase.forms import *
from django.shortcuts import render_to_response
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from datetime import datetime
from django.http import HttpResponseRedirect
from django.template import RequestContext
from django.core.context_processors import csrf


def view_question(request, q_id):
    try:
        question = Question.objects.get(id=q_id)
    except Question.DoesNotExist:
        return render_to_response('no_question.html', {"request": request, })
    try:
        answers = Answer.objects.filter(question=question).exclude(is_best=True)
        try:
            best_answer = Answer.objects.filter(question=question).filter(is_best=True)
        except Answer.DoesNotExist:
            best_answer = None
    except Answer.DoesNotExist:
        answers = None
        best_answer = None
    args = {
        'question': question.question,
        'more_info': question.more_info,
        'best_answer': best_answer,
        'answers': answers,
        'date': question.date,
        'author': question.user,
        'request': request,
        'question_id': q_id,
    }
    return render_to_response('view_question.html', args)


@login_required
def create_question(request):
    c = {}
    c.update(csrf(request))
    if request.method == 'POST':
        form = CreateQuestionForm(request.POST)
        if form.is_valid():
            question = form.save(commit=False)
            question.user = request.user
            question.date = datetime.now().date()
            question.save()
        return HttpResponseRedirect('/knowledgebase/' + str(question.id) + '/')
    else:
        form = CreateQuestionForm()
        form_fields = []
        for field in form.visible_fields():
            field_info = {
                'help_text': field.help_text,
                'label_tag': field.label_tag,
                'field': field,
            }
            form_fields.append(field_info)
        args = {
            'form_fields': form_fields,
            'user': request.user,
            'request': request,
        }
        return render_to_response('create_question.html', args, context_instance=RequestContext(request))


def kb_home(request):
    return HttpResponseRedirect('/knowledgebase/create/')
