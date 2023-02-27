from django.http import HttpResponse, JsonResponse
from django.template import loader
from .controllers.broker_controller import BrokerController
import telebot
from telebot import util

def home(request):
    template = loader.get_template('home.html')
    return HttpResponse(template.render())



def get_recs(request):
    # my_data = request.POST.get('my_data')
    # Call your Python function here
    bc = BrokerController()
    print('obtaining pos.. ')
    pos = bc.get_my_open_pos()
    print('obtained open pos! ')
    
    print('calculating recommended actions.. ')
    pos_with_recommendations = bc.get_my_recommended_actions(pos)
    print('obtained recommended actions!')
    
    return JsonResponse({'result': pos_with_recommendations})

def send_tele(request):
    output_msg = 'hi'
    # for pos in pos_with_recommendations:
    #     if pos.get('recommendation') is not None:
    #         output_msg = output_msg + '\n' + pos.get('recommendation') + ' at ' + str(pos.get('stop_loss')) + ', reason: ' + pos.get('reason') 

    print('sending to telegram..')
    bot=telebot.TeleBot("5244204118:AAFLg6BjMqgfv6WNclKVDaIEgKcZhPnK818")
    bot.send_message(27392018, output_msg)
    return JsonResponse({'result': 'success'})