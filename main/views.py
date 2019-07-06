from django.shortcuts import render,redirect
from django.http import JsonResponse,HttpResponse
from django.views.generic import DetailView
from .models import Book,Genre,Author,Review
from .search import get_query,pg_records
from django.db.models import Q
from django.forms.models import model_to_dict
from django.core import serializers
import json
from django.core.paginator import Paginator,PageNotAnInteger, EmptyPage
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
import redis
from actions.utils import create_action
from dal import autocomplete
from django.conf import settings
from .forms import SearchForm,ReviewForm
from haystack.query import SearchQuerySet
from django.views.generic.edit import CreateView
from django.contrib import messages

#connect to redis
r = redis.StrictRedis(host=settings.REDIS_HOST,port=settings.REDIS_PORT,db=settings.REDIS_DB)

# Create your views here.


class BookDetail(DetailView):
	model=Book
	template='main/bookdetail.html'


def bookdetail(request,pk):
	book=Book.objects.get(id=pk)
	ratings=Book.objects.get_average(id=pk)
	flg=False
	gr=None
	if request.user.is_authenticated:
		if not Review.objects.filter(user=request.user,book=book):
			flg=True
		else:
			gr=Review.objects.filter(user=request.user,book=book)[0]
	total_views = r.incr('book:{}:views'.format(book.id))
	r.zincrby('book_ranking', book.id, 1)

	return render(request,'main/bookdetail.html',{'rating':ratings,'book':book,'total_views': total_views,'flg1':flg,'ur':gr})


'''def search(request):
	query_string = ''
	found_entries = None
	data={''}
	if request.method=='GET':
		submitbutton= request.GET.get('submit')
		if ('q' in request.GET) and request.GET['q'].strip():
			query_string = request.GET['q']
			entry_query = get_query(query_string, ['title','isbn'])
			results = Book.objects.filter(entry_query).distinct()
			data=serializers.serialize('json',results,fields=('title','author'))
			#context={'results':item,'submitbutton': submitbutton}
			#return render(request, 'main/search.html', context)
			return HttpResponse(data)
		else:
			return HttpResponse(data)
	else:
		return HttpResponse(data)'''




def booklist(request):
	books=Book.objects.order_by('-id').all()
	paginator=Paginator(books,5)
	page=request.GET.get('page')
	try:
		books=paginator.page(page)
	except PageNotAnInteger:
		books=paginator.page(1)
	except EmptyPage:
		if request.is_ajax():
			return HttpResponse('')
		images=paginator.page(paginator.num_pages)
	if request.is_ajax():
		return render(request,'main/book_list_ajax.html',{'books':books})
	return render(request,'main/home.html',{'books':books})
	 

def genrelist(request):
	genres=Genre.objects.order_by('name')
	return render(request,'main/genrelist.html',{'genres':genres})

def genredetail(request,pk):
	genre=Genre.objects.get(id=pk)
	count=genre.genred.count()

	return render(request,'main/genredetail.html',{'genre':genre,'count':count})

def authorlist(request):
	authors=Author.objects.order_by('name')
	return render(request,'main/authorlist.html',{'authors':authors})

def authordetail(request,pk):
	author=Author.objects.get(id=pk)
	return render(request,'main/authordetail.html',{'author':author})









@login_required
 
def like_review(request):
	review_id=None
	if request.method=='GET':
		review_id=request.GET.get('id');
		 
		likes=0
		if review_id:

			review=Review.objects.get(id=review_id)
			if not review.already_liked(request.user):
				review.vote(request.user)
				review.save()
				create_action(request.user, 'Liked review',review)
				likes=review.votes

	return HttpResponse(likes)

@login_required
def book_ranking_view(request):
	book_ranking = r.zrange('book_ranking', 0, -1,desc=True)[:10]
	book_ranking_ids = [int(id) for id in book_ranking]
	most_viewed = list(Book.objects.filter(id__in=book_ranking_ids))
	most_viewed.sort(key=lambda x: book_ranking_ids.index(x.id))
	return render(request,'main/bookrankingview.html',{'books':most_viewed})

class BookAutocomplete(autocomplete.Select2QuerySetView):
	def get_queryset(self):
		if not self.request.user.is_authenticated:
			return Book.objects.none()
		qs = Book.objects.all()
		if self.q:
			qs = qs.filter(name__icontains=self.q) | qs.filter(comNumber__icontains=self.q)

		return qs

def autocompleteModel(request):
	if request.is_ajax():
		q = request.GET.get('term', '')
		search_qs = Book.objects.filter(title__icontains=q) 
		results=[]
		print(q)
		for r in search_qs:
			results.append(r.title)
		data = json.dumps(results)
	else:
		data='fail'
	mimetype = 'application/json'
	return HttpResponse(data, mimetype)


		 
	

	 
def book_search(request):
	form=SearchForm()
	cd=None
	results=None
	total_results=None
	if 'query' in request.GET:
		print(request.GET.get('query'))
		form=SearchForm(request.GET)

		if form.is_valid():
			cd=form.cleaned_data
			results=SearchQuerySet().models(Book).filter(content=cd['query']).load_all()
			total_results=results.count()
	return render(request,'main/search.html',{'form':form,'cd':cd,'results':results,'total_results':total_results})

			 
'''
def search(request):
	 flg=False
	 if request.method == 'POST':
	 	search_text= request.POST.get('search_text')
	 else:
	 	search_text=''
	 entry_query = get_query(search_text, ['title','isbn'])
	 books = Book.objects.filter(entry_query).distinct()
	 if books.count() > 0:

	 return render(request,'main/ajax_search.html',{'books':books})
'''	 
#
#E:\solr-6.4.0\bin>/solr start -e cloud -noprompt

def search(request):
	flg=False
	if request.method == 'POST':
		search_text=request.POST.get('search_text')
	else:
		search_text=''
	#entry_query=get_query(search_text, ['title','isbn'])
	#books=Book.objects.filter(entry_query).distinct()
	books=Book.objects.filter(title__icontains=search_text)
	if books.count() == 0:
		flg=True
	return render(request,'main/ajax_search.html',{'books':books,'flg':flg})


@login_required
def add_review(request,pk):
	given=False
	if request.method == 'POST':
		f=ReviewForm(request.POST)

		if f.is_valid():
			new_review=f.save(commit=False)
			book=Book.objects.get(id=pk)
			user=request.user
			new_review.book=book
			new_review.user=user
			new_review.save()
			f.save()
			create_action(request.user, 'Added a review',new_review)
			messages.add_message(request, messages.INFO, 'Review added.')
			return redirect(new_review.get_absolute_url())
	else:
		f=ReviewForm()
	return render(request,'main/review_add.html',{'form':f})
