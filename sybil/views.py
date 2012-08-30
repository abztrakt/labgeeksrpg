from haystack.views import *
from labgeeksrpg.delphi.models import Question
from labgeeksrpg.pythia.models import Page
from django.shortcuts import render_to_response


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
    return render_to_response('oracles.html', locals())
