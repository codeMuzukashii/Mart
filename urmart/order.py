from django.views.decorators.http import require_http_methods
from .models import Order, Product


# def compose(*funs):
#     def deco(f):
#         for fun in reversed(funs):
#             f = fun(f)
#         return f
#     return deco


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
        print(args)
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
    except:
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
    except:
        raise
    msg = '商品到貨' if is_arrived is True else 'success'
    return {'success': True, 'msg': msg}