import haystack
haystack.autodiscover()

from haystack.query import SearchQuerySet

SearchQuerySet().autocomplete(content_auto='test')
