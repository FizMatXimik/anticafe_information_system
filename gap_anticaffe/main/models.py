from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse


class Clients(models.Model):
    fio = models.CharField(max_length=100, verbose_name='ФИО')
    slug = models.SlugField(max_length=255, unique=True, db_index=True, verbose_name="URL")
    birth_date = models.DateField(blank=True, verbose_name='Дата рождения')
    address = models.CharField(max_length=100, blank=True, verbose_name='Домашний адрес')
    phone = models.CharField(max_length=20, verbose_name='Телефон')
    e_mail = models.CharField(max_length=100, blank=True, verbose_name='E-mail')
    photo = models.ImageField(upload_to="photos/%Y/%m/%d/", null=True)
    registration_date = models.DateField(auto_now_add=True, verbose_name='Дата регистрации')
    activity_indicator = models.IntegerField(default=1, verbose_name='Показатель активности')

    def __str__(self):
        return self.fio

    def get_absolute_url(self):
        return reverse('client', kwargs={'client_slug': self.slug})

    class Meta:
        app_label = "main"
        managed = True
        verbose_name = 'Клиент'
        verbose_name_plural = 'Клиенты'
        ordering = ['fio']


class Branch(models.Model):
    address = models.CharField(max_length=100, verbose_name='Адрес')
    slug = models.SlugField(max_length=255, unique=True, db_index=True, verbose_name="URL")
    phone = models.CharField(max_length=20, verbose_name='Телефон')
    registration_date = models.DateField(auto_now_add=True, verbose_name='Дата регистрации')
    user = models.ForeignKey(User, on_delete=models.PROTECT, verbose_name='Пользователь', blank=True, null=True)

    def __str__(self):
        return self.address

    def get_absolute_url(self):
        return reverse('branch', kwargs={'branch_slug': self.slug})

    class Meta:
        app_label = "main"
        managed = True
        verbose_name = 'Заведение'
        verbose_name_plural = 'Заведения'
        ordering = ['address']


class GoodsAndServices(models.Model):
    name = models.CharField(max_length=100, db_index=True, verbose_name='Наименование')
    slug = models.SlugField(max_length=255, unique=True, db_index=True, verbose_name="URL")
    group = models.CharField(max_length=100, blank=True, verbose_name='Группа')
    description = models.TextField(blank=True, verbose_name='Описание')
    remaining_quantity = models.IntegerField(verbose_name='Осталось')
    branch = models.ForeignKey(Branch, on_delete=models.PROTECT, verbose_name='Заведение')

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('g_s', kwargs={'g_s_slug': self.slug})

    class Meta:
        app_label = "main"
        managed = True
        verbose_name = 'Товар/Услуга'
        verbose_name_plural = 'Товары и Услуги'
        ordering = ['name']


class PriceList(models.Model):
    good_or_service = models.OneToOneField(GoodsAndServices, on_delete=models.PROTECT, verbose_name='Товар/Услуга')
    slug = models.SlugField(max_length=255, unique=True, db_index=True, verbose_name="URL")
    price = models.FloatField(verbose_name='Цена')

    def __str__(self):
        return self.good_or_service.name

    def get_absolute_url(self):
        return reverse('price_list', kwargs={'price_list_slug': self.slug})

    class Meta:
        app_label = "main"
        managed = True
        verbose_name = 'Запись в прейскуранте с ценами'
        verbose_name_plural = 'Записи прейскуранта с ценами'
        ordering = ['good_or_service']


class Suppliers(models.Model):
    fio = models.CharField(max_length=100, verbose_name='ФИО')
    slug = models.SlugField(max_length=255, unique=True, db_index=True, verbose_name="URL")
    inn = models.CharField(max_length=20, db_index=True, verbose_name='ИНН')
    phone = models.CharField(max_length=20, verbose_name='Телефон')
    e_mail = models.CharField(max_length=100, verbose_name='E-mail')
    registration_date = models.DateField(auto_now_add=True, verbose_name='Дата регистрации')

    def __str__(self):
        return self.fio

    def get_absolute_url(self):
        return reverse('supplier', kwargs={'supplier_slug': self.slug})

    class Meta:
        app_label = "main"
        managed = True
        verbose_name = 'Поставщик'
        verbose_name_plural = 'Поставщики'
        ordering = ['fio']


class Contracts(models.Model):
    good_or_service = models.OneToOneField(GoodsAndServices, on_delete=models.PROTECT, verbose_name='Товар/Услуга')
    slug = models.SlugField(max_length=255, unique=True, db_index=True, verbose_name="URL")
    supplier = models.ForeignKey(Suppliers, on_delete=models.PROTECT, verbose_name='Поставщик')
    quantity = models.IntegerField(verbose_name='Количество поставляемых товаров/услуг')
    price = models.FloatField(verbose_name='Цена')
    delivery_schedule = models.TextField(blank=True, verbose_name='График поставки')

    def __str__(self):
        return self.good_or_service.name

    def get_absolute_url(self):
        return reverse('contract', kwargs={'contract_slug': self.slug})

    class Meta:
        app_label = "main"
        managed = True
        verbose_name = 'Контракт'
        verbose_name_plural = 'Контракты'
        ordering = ['good_or_service', 'supplier']


