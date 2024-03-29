import datetime
from haystack import indexes
from .models import Book


class BookIndex(indexes.SearchIndex, indexes.Indexable):
	text = indexes.CharField(document=True, use_template=True)
	title=indexes.CharField(model_attr='title')
	isbn=indexes.CharField(model_attr='isbn')
	published=indexes.DateTimeField(model_attr='published')

	def get_model(self):
		return Book
	def index_queryset(self, using=None):
		return self.get_model().objects.all()