# Generated by Django 3.1.2 on 2021-08-10 15:00

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='AdvSlider',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('adv_image', models.ImageField(default='static/media/adv_slider/default.webp', upload_to='static/media/adv_slider')),
            ],
        ),
        migrations.CreateModel(
            name='Brend',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('brend', models.CharField(max_length=20)),
            ],
            options={
                'ordering': ['brend'],
            },
        ),
        migrations.CreateModel(
            name='Color',
            fields=[
                ('name_color', models.CharField(max_length=15, primary_key=True, serialize=False)),
            ],
        ),
        migrations.CreateModel(
            name='Footwear',
            fields=[
                ('id', models.CharField(max_length=10, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=100)),
                ('popular', models.IntegerField(default='0')),
                ('price', models.IntegerField(default='0')),
                ('color', models.ManyToManyField(to='KidsStepShop.Color')),
                ('footwear_brend', models.ForeignKey(default='0', null=True, on_delete=django.db.models.deletion.SET_NULL, to='KidsStepShop.brend')),
            ],
            options={
                'ordering': ['footwear_type'],
            },
        ),
        migrations.CreateModel(
            name='Gender',
            fields=[
                ('id_gender', models.CharField(max_length=20, primary_key=True, serialize=False)),
                ('gender', models.CharField(default='0', max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='Image',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(default='static/media/footwear/default.webp', upload_to='static/media/footwear')),
            ],
        ),
        migrations.CreateModel(
            name='Size',
            fields=[
                ('size', models.CharField(max_length=10, primary_key=True, serialize=False)),
            ],
        ),
        migrations.CreateModel(
            name='StatusOrder',
            fields=[
                ('status', models.CharField(max_length=30, primary_key=True, serialize=False)),
            ],
        ),
        migrations.CreateModel(
            name='StatusProduct',
            fields=[
                ('status', models.CharField(max_length=30, primary_key=True, serialize=False)),
            ],
        ),
        migrations.CreateModel(
            name='Type',
            fields=[
                ('id_type', models.CharField(max_length=20, primary_key=True, serialize=False)),
                ('type', models.CharField(default='0', max_length=20)),
            ],
            options={
                'ordering': ['type'],
            },
        ),
        migrations.CreateModel(
            name='TypePrw',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('prw_image', models.ImageField(default='static/media/images/default.webp', upload_to='static/media/images')),
                ('prw_gender', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='KidsStepShop.gender')),
                ('prw_type', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='KidsStepShop.type')),
            ],
        ),
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('phone', models.CharField(max_length=10, null=True)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id_product', models.AutoField(auto_created=True, primary_key=True, serialize=False)),
                ('user_name', models.CharField(max_length=100, null=True)),
                ('prod_status', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='KidsStepShop.statusproduct')),
                ('product', models.ForeignKey(max_length=100, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='KidsStepShop.footwear')),
                ('size', models.ForeignKey(max_length=100, null=True, on_delete=django.db.models.deletion.CASCADE, to='KidsStepShop.size')),
            ],
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id_order', models.AutoField(auto_created=True, primary_key=True, serialize=False)),
                ('article', models.IntegerField(default='0000')),
                ('user_order', models.CharField(default='аноним', max_length=100, null=True)),
                ('delivery', models.CharField(max_length=100, null=True)),
                ('total_price', models.IntegerField(null=True)),
                ('product', models.ManyToManyField(to='KidsStepShop.Product')),
                ('status', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='KidsStepShop.statusorder')),
            ],
        ),
        migrations.AddField(
            model_name='gender',
            name='g_type',
            field=models.ManyToManyField(to='KidsStepShop.Type'),
        ),
        migrations.AddField(
            model_name='footwear',
            name='footwear_gender',
            field=models.ManyToManyField(to='KidsStepShop.Gender'),
        ),
        migrations.AddField(
            model_name='footwear',
            name='footwear_type',
            field=models.ForeignKey(default='0', null=True, on_delete=django.db.models.deletion.SET_NULL, to='KidsStepShop.type'),
        ),
        migrations.AddField(
            model_name='footwear',
            name='image',
            field=models.ManyToManyField(to='KidsStepShop.Image'),
        ),
        migrations.AddField(
            model_name='footwear',
            name='size',
            field=models.ManyToManyField(to='KidsStepShop.Size'),
        ),
    ]