class Events(models.Model):
    name = models.CharField(max_length=100, db_index=True, verbose_name='Наименование')
    slug = models.SlugField(max_length=255, unique=True, db_index=True, verbose_name="URL")
    description = models.TextField(blank=True, verbose_name='Описание')
    date_time_of_event = models.DateTimeField(verbose_name='Дата регистрации')
    max_num_of_participants = models.IntegerField(default=99, verbose_name='Максимальное кол-во участников')
    current_num_of_participants = models.IntegerField(default=0, verbose_name='Текущее кол-во участников')
    price = models.FloatField(default=0.0, verbose_name='Цена')
    branch = models.ForeignKey(Branch, on_delete=models.PROTECT, verbose_name='Заведение')

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('event', kwargs={'event_slug': self.slug})

    class Meta:
        app_label = "main"
        managed = True
        verbose_name = 'Мероприятие'
        verbose_name_plural = 'Мероприятия'
        ordering = ['name']


class Reservations(models.Model):
    date_time_of_reservation = models.DateTimeField(verbose_name='Дата и время бронирования')
    slug = models.SlugField(max_length=255, unique=True, db_index=True, verbose_name="URL")
    client_name = models.CharField(max_length=100, verbose_name='Имя клиента')
    object_of_reservation = models.CharField(max_length=100, verbose_name='Объект бронирования')
    event = models.ForeignKey(Events, on_delete=models.PROTECT, verbose_name='Мероприятие', null=True, blank=True)
    table_num = models.IntegerField(null=True, verbose_name='Номер стола', blank=True)
    branch = models.ForeignKey(Branch, on_delete=models.PROTECT, verbose_name='Заведение')
    num_of_persons = models.IntegerField(default=0, verbose_name='Кол-во человек')

    def __str__(self):
        return self.client_name

    def get_absolute_url(self):
        return reverse('reservation', kwargs={'reservation_slug': self.slug})

    class Meta:
        app_label = "main"
        managed = True
        verbose_name = 'Бронирование'
        verbose_name_plural = 'Бронирования'
        ordering = ['date_time_of_reservation', 'client_name']


class Visits(models.Model):
    date_of_visit = models.DateField(verbose_name='Дата посещения')
    slug = models.SlugField(max_length=255, unique=True, db_index=True, verbose_name="URL")
    client = models.ForeignKey(Clients, on_delete=models.PROTECT, verbose_name='Клиент')
    goods_and_services = models.TextField(verbose_name='Купленные товары и услуги')
    is_reserved = models.BooleanField(default=False, verbose_name='Зарезервировано')
    reservation = models.OneToOneField(Reservations, on_delete=models.PROTECT, verbose_name='Бронирование', null=True, blank=True)
    time_start = models.TimeField(verbose_name='Время начала посещения')
    time_end = models.TimeField(verbose_name='Время окончания посещения', null=True, blank=True)
    payment_price = models.FloatField(null=True, verbose_name='Цена к оплате', blank=True)
    branch = models.ForeignKey(Branch, on_delete=models.PROTECT, verbose_name='Заведение')

    def __str__(self):
        return self.date_of_visit

    def get_absolute_url(self):
        return reverse('visit', kwargs={'visit_slug': self.slug})

    class Meta:
        app_label = "main"
        managed = True
        verbose_name = 'Посещение'
        verbose_name_plural = 'Посещения'
        ordering = ['date_of_visit', 'client']


class Staff(models.Model):
    last_name = models.CharField(max_length=100, verbose_name='Фамилия')
    slug = models.SlugField(max_length=255, unique=True, db_index=True, verbose_name="URL")
    first_name = models.CharField(max_length=100, verbose_name='Имя')
    patronymic = models.CharField(max_length=100, verbose_name='Отчество')
    birth_date = models.DateField(blank=True, verbose_name='Дата рождения')
    address = models.CharField(max_length=100, blank=True, verbose_name='Домашний адрес')
    phone = models.CharField(max_length=20, verbose_name='Телефон')
    e_mail = models.CharField(max_length=100, blank=True, verbose_name='E-mail')
    registration_date = models.DateField(auto_now_add=True, verbose_name='Дата принятия на работу')
    num_of_employment_contract = models.IntegerField(null=True, verbose_name='Номер трудового договора')
    duration_of_contract = models.CharField(max_length=100, verbose_name='Срок действия трудового договора')
    salary = models.IntegerField(verbose_name='Оклад')
    branch = models.ForeignKey(Branch, on_delete=models.PROTECT, verbose_name='Заведение')

    def __str__(self):
        return self.last_name

    def get_absolute_url(self):
        return reverse('stuff', kwargs={'stuff_slug': self.slug})

    class Meta:
        app_label = "main"
        managed = True
        verbose_name = 'Сотрудник'
        verbose_name_plural = 'Сотрудники'
        ordering = ['last_name', 'first_name']
