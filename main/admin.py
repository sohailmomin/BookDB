from django.contrib import admin
from .models import Book,Genre,Publication,Author,Review,Votes


admin.site.register(Book)
admin.site.register(Genre)
admin.site.register(Publication)
admin.site.register(Author)
admin.site.register(Review)
admin.site.register(Votes)
 
