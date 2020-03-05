from traceback import format_exc
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django_tables2 import RequestConfig
from django.http import JsonResponse
from . import order
from .table import ProductTable, OrderTable
from .models import Product, Order


def product(request):
    tb_product = ProductTable(Product.objects.all())
    RequestConfig(request).configure(tb_product)

    pro_obj = Product.objects.values()
    pro_id_list = [p['product_id'] for p in pro_obj]

    tb_order = OrderTable(Order.objects.all())
    RequestConfig(request).configure(tb_order)
    tables = dict(
        tb_product=tb_product,
        tb_order=tb_order,
        pro_id_list=pro_id_list,
    )
    return render(request, 'urmart.html', tables)


@csrf_exempt
def save_order(request):
    msg = ''
    status = 500
    if request.is_ajax() and request.method == 'POST':
        try:
            product_id = request.POST.get('product_id')
            qty = request.POST.get('qty')
            is_vip = request.POST.get('is_vip')

            result = order.create_order(product_id, qty, is_vip)

            if result['success'] is True:
                status = 200
                msg = 'success'
            else:
                status = 400
                msg = result['msg']
        except:
            print(format_exc())

    else:
        status = 400
        msg = 'The request is not valid.'

    response = dict(
        message=msg,
    )
    return JsonResponse(response, status=status, safe=False)


@csrf_exempt
def delete_order(request):
    msg = ''
    status = 500
    if request.is_ajax() and request.method == 'POST':
        try:
            order_id = request.POST.get('order_id')

            result = order.delete_order(order_id)

            if result['success'] is True:
                status = 200
                msg = result['msg']
            else:
                status = 400
                msg = result['msg']
        except:
            status = 500
            msg = 'exception occurred.'
            print(format_exc())

    else:
        status = 400
        msg = 'The request is not valid.'

    response = dict(
        message=msg,
    )
    return JsonResponse(response, status=status, safe=False)


def send_shop_info_today():
    order.send_shop_info_today()
    return


@csrf_exempt
def show_top3(request):
    msg = ''
    status = 500
    result = []
    if request.is_ajax() and request.method == 'POST':
        try:
            result = order.show_top3()
            status = 200
            msg = ''
        except:
            status = 500
            msg = 'exception occurred.'
            print(format_exc())
    else:
        status = 400
        msg = 'The request is not valid.'

    response = dict(
        message=msg,
        data=result
    )
    return JsonResponse(response, status=status, safe=False)
