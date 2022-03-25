from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView
from django.db.models import Q, F
from django.http import HttpResponse, HttpResponseNotFound
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView
import datetime
import reportlab
from reportlab.pdfgen import canvas
from io import BytesIO

from .utils import *

from .forms import *
from .models import *

main_menu = [{'title': 'Авторизация пользователя', 'url_name': 'login'},
             {'title': 'О системе', 'url_name': 'about'}
             ]

admin_menu = [{'title': 'Клиенты', 'url_name': 'doc_clients'},
              {'title': 'Заведения', 'url_name': 'doc_branches'},
              {'title': 'Товары и Услуги', 'url_name': 'doc_g_s'},
              {'title': 'Прейскурант с ценами', 'url_name': 'doc_price_list'},
              {'title': 'Поставщики', 'url_name': 'doc_suppliers'},
              {'title': 'Контракты', 'url_name': 'doc_contracts'},
              {'title': 'Мероприятия', 'url_name': 'doc_events'},
              {'title': 'Бронирования', 'url_name': 'doc_reservations'},
              {'title': 'Посещения', 'url_name': 'doc_visits'},
              {'title': 'Сотрудники', 'url_name': 'doc_stuff'},
              ]

rec_menu = [{'title': 'Клиенты', 'url_name': 'doc_clients'},
            {'title': 'Товары и Услуги', 'url_name': 'doc_g_s'},
            {'title': 'Прейскурант с ценами', 'url_name': 'doc_price_list'},
            {'title': 'Мероприятия', 'url_name': 'doc_events'},
            {'title': 'Бронирования', 'url_name': 'doc_reservations'},
            {'title': 'Посещения', 'url_name': 'doc_visits'},
            ]


def index(request):
    context = {
        'menu': main_menu,
        'title': 'Главная страница'
    }
    return render(request, 'main/index.html', context=context)


def about(request):
    return render(request, 'main/about.html', {'title': 'О системе'})


class RegisterUser(CreateView):
    form_class = RegisterUserForm
    template_name = 'main/register.html'
    success_url = reverse_lazy('main')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Регистрация'
        return context


class LoginUser(LoginView):
    form_class = LoginUserForm
    template_name = 'main/login.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Авторизация'
        return context

    def get_success_url(self):
        return reverse_lazy('menu_admin')


def logout_user(request):
    logout(request)
    return redirect('main')


def main_page(request):
    menu = admin_menu
    if request.user.groups.filter(name='rec').exists():
        menu = rec_menu
    context = {
        'menu': menu,
        'title': 'Главное меню'
    }
    return render(request, 'main/menu_page.html', context=context)


def doc_clients(request):
    open_form = 0
    only_view = 0
    form = AddClientForm()
    search_form = SearchForm()
    clients = Clients.objects.all()
    # if request.user.groups.filter(name='rec').exists():
    #     b = request.user.branch_set.first()
    #     clients = Clients.objects.filter(visits__branch=b)
    if request.method == 'POST':
        if 'fio' in request.POST:
            form = AddClientForm(request.POST, request.FILES)
            if form.is_valid():
                form.save()
            else:
                open_form = 1
        elif 'search' in request.POST:
            search_form = SearchForm(request.POST)
            clients = Clients.objects.filter(Q(fio__icontains=search_form.data['search']) |
                                             Q(e_mail__icontains=search_form.data['search']) |
                                             Q(phone__icontains=search_form.data['search']) |
                                             Q(registration_date__icontains=search_form.data['search']))
    context = make_context('Журнал Клиентов', form, clients, open_form, search_form, only_view=only_view)
    return render(request, 'main/clients.html', context=context)


def show_client(request, client_slug):
    client = get_object_or_404(Clients, slug=client_slug)
    open_form = 0
    form = AddClientForm(instance=client)
    del_form = DelForm()
    if request.method == 'POST':
        if 'fio' in request.POST:
            form = AddClientForm(request.POST, request.FILES, instance=client)
            if form.is_valid():
                open_form = 0
                form.save()
            else:
                open_form = 1
        elif 'delete' in request.POST:
            del_form = DelForm(request.POST)
            client.delete()
            return redirect('doc_clients')
    context = make_context(client.fio, form, client, open_form, del_form=del_form)
    return render(request, 'main/client.html', context=context)


