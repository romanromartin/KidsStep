from django.contrib import admin
from django.contrib.admin.filters import SimpleListFilter
from .models import Gender, Type, Brend, Footwear, Color, Profile, Size, StatusOrder, Product, AdvSlider, Order, \
    StatusProduct, TypePrw, Image
from parler.admin import TranslatableAdmin


@admin.register(Gender)
class GenderAdmin(TranslatableAdmin):
    list_display = ['id_gender', 'gender']


@admin.register(Type)
class TypeAdmin(TranslatableAdmin):
    list_display = ['id_type', 'type']


@admin.register(TypePrw)
class TypePreviewAdmin(admin.ModelAdmin):
    list_display = ('str_gender', 'str_type', 'image_tag' )
    readonly_fields = ['image_tag']


@admin.register(Brend)
class BrendAdmin(admin.ModelAdmin):
    pass


@admin.register(Footwear)
class FootwearAdmin(TranslatableAdmin):
    list_display = ('name', 'get_gender', 'footwear_type', 'footwear_brend', 'id',  'get_colors', 'get_size', 'price', 'popular')
    list_filter = ('footwear_type', 'footwear_brend','footwear_gender')
#     fields = ['id', 'name', ('footwear_gender', 'footwear_type'), 'footwear_brend','price', 'color', 'size', 'popular']
#     # readonly_fields = ['image_tag', 'image_tag_side', 'image_tag_top', 'image_tag_scale']

# @admin.register(Image)
# class ImageAdmin(admin.ModelAdmin):
#     list_display = ('id_image',  'image_tag')
#     readonly_fields = ['image_tag']
#
#
#
@admin.register(Color)
class ColorAdmin(TranslatableAdmin):
    list_display = ['id_color', 'name_color']


# @admin.register(Profile)
# class ProfileAdmin(admin.ModelAdmin):
#     list_display = ('user', 'phone')
#

@admin.register(Size)
class SizeAdmin(admin.ModelAdmin):
    pass

#
# @admin.register(StatusOrder)
# class StatusOrderAdmin(admin.ModelAdmin):
#     pass
#
#
# @admin.register(StatusProduct)
# class StatusProductAdmin(admin.ModelAdmin):
#     pass
#
#




# @admin.register(Product)
# class ProductAdmin(admin.ModelAdmin):
#     list_display = ('id_product', 'user_name', 'prod_name', 'prod_gender', 'prod_type', 'size', 'prod_status')
#     list_filter = ('user_name', 'size')
#
# @admin.register(Order)
# class OrderAdmin(admin.ModelAdmin):
#     pass


@admin.register(AdvSlider)
class AdvSliderAdmin(admin.ModelAdmin):
    list_display = ('image_tag', 'adv_image')
    fields = ['image_tag', 'adv_image']
    readonly_fields = ['image_tag']