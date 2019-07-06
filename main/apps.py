from django.apps import AppConfig
from django import search as watson
 

class MainConfig(AppConfig):
    name = 'main'
    def ready(self):
    	book=self.get_model("Book")
    	watson.register(Book)


