from django.urls import path,reverse,re_path
from . import views
from django.views.generic.base import TemplateView
from .views import BookAutocomplete

urlpatterns=[
        
        path('', views.booklist, name='home'),
		path('bookdetail/<int:pk>',views.bookdetail,name='bookdetail'),
		path('search/',views.search,name='search'),
		path('genrelist/',views.genrelist,name='genrelist'),
		path('genredetail/<int:pk>',views.genredetail,name='genredetail'),
		path('authorlist/',views.authorlist,name='authorlist'),
		path('authordetail/<int:pk>',views.authordetail,name='authordetail'),
		path('like/',views.like_review,name='like_review'),
		path('bookviewrank/',views.book_ranking_view,name='book_ranking_view'),
		re_path(r'^country-autocomplete/$',BookAutocomplete.as_view(),name='book-autocomplete'),
		path('ajax_calls/search/',views.autocompleteModel,name='book_auto'),
		path('searchbooks/',views.book_search,name='searchbooks'),
		path('add_review/<int:pk>',views.add_review,name='review_add'),
		 

]