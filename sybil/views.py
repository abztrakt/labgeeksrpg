from haystack.views import *
from labgeeksrpg.sybil.models import *
from labgeeksrpg.delphi.models import Question
from labgeeksrpg.pythia.models import Page
from django.shortcuts import render_to_response
from django.core.context_processors import csrf
from django.template import RequestContext
from datetime import datetime
from django.contrib.auth.decorators import login_required
from labgeeksrpg.sybil.forms import *


class SybilSearch(SearchView):
    def __name__(self):
        return 'SybilSearch'

    def get_results(self):
        """
        Fetches the results via the form.
        Returns an empty list if there's no query to search with.
        """
        questions = []
        returned_results = []
        results = self.form.search()
        for result in results:
            if result.model_name == 'question':
                if not result.object.pk in questions:
                    returned_results.append(result)
                    questions.append(result.object.pk)
            elif result.model_name == 'answer':
                if not result.object.question.pk in questions:
                    returned_results.append(result)
                    questions.append(result.object.question.pk)
            else:
                returned_results.append(result)

        return returned_results

    def extra_context(self):
        return {'request': self.request, }


def oracle_home(request):
    pages = Page.objects.all().order_by('times_viewed')[:10]
    questions = Question.objects.all().order_by('times_viewed')[:10]
    return render_to_response('oracles.html', locals())


@login_required
def upload_image(request):
    c = {}
    c.update(csrf(request))
    max_pk = 0
    try:
        screenshots = Screenshot.objects.all().order_by('pk')
        if screenshots:
            max_pk = screenshots[0].pk
    except:
        pass
    if request.method == 'POST':
        form = UploadPictureForm(request.POST, request.FILES)
        if form.is_valid():
            screenshot = form.save(commit=False)
            screenshot.user = request.user
            screenshot.date = datetime.now().date()
            screenshot.name = request.FILES['picture']._get_name().replace(" ", "_")
            screenshot.save()
            markdown_code = '![alt](/uploads/oracles/screenshots/' + screenshot.name + ')'
            return render_to_response('upload_success.html', locals())
        return render_to_response('upload_failure.html', locals())
    else:
        form = UploadPictureForm()
        form_fields = []
        for field in form.visible_fields():
            form_fields.append(field)
        args = {
            'form_fields': form_fields,
            'user': request.user,
            'request': request,
        }
        return render_to_response('upload_picture.html', args, context_instance=RequestContext(request))
