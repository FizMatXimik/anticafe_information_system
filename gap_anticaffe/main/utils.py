import datetime

from django.shortcuts import get_object_or_404

from main.models import *


def make_context(title, form, note, open_form, search_form=None, del_form=None, only_view=0):
    context = {
        'title': title,
        'form': form,
        'search_form': search_form,
        'del_form': del_form,
        'note': note,
        'open_form': open_form,
        'only_view': only_view
    }
    return context


def payment_price_count(form):
    if form.cleaned_data['time_end'] is not None:
        form.cleaned_data['payment_price'] = 0
        for i in form.cleaned_data['goods_and_services'].split(','):
            if 'Товар' in i or 'Услуга' in i:
                g_s = int(i.split(':')[1])
                if get_object_or_404(GoodsAndServices, pk=g_s).name == 'Основной тариф':
                    time = datetime.datetime.strptime(str(form.cleaned_data['time_end']),
                                                      '%H:%M:%S') - datetime.datetime.strptime(
                        str(form.cleaned_data['time_start']), '%H:%M:%S')
                    form.cleaned_data['payment_price'] += get_object_or_404(PriceList, good_or_service__pk=g_s).price * (
                            time.total_seconds() // 60)
                else:
                    form.cleaned_data['payment_price'] += get_object_or_404(PriceList, good_or_service__pk=g_s).price
            elif 'Мероприятие' in i:
                event = i.split(':')[1]
                form.cleaned_data['payment_price'] += get_object_or_404(Events, pk=event).price
    return form.cleaned_data
