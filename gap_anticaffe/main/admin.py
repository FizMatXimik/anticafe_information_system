from django.contrib import admin

from .models import *


class ClientsAdmin(admin.ModelAdmin):
    list_display = ('id', 'fio', 'birth_date', 'address', 'phone', 'e_mail', 'registration_date', 'activity_indicator')
    list_display_links = ('id', 'fio')
    search_fields = ('fio',)
    prepopulated_fields = {'slug': ('fio',)}


class BranchAdmin(admin.ModelAdmin):
    list_display = ('id', 'address', 'phone', 'registration_date')
    list_display_links = ('id', 'address')
    search_fields = ('address', 'phone')
    prepopulated_fields = {'slug': ('address',)}


class GoodsAndServicesAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'group', 'description', 'remaining_quantity', 'branch')
    list_display_links = ('id', 'name')
    list_filter = ('branch',)
    search_fields = ('name', 'group', 'description')
    prepopulated_fields = {'slug': ('name',)}


class PriceListAdmin(admin.ModelAdmin):
    list_display = ('good_or_service', 'price')
    list_display_links = ('good_or_service',)
    search_fields = ('good_or_service',)
    prepopulated_fields = {'slug': ('good_or_service',)}



class SuppliersAdmin(admin.ModelAdmin):
    list_display = ('id', 'fio', 'inn', 'phone', 'e_mail', 'registration_date')
    list_display_links = ('id', 'fio', 'inn')
    search_fields = ('fio', 'inn')
    prepopulated_fields = {'slug': ('fio', 'inn',)}


class ContractsAdmin(admin.ModelAdmin):
    list_display = ('id', 'good_or_service', 'supplier', 'quantity', 'price', 'delivery_schedule')
    list_display_links = ('id', 'good_or_service')
    search_fields = ('good_or_service', 'supplier')
    prepopulated_fields = {'slug': ('good_or_service', 'supplier',)}


class EventsAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'description', 'date_time_of_event', 'max_num_of_participants', 'current_num_of_participants', 'price', 'branch')
    list_display_links = ('id', 'name')
    search_fields = ('name', 'description')
    prepopulated_fields = {'slug': ('name',)}


class ReservationsAdmin(admin.ModelAdmin):
    list_display = ('id', 'date_time_of_reservation', 'client_name', 'object_of_reservation', 'event', 'table_num', 'branch', 'num_of_persons')
    list_display_links = ('id', 'date_time_of_reservation')
    search_fields = ('date_time_of_reservation', 'client_name')
    prepopulated_fields = {'slug': ('date_time_of_reservation', 'client_name',)}


class VisitsAdmin(admin.ModelAdmin):
    list_display = ('id', 'date_of_visit', 'client', 'goods_and_services', 'is_reserved', 'reservation', 'time_start', 'time_end', 'payment_price', 'branch')
    list_display_links = ('id', 'date_of_visit', 'client')
    search_fields = ('date_of_visit', 'client')
    prepopulated_fields = {'slug': ('date_of_visit', 'client',)}


class StaffAdmin(admin.ModelAdmin):
    list_display = ('id', 'last_name', 'first_name', 'patronymic', 'birth_date', 'address', 'phone', 'e_mail', 'registration_date', 'num_of_employment_contract', 'duration_of_contract', 'salary', 'branch')
    list_display_links = ('id', 'last_name', 'num_of_employment_contract')
    search_fields = ('last_name', 'num_of_employment_contract')
    prepopulated_fields = {'slug': ('last_name', 'first_name',)}


admin.site.register(Clients, ClientsAdmin)
admin.site.register(Branch, BranchAdmin)
admin.site.register(GoodsAndServices, GoodsAndServicesAdmin)
admin.site.register(PriceList, PriceListAdmin)
admin.site.register(Suppliers, SuppliersAdmin)
admin.site.register(Contracts, ContractsAdmin)
admin.site.register(Events, EventsAdmin)
admin.site.register(Reservations, ReservationsAdmin)
admin.site.register(Visits, VisitsAdmin)
admin.site.register(Staff, StaffAdmin)

