from django.contrib.auth.models import User
from django.db import models
from django.core.files.storage import FileSystemStorage
from django.urls import reverse
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.translation import ugettext_lazy as _
from smart_selects.db_fields import ChainedForeignKey
from parler.models import TranslatableModel, TranslatedFields



class Color(TranslatableModel):
    id_color = models.CharField(primary_key=True,  max_length=15, auto_created=True)
    translations = TranslatedFields(
        name_color=models.CharField(max_length=15))

    # def __str__(self):
    #     return self.name_color


class Size(models.Model):
    id_size = models.CharField(primary_key=True, max_length=10, auto_created=True)
    size = models.CharField(max_length=10)

    def __str__(self):
        return self.size



class Gender(TranslatableModel):
    id_gender = models.CharField(primary_key=True, max_length=20, null=False,)
    g_type = models.ManyToManyField('Type')
    translations = TranslatedFields(
        gender=models.CharField(max_length=20, null=False, default='0'))

    # def __str__(self):
    #     return self.gender


class Type(TranslatableModel):
    id_type = models.CharField(primary_key=True, max_length=20, null=False, )
    translations = TranslatedFields(
        type=models.CharField(max_length=20, null=False, default='0'))

    # class Meta:
    #     ordering = ["type"]
    #
    # # def __str__(self):
    # #     return self.type


class TypePrw(models.Model):
    prw_image = models.ImageField(upload_to='static/media/images', default='static/media/images/default.webp')
    prw_gender = models.ForeignKey(Gender, null=True, on_delete=models.CASCADE)
    prw_type = models.ForeignKey(Type, null=True, on_delete=models.CASCADE)

    def str_type(self):
        return self.prw_type.type
    str_type.short_description = 'Тип'

    def str_gender(self):
        return self.prw_gender.gender
    str_gender.short_description = 'Пол'

    def image_tag(self):
        return mark_safe('<img src="/%s" width = 100px; />' % self.prw_image)
    image_tag.short_description = 'Image'


class Brend(models.Model):
    brend = models.CharField(max_length=20, null=False)

    class Meta:
        ordering = ["brend"]

    def __str__(self):
        return self.brend


class Footwear(TranslatableModel):
    id = models.CharField(primary_key=True, max_length=10)
    footwear_brend = models.ForeignKey('Brend', on_delete=models.CASCADE, null=True, default='undefined')
    footwear_gender = models.ManyToManyField('Gender')
    footwear_type = models.ForeignKey(Type, on_delete=models.CASCADE, null=True, default='undefined')
    popular = models.IntegerField(null=False, default='0')
    image = models.ManyToManyField('Image')
    price = models.IntegerField(default='0')
    color = models.ManyToManyField('Color')
    size = models.ManyToManyField(Size)
    translations = TranslatedFields(
        name=models.CharField(max_length=100, null=False))
    in_use = models.BooleanField(default=True)


    class Meta:
        ordering = ["footwear_type"]

    def get_colors(self):
        return ', '.join(col.name_color for col in self.color.all())
    get_colors.short_description = 'Colors'

    def get_size(self):
        return ','.join(s.size for s in self.size.all())
    get_size.short_description = 'Size'

    def get_gender(self):
        return ','.join(s.gender for s in self.footwear_gender.all())
    get_size.short_description = 'Gender'


class Image(models.Model):
    id_image = models.CharField(primary_key=True, max_length=15, auto_created=True)
    image = models.ImageField(upload_to='static/media/footwear', default='static/media/footwear/default.webp')

    def image_tag(self):
        return mark_safe('<img src="/%s" width = 100px; />' % self.image)
    image_tag.short_description = 'Image'


class Product(models.Model):
    id_product = models.AutoField(primary_key=True, auto_created=True)
    product = models.ForeignKey('Footwear', max_length=100, null=True, on_delete=models.DO_NOTHING)
    order = models.ForeignKey('Order', max_length=100, null=True,on_delete=models.CASCADE)
    size = models.ForeignKey('Size', max_length=100, null=True, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1, null=False)


    # def prod_name(self):
    #     return self.product.name
    # prod_name.short_description = 'Name product'

    # def prod_gender(self):
    #     return self.product.footwear_gender
    # prod_gender.short_description = 'Gender'

    # def prod_type(self):
    #     return self.product.footwear_type

    # prod_type.short_description = 'Type'


class Order(models.Model):
    id_order = models.AutoField(primary_key=True, auto_created=True)
    article = models.IntegerField(default='0000')
    user_order = models.CharField(max_length=100, null=True, default='аноним')
    delivery = models.CharField(max_length=100, null=True)
    status = models.ForeignKey('StatusOrder', null=True, on_delete=models.CASCADE)



class StatusOrder(TranslatableModel):
    id_status_order = models.CharField(primary_key=True, max_length=20, null=False, )
    translations = TranslatedFields(
        status=models.CharField(max_length=40, default='0'))

    # def __str__(self):
    #     return self.status



class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = models.CharField(max_length=10, null=True)


@receiver(post_save, sender=User)
def update_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
    instance.profile.save()


from django.utils.html import mark_safe


class AdvSlider(models.Model):
    adv_image = models.ImageField(upload_to='static/media/adv_slider', default='static/media/adv_slider/default.webp')

    def image_tag(self):
        return mark_safe('<img src="/%s"  />' % self.adv_image)

    image_tag.short_description = 'Image'


    def __str__(self):
        return str(self.adv_image) if self.adv_image else ''


