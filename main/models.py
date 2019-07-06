from django.db import models
from django.core.validators import RegexValidator,MaxValueValidator,MinValueValidator
from django.urls import reverse

# Create your models here.
from users.models import CustomUser
 
# Register your models here.

#MyUser = apps.get_model('users', 'CustomUser')

class Author(models.Model):
	name=models.CharField(max_length=200)
	birth_place=models.CharField(max_length=200)
	website=models.URLField(max_length=300)
	twitter=models.URLField(max_length=300,validators=[RegexValidator(regex=r'https://twitter.com/[A-Za-z0-9_]+')])
	since = models.DateTimeField(auto_now_add=True)
	about=models.TextField()
	user=models.OneToOneField(CustomUser,on_delete=models.CASCADE)
	image = models.ImageField(upload_to='images/',default='images/placeholder.png')

	def __str__(self):
		return f'{self.name}'

	def get_absolute_url(self):
		return reverse('authordetail',args=[self.id])

class Publication(models.Model):
	name=models.CharField(max_length=200,unique=True)

	def __str__(self):
		return f'{self.name}'

class Genre(models.Model):
	name=models.CharField(max_length=200)

	def __str__(self):
		return f'{self.name}'

	def get_absolute_url(self):
		return reverse('genredetail',args=[self.id])



class BookManager(models.Manager):
	def get_average(self,id):
		r=self.get(id=id)
		count=r.reviews.count()
		if count == 0:
			return 0
		z=r.reviews
		a=len(z.filter(ratings__range=[0.0,1.0]))
		b=len(z.filter(ratings__range=[1.1,2.0]))
		c=len(z.filter(ratings__range=[2.1,3.0]))
		d=len(z.filter(ratings__range=[3.1,4.0]))
		e=len(z.filter(ratings__range=[4.1,5.0]))
		#rate=(a+b+c+d+e)
		rate=a+(b*2)+(c*2)+(d*4)+(e*5)
		
		count=r.reviews.count()
		rate/=count
		return rate





class Book(models.Model):
	title=models.CharField(max_length=200,unique=True)
	description=models.TextField()
	author=models.ManyToManyField(Author,related_name='authored')
	publication=models.ForeignKey(Publication,on_delete=models.CASCADE,related_name='published')
	genre=models.ManyToManyField(Genre,related_name='genred')
	pages=models.PositiveIntegerField()
	published=models.DateTimeField()
	image = models.ImageField(upload_to='images/',default='images/placeholder.png')
	isbn=models.CharField(max_length=300)
	amazon=models.URLField(max_length=400,default="https://www.amazon.com/")
	objects=BookManager()


	def __str__(self):
		return f'{self.title}'

	def get_absolute_url(self):
		return reverse('bookdetail', args=[self.id])

 


	



class Review(models.Model):

	user=models.ForeignKey(CustomUser,on_delete=models.CASCADE,related_name='reviews',blank=True, null=True)
	ratings=models.FloatField(validators=[MinValueValidator(0.0),MaxValueValidator(5.0)])
	detail=models.TextField()
	created=models.DateTimeField(auto_now_add=True)
	updated=models.DateTimeField(auto_now=True)
	active=models.BooleanField(default=True)
	book=models.ForeignKey(Book,on_delete=models.CASCADE,related_name='reviews')
	votes = models.IntegerField(db_index=True,default = 0)
	users_like=models.ManyToManyField(CustomUser,related_name='reviews_liked',blank=True)
	

	class Meta:
		ordering=('created',)
		unique_together = ('user', 'book')

	def __str__(self):
		return f'{self.user.email}'

	def get_absolute_url(self):
		return self.book.get_absolute_url()+'#review-'+str(self.id)

	def get_user(self):
		return f'{self.user}'

	def vote(self,user):
		try:
			self.review_votes.create(user=user,review=self)
			self.votes+=1
			self.users_like.add(user)
		except IntegrityError:
			return 'already upvoted'
		return 'ok'

	def already_liked(self,user):
		votes=self.review_votes.all()
		for v in votes:
			if v.user.username == user.username:
				return True
		else:
			return False




class Votes(models.Model):
	user=models.ForeignKey(CustomUser,on_delete=models.CASCADE,related_name='user_votes')
	review=models.ForeignKey(Review,on_delete=models.CASCADE,related_name='review_votes')

	class Meta:
		unique_together = ('user', 'review')


 