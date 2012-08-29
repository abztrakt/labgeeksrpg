from haystack.views import *


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
                if not result.pk in questions:
                    returned_results.append(result)
                    questions.append(result.pk)
            elif result.model_name == 'answer':
                if not result.question.pk in questions:
                    returned_results.append(result)
                    questions.append(result.question.pk)
            else:
                returned_results.append(result)

        return returned_results
