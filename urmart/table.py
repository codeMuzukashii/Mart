# coding: utf8
import django_tables2
from .models import Product, Order


class ProductTable(django_tables2.Table):
    class Meta:
        model = Product
        # add class="paleblue" to <table> tag
        attrs = {'class': 'paleblue'}


class OrderTable(django_tables2.Table):
    edit = django_tables2.TemplateColumn(
        '<button data-toggle="tooltip" title="" class="btn btn-danger btn-xs delete_btn button1" value="{{ record.id }}">-</button>',
        orderable=False,
        verbose_name=''
    )
    class Meta:
        model = Order
        # add class="paleblue" to <table> tag
        attrs = {'class': 'paleblue'}
        fields = ['id', 'product_id', 'qty', 'price', 'shop_id', 'edit']
