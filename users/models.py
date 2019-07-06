# users/models.py
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.urls import reverse


class CustomUser(AbstractUser):
    # add additional fields in here
    age = models.PositiveIntegerField(null=True, blank=True)
    is_author=models.BooleanField(default=False)
    following=models.ManyToManyField('self',through='Contact',related_name='followers',symmetrical=False)
    image=models.ImageField(upload_to='images/',default='images/placeholder.png')

    def get_absolute_url(self):
    	return reverse('user_detail', args=[self.username])

    def __str__(self):
        return self.email



class Contact(models.Model):
	user_from=models.ForeignKey(CustomUser,related_name='rel_from_set',on_delete=models.CASCADE)
	user_to=models.ForeignKey(CustomUser,related_name='rel_to_set',on_delete=models.CASCADE)
	created=models.DateTimeField(auto_now_add=True,db_index=True)

	class Meta:
		ordering=['-created']

	def __str__(self):
		return f'{self.user_from} follows {self.user_to}'