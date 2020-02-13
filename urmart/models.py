from django.db import models


class Product(models.Model):
    product_id = models.BigAutoField(primary_key=True)
    stock_pcs = models.IntegerField(default=0)
    price = models.IntegerField(default=0)
    shop_id = models.CharField(null=True, max_length=5)
    vip = models.BooleanField(default=False)

    class Meta:
        db_table = 'tb_product'

    def __str__(self):
        """String for representing the Model object."""
        return str(self.product_id)


class Order(models.Model):
    id = models.BigAutoField(primary_key=True)
    product_id = models.ForeignKey(Product, related_name='orders', on_delete=models.SET_NULL, null=True)
    qty = models.IntegerField(default=0)
    price = models.IntegerField(default=0)
    shop_id = models.CharField(null=True, max_length=5)

    class Meta:
        db_table = 'tb_order'

    def __str__(self):
        """String for representing the Model object."""
        return str(self.id)


class Customer(models.Model):
    customer_id = models.CharField(null=True, max_length=5)
    is_vip = models.BooleanField(default=False)

    class Meta:
        db_table = 'tb_customer'

    def __str__(self):
        """String for representing the Model object."""
        return str(self.customer_id)