def doc_branches(request):
    open_form = 0
    only_view = 0
    form = AddBranchForm()
    search_form = SearchForm()
    branches = Branch.objects.all()
    if request.method == 'POST':
        if 'address' in request.POST:
            form = AddBranchForm(request.POST, request.FILES)
            if form.is_valid():
                form.save()
            else:
                open_form = 1
        elif 'search' in request.POST:
            search_form = SearchForm(request.POST)
            branches = Branch.objects.filter(Q(address__icontains=search_form.data['search']) |
                                             Q(phone__icontains=search_form.data['search']) |
                                             Q(registration_date__icontains=search_form.data['search']) |
                                             Q(user__username__icontains=search_form.data['search']))
    context = make_context('База заведений', form, branches, open_form, search_form, only_view=only_view)
    return render(request, 'main/branches.html', context=context)


def show_branch(request, branch_slug):
    branch = get_object_or_404(Branch, slug=branch_slug)
    only_view = 0
    open_form = 0
    form = AddBranchForm(instance=branch)
    del_form = DelForm()
    if request.method == 'POST':
        if 'address' in request.POST:
            form = AddBranchForm(request.POST, request.FILES, instance=branch)
            if form.is_valid():
                open_form = 0
                form.save()
            else:
                open_form = 1
        elif 'delete' in request.POST:
            del_form = DelForm(request.POST)
            branch.delete()
            return redirect('doc_branches')
    context = make_context(branch.address, form, branch, open_form, del_form=del_form, only_view=only_view)
    return render(request, 'main/branch.html', context=context)


def doc_g_s(request):
    open_form = 0
    only_view = 0
    form = AddGoodsAndServicesForm()
    search_form = SearchForm()
    g_s = GoodsAndServices.objects.all()
    if request.user.groups.filter(name='rec').exists():
        b = request.user.branch_set.first()
        g_s = GoodsAndServices.objects.filter(branch=b)
        only_view = 1
    if request.method == 'POST':
        if 'name' in request.POST:
            form = AddGoodsAndServicesForm(request.POST, request.FILES)
            if form.is_valid():
                form.save()
            else:
                open_form = 1
        elif 'search' in request.POST:
            search_form = SearchForm(request.POST)
            g_s = GoodsAndServices.objects.filter(Q(name__icontains=search_form.data['search']) |
                                                  Q(group__icontains=search_form.data['search']) |
                                                  Q(remaining_quantity__icontains=search_form.data['search']) |
                                                  Q(branch__address__icontains=search_form.data['search']))
            if request.user.groups.filter(name='rec').exists():
                b = request.user.branch_set.first()
                g_s = GoodsAndServices.objects.filter((Q(name__icontains=search_form.data['search']) |
                                                       Q(group__icontains=search_form.data['search']) |
                                                       Q(remaining_quantity__icontains=search_form.data['search']) |
                                                       Q(branch__address__icontains=search_form.data['search'])) &
                                                      Q(branch=b))
    context = make_context('Журнал Товаров и Услуг', form, g_s, open_form, search_form, only_view=only_view)
    return render(request, 'main/goods_services.html', context=context)


def show_g_s(request, g_s_slug):
    g_s = get_object_or_404(GoodsAndServices, slug=g_s_slug)
    open_form = 0
    only_view = 0
    if request.user.groups.filter(name='rec').exists():
        only_view = 1
    form = AddGoodsAndServicesForm(instance=g_s)
    del_form = DelForm()
    if request.method == 'POST':
        if 'name' in request.POST:
            form = AddGoodsAndServicesForm(request.POST, request.FILES, instance=g_s)
            if form.is_valid():
                open_form = 0
                form.save()
            else:
                open_form = 1
        elif 'delete' in request.POST:
            del_form = DelForm(request.POST)
            g_s.delete()
            return redirect('doc_g_s')
    context = make_context(g_s.name, form, g_s, open_form, del_form=del_form, only_view=only_view)
    return render(request, 'main/good_or_service.html', context=context)


