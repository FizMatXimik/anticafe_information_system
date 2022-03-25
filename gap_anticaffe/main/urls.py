from django.urls import path
from .views import *

urlpatterns = [
    path('', index, name='main'),
    path('about/', about, name='about'),
    path('login/', LoginUser.as_view(), name='login'),
    path('logout/', logout_user, name='logout'),
    path('register/', RegisterUser.as_view(), name='register'),
    path('menu/', main_page, name='menu_admin'),
    path('doc_clients/', doc_clients, name='doc_clients'),
    path('doc_clients/<slug:client_slug>/', show_client, name='client'),
    path('doc_branches/', doc_branches, name='doc_branches'),
    path('doc_branches/<slug:branch_slug>/', show_branch, name='branch'),
    path('doc_g_s/', doc_g_s, name='doc_g_s'),
    path('doc_g_s/<slug:g_s_slug>/', show_g_s, name='g_s'),
    path('doc_price_list/', doc_price_list, name='doc_price_list'),
    path('doc_price_list/<slug:price_list_slug>/', show_price_list, name='price_list'),
    path('doc_suppliers/', doc_suppliers, name='doc_suppliers'),
    path('doc_suppliers/<slug:supplier_slug>/', show_supplier, name='supplier'),
    path('doc_contracts/', doc_contracts, name='doc_contracts'),
    path('doc_contracts/<slug:contract_slug>/', show_contract, name='contract'),
    path('doc_events/', doc_events, name='doc_events'),
    path('doc_events/<slug:event_slug>/', show_event, name='event'),
    path('doc_reservations/', doc_reservations, name='doc_reservations'),
    path('doc_reservations/<slug:reservation_slug>/', show_reservation, name='reservation'),
    path('doc_visits/', doc_visits, name='doc_visits'),
    path('doc_visits/<slug:visit_slug>/', show_visit, name='visit'),
    path('doc_stuff/', doc_stuff, name='doc_stuff'),
    path('doc_stuff/<slug:stuff_slug>/', show_stuff, name='stuff'),

]