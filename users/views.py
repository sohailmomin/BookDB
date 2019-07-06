from django.urls import reverse_lazy
from django.views import generic
from django.shortcuts import get_object_or_404,render
from .models import CustomUser,Contact
 
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.http import JsonResponse
from .forms import CustomUserCreationForm
from common.decorators import ajax_required
from actions.models import Action
from actions.utils import create_action

class SignUp(generic.CreateView):
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'registration/signup.html'

@login_required
def user_list(request):
	users=CustomUser.objects.order_by('username')
	return render(request,'users/user_list.html',{'users':users})

@login_required
def user_detail(request,username):
	user=get_object_or_404(CustomUser,username=username)
	return render(request,'users/user_detail.html',{'user':user})

@ajax_required
@require_POST
@login_required
def user_follow(request):
	
	user_id=request.POST.get('id')
	action=request.POST.get('action')


	if user_id and action:
		try:
			user=CustomUser.objects.get(id=user_id)
			if action == 'follow':
				Contact.objects.get_or_create(user_from=request.user,user_to=user)
				create_action(request.user, 'started following',user)
			else:
				Contact.objects.filter(user_from=request.user,user_to=user).delete()
			return JsonResponse({'status':'ok'})
		except CustomUser.DoesNotExist:
			return JsonResponse({'status':'ko'})
	return JsonResponse({'status':'ko'})




			 


@login_required
def  dashboard(request):
	actions = Action.objects.exclude(user=request.user)
	following_ids = request.user.following.values_list('id',flat=True)
	if following_ids:
		actions = actions.filter(user_id__in=following_ids)#.prefetch_related('target')

	actions = actions[:10]
	return render(request,'users/dashboard.html',{'actions':actions})