def doc_price_list(request):
    open_form = 0
    only_view = 0
    form = AddPriceListForm()
    search_form = SearchForm()
    price_list = PriceList.objects.all()
    if request.user.groups.filter(name='rec').exists():
        b = request.user.branch_set.first()
        price_list = PriceList.objects.filter(good_or_service__branch=b)
        only_view = 1
    if request.method == 'POST':
        if 'price' in request.POST:
            form = AddPriceListForm(request.POST, request.FILES)
            if form.is_valid():
                form.save()
            else:
                open_form = 1
        elif 'search' in request.POST:
            search_form = SearchForm(request.POST)
            price_list = PriceList.objects.filter(Q(good_or_service__name__icontains=search_form.data['search']) |
                                                  Q(price__icontains=search_form.data['search']))
            if request.user.groups.filter(name='rec').exists():
                b = request.user.branch_set.first()
                price_list = PriceList.objects.filter((Q(good_or_service__name__icontains=search_form.data['search']) |
                                                       Q(price__icontains=search_form.data['search'])) &
                                                      Q(good_or_service__branch=b))
    context = make_context('Прейскурант с ценами', form, price_list, open_form, search_form, only_view=only_view)
    return render(request, 'main/price_list.html', context=context)


def show_price_list(request, price_list_slug):
    price_list_note = get_object_or_404(PriceList, slug=price_list_slug)
    open_form = 0
    only_view = 0
    if request.user.groups.filter(name='rec').exists():
        only_view = 1
    form = AddPriceListForm(instance=price_list_note)
    del_form = DelForm()
    if request.method == 'POST':
        if 'price' in request.POST:
            form = AddPriceListForm(request.POST, request.FILES, instance=price_list_note)
            if form.is_valid():
                open_form = 0
                form.save()
            else:
                open_form = 1
        elif 'delete' in request.POST:
            del_form = DelForm(request.POST)
            price_list_note.delete()
            return redirect('doc_price_list')
    context = make_context(price_list_note.good_or_service.name, form, price_list_note, open_form, del_form=del_form,
                           only_view=only_view)
    return render(request, 'main/price_list_note.html', context=context)


def doc_suppliers(request):
    open_form = 0
    only_view = 0
    form = AddSuppliersForm()
    search_form = SearchForm()
    suppliers = Suppliers.objects.all()
    if request.method == 'POST':
        if 'fio' in request.POST:
            form = AddSuppliersForm(request.POST, request.FILES)
            if form.is_valid():
                form.save()
            else:
                open_form = 1
        elif 'search' in request.POST:
            search_form = SearchForm(request.POST)
            suppliers = Suppliers.objects.filter(Q(fio__icontains=search_form.data['search']) |
                                             Q(inn__icontains=search_form.data['search']) |
                                             Q(phone__icontains=search_form.data['search']) |
                                             Q(e_mail__icontains=search_form.data['search']))
    context = make_context('База поставщиков', form, suppliers, open_form, search_form=search_form,
                           only_view=only_view)
    return render(request, 'main/suppliers.html', context=context)


def show_supplier(request, supplier_slug):
    supplier = get_object_or_404(Suppliers, slug=supplier_slug)
    open_form = 0
    only_view = 0
    form = AddSuppliersForm(instance=supplier)
    del_form = DelForm()
    if request.method == 'POST':
        if 'fio' in request.POST:
            form = AddSuppliersForm(request.POST, request.FILES, instance=supplier)
            if form.is_valid():
                open_form = 0
                form.save()
            else:
                open_form = 1
        elif 'delete' in request.POST:
            del_form = DelForm(request.POST)
            supplier.delete()
            return redirect('doc_suppliers')
    context = make_context(supplier.fio, form, supplier, open_form, del_form=del_form, only_view=only_view)
    return render(request, 'main/supplier.html', context=context)


