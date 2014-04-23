from django.shortcuts import render,render_to_response
from django.http import HttpResponse
from models import BoxNumber
from Utilities import Utilities 

def game(request):
	message_xy = ""
	message_num = ""
	preference = ""
	if 'user_preference' in request.GET:
		Utilities().reset_game()
		preference = request.GET['user_preference']
		if ((preference=='y') or(preference=='Y')):
			if preference=='y':
				preference = 'Y'
			Utilities().insert_preference(preference)
			Utilities().first_move()
			message_num = "Game is in progress"
		elif ((preference=='x') or(preference=='X')):
			preference = 'X'
			Utilities().insert_preference(preference)
		else:
			preference = 'X'
			message_xy = "please enter either x or y, if you are seeing this message then we assume your preference is X"
			Utilities().insert_preference(preference)
		print preference
	preference = Utilities().get_preference()
	if 'user_input' in request.GET:
		print 'user input received'
		message_num = Utilities().call_to_ai_for_new_value(request.GET['user_input'])	
	boxvalues1 = BoxNumber.objects.all()[:3]
	boxvalues2 = BoxNumber.objects.all()[3:6]
	boxvalues3 = BoxNumber.objects.all()[6:9]
	return render_to_response('index.html',{'BoxNumber1':boxvalues1,'BoxNumber2':boxvalues2,'BoxNumber3':boxvalues3,'preference':preference,'message_xy':message_xy,'message_num':message_num})

# Create your views here.
