from django import template
from main.models import *

register = template.Library()


# @register.inclusion_tag('main/index.html')
# def show_main_menu():
#     menu = [{'title': 'Администратор', 'url_name': 'autor_admin'},
#             {'title': 'Сотрудник рецепции', 'url_name': 'autor_rec'},
#             {'title': 'О системе', 'url_name': 'about'}
#             ]
#     return {'menu': menu}


# @register.simple_tag()
# def is_rec_user(user):
#     return user.groups.filter(name='rec').exists()

# @register.simple_tag()
# def get_client_form_filds():
#     return



# @register.inclusion_tag('main/clients.html')
# def show_clients():
#     clients = Clients.objects.all()
#     return {'clients': clients}