def doc_contracts(request):
    open_form = 0
    only_view = 0
    form = AddContractsForm()
    search_form = SearchForm()
    contracts = Contracts.objects.all()
    if request.method == 'POST':
        if 'good_or_service' in request.POST:
            form = AddContractsForm(request.POST, request.FILES)
            if form.is_valid():
                form.save()
            else:
                open_form = 1
        elif 'search' in request.POST:
            search_form = SearchForm(request.POST)
            contracts = Contracts.objects.filter(Q(good_or_service__name__icontains=search_form.data['search']) |
                                                 Q(supplier__fio__icontains=search_form.data['search']) |
                                                 Q(price__icontains=search_form.data['search']))
    context = make_context('Папка контрактов с поставщиками', form, contracts, open_form, search_form=search_form,
                           only_view=only_view)
    return render(request, 'main/contracts.html', context=context)


def show_contract(request, contract_slug):
    contract = get_object_or_404(Contracts, slug=contract_slug)
    open_form = 0
    only_view = 0
    form = AddContractsForm(instance=contract)
    del_form = DelForm()
    if request.method == 'POST':
        if 'good_or_service' in request.POST:
            form = AddContractsForm(request.POST, request.FILES, instance=contract)
            if form.is_valid():
                open_form = 0
                form.save()
            else:
                open_form = 1
        elif 'delete' in request.POST:
            del_form = DelForm(request.POST)
            contract.delete()
            return redirect('doc_contracts')
    context = make_context(contract.good_or_service, form, contract, open_form, del_form=del_form, only_view=only_view)
    return render(request, 'main/contract.html', context=context)


def doc_events(request):
    open_form = 0
    only_view = 0
    form = AddEventsForm()
    search_form = SearchForm()
    events = Events.objects.all()
    if request.user.groups.filter(name='rec').exists():
        b = request.user.branch_set.first()
        events = Events.objects.filter(branch=b)
        only_view = 1
    if request.method == 'POST':
        if 'name' in request.POST:
            form = AddEventsForm(request.POST, request.FILES)
            if form.is_valid():
                open_form = 0
                form.save()
            else:
                open_form = 1
        elif 'search' in request.POST:
            search_form = SearchForm(request.POST)
            events = Events.objects.filter(Q(name__icontains=search_form.data['search']) |
                                           Q(date_time_of_event__icontains=search_form.data['search']) |
                                           Q(branch__address__icontains=search_form.data['search']))
            if request.user.groups.filter(name='rec').exists():
                b = request.user.branch_set.first()
                events = Events.objects.filter((Q(name__icontains=search_form.data['search']) |
                                                Q(date_time_of_event__icontains=search_form.data[
                                                    'search']) |
                                                Q(branch__address__icontains=search_form.data['search'])) &
                                               Q(branch=b))
    context = make_context('Журнал Мероприятий', form, events, open_form, search_form, only_view=only_view)
    return render(request, 'main/events.html', context=context)


def show_event(request, event_slug):
    event = get_object_or_404(Events, slug=event_slug)
    open_form = 0
    only_view = 0
    if request.user.groups.filter(name='rec').exists():
        only_view = 1
    form = AddEventsForm(instance=event)
    del_form = DelForm()
    if request.method == 'POST':
        if 'name' in request.POST:
            form = AddEventsForm(request.POST, request.FILES, instance=event)
            if form.is_valid():
                open_form = 0
                form.save()
            else:
                open_form = 1
        elif 'delete' in request.POST:
            del_form = DelForm(request.POST)
            event.delete()
            return redirect('doc_events')
    context = make_context(event.name, form, event, open_form, del_form=del_form,
                           only_view=only_view)
    return render(request, 'main/event.html', context=context)


