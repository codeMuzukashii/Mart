import json
from traceback import format_exc
from .models import Order, Product
from django.core.mail import EmailMessage
from django.db import connection

def check_is_vip_only(function):
    def wrapper(*args, **kwargs):
        product_id = args[0]
        is_vip = args[2]
        product_obj = Product.objects.get(product_id=product_id)
        if is_vip in (1, '1'):
            is_vip = True
        else:
            is_vip = False

        if is_vip is False and product_obj.vip is True:
            return {'success': False, 'msg': 'this product is for vip only.'}
        else:
            return function(*args, **kwargs)
    return wrapper


def check_stock_pcs(function):
    def wrapper(*args, **kwargs):
        product_id = args[0]
        qty = int(args[1] or 0)
        product_obj = Product.objects.get(product_id=product_id)
        stock_pcs = product_obj.stock_pcs

        if qty == 0:
            return {'success': False, 'msg': 'create a order of 0 qty is illegal.'}
        if qty > stock_pcs:
            return {'success': False, 'msg': 'out of stock.'}
        else:
            return function(*args, **kwargs)
    return wrapper


def check_stock_is_arrived(function):
    def wrapper(*args, **kwargs):
        order_id = args[0]
        order_obj = Order.objects.get(id=order_id)
        product_obj = order_obj.product_id
        qty = order_obj.qty
        stock_pcs_in_db = product_obj.stock_pcs

        is_arrived = True if stock_pcs_in_db == 0 and qty >= 1 else False

        return function(*args, **kwargs, is_arrived=is_arrived)
    return wrapper


@check_stock_pcs
@check_is_vip_only
def create_order(product_id, qty, is_vip):
    order_obj = Order()
    product_obj = Product.objects.get(product_id=product_id)
    price = product_obj.price
    shop_id = product_obj.shop_id
    order_obj.product_id = product_obj
    order_obj.qty = qty
    order_obj.price = price
    order_obj.shop_id = shop_id
    try:
        order_obj.save()
        product_obj.stock_pcs -= int(qty)
        product_obj.save()
    except Exception:
        raise
    return {'success': True, 'msg': ''}


@check_stock_is_arrived
def delete_order(order_id, is_arrived=False):
    order_obj = Order.objects.get(id=order_id)
    product_obj = order_obj.product_id
    try:
        order_obj.delete()
        product_obj.stock_pcs += int(order_obj.qty)
        product_obj.save()
    except Exception:
        raise
    msg = '商品到貨' if is_arrived is True else 'success'
    return {'success': True, 'msg': msg}


def send_shop_info_today():
    try:
        cursor = connection.cursor()
        sql = "select `shop_id`, (`price` * `qty`) as `total_price`, sum(`qty`) as `total_qty`, count(*) as `total_orders` from `tb_order` GROUP by `shop_id`;"
        cursor.execute(sql)
        datas = cursor.fetchall()
        result = []
        for data in datas:
            result.append(dict({
                "shop_id": data[0],
                "total_price": data[1],
                "total_qty": data[2],
                "total_orders": data[3]
            }))
        email = EmailMessage('Shop info of today', json.dumps(result), to=['blitz9211@msn.com'])
        email.send()

    except Exception:
        print('send_shop_info_today exception:')
        print(format_exc())


def show_top3():
    result = []
    try:
        cursor = connection.cursor()
        sql = "select `product_id_id`, sum(`qty`) as `total_qty` from `tb_order` GROUP by `product_id_id` order by `total_qty` desc limit 3;"

        cursor.execute(sql)
        datas = cursor.fetchall()
        for data in datas:
            result.append(dict({
                "product_id": data[0],
                "total_qty": data[1],
            }))
    except Exception:
        raise
    return result