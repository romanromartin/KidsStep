from django import template
from KidsStepShop.models import Product
register = template.Library()



@register.filter
def index(indexable, i):
    return indexable[i]

@register.filter
def product_price(indexable):
    return indexable[3].price

@register.filter
def product_price_sum(indexable):
    return int(indexable[3].price) * int(indexable[5])

@register.filter
def product_name(indexable):
    return indexable[3].name

@register.filter
def product_image(indexable):
    return indexable[3].image.first().image

@register.filter
def product_id(indexable):
    return indexable[3].id

@register.filter
def product_type(indexable):
    return indexable[3].footwear_type

@register.filter
def sum_pr(pr):
    return pr.quantity * pr.product.price

@register.filter
def total_sum(od):
    total = 0
    for pr in od.product_set.all():
        print(pr.quantity * pr.product.price)
        total += pr.quantity * pr.product.price
    return total