def doc_reservations(request):
    open_form = 0
    only_view = 0
    form = AddReservationsForm()
    search_form = SearchForm()
    reservations = Reservations.objects.all()
    if request.user.groups.filter(name='rec').exists():
        b = request.user.branch_set.first()
        reservations = Reservations.objects.filter(branch=b)
    if request.method == 'POST':
        if 'client_name' in request.POST:
            form = AddReservationsForm(request.POST, request.FILES)
            if form.is_valid():
                try:
                    r = Reservations.objects.create(**form.cleaned_data)
                    if r.event is not None:
                        if r.num_of_persons + r.event.current_num_of_participants > r.event.max_num_of_participants:
                            m = r.event.max_num_of_participants - r.event.current_num_of_participants
                            r.delete()
                            form.add_error(None, f'Мест на мероприятии осталось: {m}')
                            open_form = 1
                        else:
                            r.event.current_num_of_participants = r.event.current_num_of_participants + r.num_of_persons
                            r.event.save()
                except:
                    form.add_error(None, 'Ошибка добавления формы')
                    open_form = 1
                # open_form = 0
                # form.save()
            else:
                open_form = 1
        elif 'search' in request.POST:
            search_form = SearchForm(request.POST)
            reservations = Reservations.objects.filter(Q(client_name__icontains=search_form.data['search']) |
                                                       Q(object_of_reservation__icontains=search_form.data['search']) |
                                                       Q(date_time_of_reservation__icontains=search_form.data[
                                                           'search']) |
                                                       Q(branch__address__icontains=search_form.data['search']))
            if request.user.groups.filter(name='rec').exists():
                b = request.user.branch_set.first()
                reservations = Reservations.objects.filter((Q(client_name__icontains=search_form.data['search']) |
                                                            Q(object_of_reservation__icontains=search_form.data[
                                                                'search']) |
                                                            Q(date_time_of_reservation__icontains=search_form.data[
                                                                'search']) |
                                                            Q(branch__address__icontains=search_form.data['search'])) &
                                                           Q(branch=b))
    context = make_context('Журнал Бронирований', form, reservations, open_form, search_form, only_view=only_view)
    return render(request, 'main/reservations.html', context=context)


def show_reservation(request, reservation_slug):
    reservation = get_object_or_404(Reservations, slug=reservation_slug)
    open_form = 0
    only_view = 0
    form = AddReservationsForm(instance=reservation)
    del_form = DelForm()
    if request.method == 'POST':
        if 'client_name' in request.POST:
            form = AddReservationsForm(request.POST, request.FILES, instance=reservation)
            if form.is_valid():
                # try:
                #     if form.cleaned_data['event'] is not None:
                #         print(form.cleaned_data['num_of_persons'])
                #         print(reservation.event.current_num_of_participants)
                #         print(reservation.num_of_persons)
                #         if form.cleaned_data['num_of_persons'] + reservation.event.current_num_of_participants - reservation.num_of_persons > reservation.event.max_num_of_participants:
                #             m = reservation.event.max_num_of_participants - reservation.event.current_num_of_participants + reservation.num_of_persons
                #             print(form.cleaned_data['num_of_persons'])
                #             print(form.cleaned_data['m'])
                #             form.add_error(None, f'Мест на мероприятии осталось: {m}')
                #             open_form = 1
                #         else:
                #             reservation.event.current_num_of_participants = reservation.event.current_num_of_participants - reservation.num_of_persons + form.cleaned_data['num_of_persons']
                #             reservation.event.save()
                #     form.save()
                # except:
                #     form.add_error(None, 'Ошибка добавления формы')
                #     open_form = 1
                open_form = 0
                form.save()
            else:
                open_form = 1
        elif 'delete' in request.POST:
            del_form = DelForm(request.POST)
            if reservation.event is not None:
                reservation.event.current_num_of_participants = reservation.event.current_num_of_participants - reservation.num_of_persons
                reservation.event.save()
            reservation.delete()
            return redirect('doc_reservations')
    context = make_context(reservation.date_time_of_reservation, form, reservation, open_form, del_form=del_form,
                           only_view=only_view)
    return render(request, 'main/reservation.html', context=context)


def doc_visits(request):
    open_form = 0
    only_view = 0
    form = AddVisitsForm()
    search_form = SearchForm()
    visits = Visits.objects.all()
    if request.user.groups.filter(name='rec').exists():
        b = request.user.branch_set.first()
        visits = Visits.objects.filter(branch=b)
    if request.method == 'POST':
        if 'date_of_visit' in request.POST:
            form = AddVisitsForm(request.POST, request.FILES)
            if form.is_valid():
                open_form = 0
                visit = form.save(commit=False)
                visit.client.activity_indicator = F('activity_indicator') + 1
                visit.client.save()
                visit.save()
            else:
                open_form = 1
        elif 'search' in request.POST:
            search_form = SearchForm(request.POST)
            visits = Visits.objects.filter(Q(date_of_visit__icontains=search_form.data['search']) |
                                           Q(client__fio__icontains=search_form.data['search']) |
                                           Q(goods_and_services__icontains=search_form.data[
                                               'search']) |
                                           Q(branch__address__icontains=search_form.data['search']))
            if request.user.groups.filter(name='rec').exists():
                b = request.user.branch_set.first()
                visits = Visits.objects.filter((Q(date_of_visit__icontains=search_form.data['search']) |
                                                Q(client__fio__icontains=search_form.data['search']) |
                                                Q(goods_and_services__icontains=search_form.data[
                                                    'search']) |
                                                Q(branch__address__icontains=search_form.data['search'])) &
                                               Q(branch=b))
    context = make_context('Журнал Посещений', form, visits, open_form, search_form, only_view=only_view)
    return render(request, 'main/visits.html', context=context)


def show_visit(request, visit_slug):
    visit = get_object_or_404(Visits, slug=visit_slug)
    open_form = 0
    only_view = 0
    form = AddVisitsForm(instance=visit)
    del_form = DelForm()
    if request.method == 'POST':
        if 'date_of_visit' in request.POST:
            form = AddVisitsForm(request.POST, request.FILES, instance=visit)
            if form.is_valid():
                new_cleaned_data = payment_price_count(form)
                open_form = 0
                visit_up = form.save(commit=False)
                visit_up.payment_price = new_cleaned_data['payment_price']
                visit_up.save()
            else:
                open_form = 1
        elif 'delete' in request.POST:
            del_form = DelForm(request.POST)
            visit.delete()
            return redirect('doc_visits')
    context = make_context(visit.date_of_visit, form, visit, open_form, del_form=del_form,
                           only_view=only_view)
    return render(request, 'main/visit.html', context=context)


def doc_stuff(request):
    open_form = 0
    only_view = 0
    form = AddStaffForm()
    search_form = SearchForm()
    stuff = Staff.objects.all()
    if request.method == 'POST':
        if 'last_name' in request.POST:
            form = AddStaffForm(request.POST, request.FILES)
            if form.is_valid():
                form.save()
            else:
                open_form = 1
        elif 'search' in request.POST:
            search_form = SearchForm(request.POST)
            stuff = Staff.objects.filter(Q(last_name__icontains=search_form.data['search']) |
                                         Q(first_name__icontains=search_form.data['search']) |
                                         Q(patronymic__icontains=search_form.data['search']) |
                                         Q(phone__icontains=search_form.data['search']) |
                                         Q(branch__address__icontains=search_form.data['search']))
    context = make_context('Папка личных дел Сотрудников', form, stuff, open_form, search_form=search_form,
                           only_view=only_view)
    return render(request, 'main/stuff.html', context=context)


def show_stuff(request, stuff_slug):
    stuff = get_object_or_404(Staff, slug=stuff_slug)
    open_form = 0
    only_view = 0
    form = AddStaffForm(instance=stuff)
    del_form = DelForm()
    if request.method == 'POST':
        if 'last_name' in request.POST:
            form = AddStaffForm(request.POST, request.FILES, instance=stuff)
            if form.is_valid():
                open_form = 0
                form.save()
            else:
                open_form = 1
        elif 'delete' in request.POST:
            del_form = DelForm(request.POST)
            stuff.delete()
            return redirect('doc_stuff')
    context = make_context(stuff.last_name, form, stuff, open_form, del_form=del_form, only_view=only_view)
    return render(request, 'main/stuff_person.html', context=context)


def pageNotFound(request, exception):
    return HttpResponseNotFound('<h1>Страница не найдена!</h1>')
