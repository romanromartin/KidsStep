# Generated by Django 3.2.9 on 2021-12-02 15:36

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import parler.fields
import parler.models


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
                ('id_color', models.CharField(auto_created=True, max_length=15, primary_key=True, serialize=False)),
            ],
            options={
                'abstract': False,
            },
            bases=(parler.models.TranslatableModelMixin, models.Model),
        ),
        migrations.CreateModel(
            name='Footwear',
            fields=[
                ('id', models.CharField(max_length=10, primary_key=True, serialize=False)),
                ('popular', models.IntegerField(default='0')),
                ('price', models.IntegerField(default='0')),
                ('in_use', models.BooleanField(default=True)),
                ('color', models.ManyToManyField(to='KidsStepShop.Color')),
                ('footwear_brend', models.ForeignKey(default='undefined', null=True, on_delete=django.db.models.deletion.CASCADE, to='KidsStepShop.brend')),
            ],
            options={
                'ordering': ['footwear_type'],
            },
            bases=(parler.models.TranslatableModelMixin, models.Model),
        ),
        migrations.CreateModel(
            name='Gender',
            fields=[
                ('id_gender', models.CharField(max_length=20, primary_key=True, serialize=False)),
            ],
            options={
                'abstract': False,
            },
            bases=(parler.models.TranslatableModelMixin, models.Model),
        ),
        migrations.CreateModel(
            name='Image',
            fields=[
                ('id_image', models.CharField(auto_created=True, max_length=15, primary_key=True, serialize=False)),
                ('image', models.ImageField(default='static/media/footwear/default.webp', upload_to='static/media/footwear')),
            ],
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id_order', models.AutoField(auto_created=True, primary_key=True, serialize=False)),
                ('article', models.IntegerField(default='0000')),
                ('user_order', models.CharField(default='аноним', max_length=100, null=True)),
                ('delivery', models.CharField(max_length=100, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Size',
            fields=[
                ('id_size', models.CharField(auto_created=True, max_length=10, primary_key=True, serialize=False)),
                ('size', models.CharField(max_length=10)),
            ],
        ),
        migrations.CreateModel(
            name='StatusOrder',
            fields=[
                ('id_status_order', models.CharField(max_length=20, primary_key=True, serialize=False)),
            ],
            options={
                'abstract': False,
            },
            bases=(parler.models.TranslatableModelMixin, models.Model),
        ),
        migrations.CreateModel(
            name='Type',
            fields=[
                ('id_type', models.CharField(max_length=20, primary_key=True, serialize=False)),
            ],
            options={
                'abstract': False,
            },
            bases=(parler.models.TranslatableModelMixin, models.Model),
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
                ('quantity', models.IntegerField(default=1)),
                ('order', models.ForeignKey(max_length=100, null=True, on_delete=django.db.models.deletion.CASCADE, to='KidsStepShop.order')),
                ('product', models.ForeignKey(max_length=100, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='KidsStepShop.footwear')),
                ('size', models.ForeignKey(max_length=100, null=True, on_delete=django.db.models.deletion.CASCADE, to='KidsStepShop.size')),
            ],
        ),
        migrations.AddField(
            model_name='order',
            name='status',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='KidsStepShop.statusorder'),
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
            field=models.ForeignKey(default='undefined', null=True, on_delete=django.db.models.deletion.CASCADE, to='KidsStepShop.type'),
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
        migrations.CreateModel(
            name='TypeTranslation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('language_code', models.CharField(db_index=True, max_length=15, verbose_name='Language')),
                ('type', models.CharField(default='0', max_length=20)),
                ('master', parler.fields.TranslationsForeignKey(editable=False, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='translations', to='KidsStepShop.type')),
            ],
            options={
                'verbose_name': 'type Translation',
                'db_table': 'KidsStepShop_type_translation',
                'db_tablespace': '',
                'managed': True,
                'default_permissions': (),
                'unique_together': {('language_code', 'master')},
            },
            bases=(parler.models.TranslatedFieldsModelMixin, models.Model),
        ),
        migrations.CreateModel(
            name='StatusOrderTranslation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('language_code', models.CharField(db_index=True, max_length=15, verbose_name='Language')),
                ('status', models.CharField(default='0', max_length=40)),
                ('master', parler.fields.TranslationsForeignKey(editable=False, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='translations', to='KidsStepShop.statusorder')),
            ],
            options={
                'verbose_name': 'status order Translation',
                'db_table': 'KidsStepShop_statusorder_translation',
                'db_tablespace': '',
                'managed': True,
                'default_permissions': (),
                'unique_together': {('language_code', 'master')},
            },
            bases=(parler.models.TranslatedFieldsModelMixin, models.Model),
        ),
        migrations.CreateModel(
            name='GenderTranslation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('language_code', models.CharField(db_index=True, max_length=15, verbose_name='Language')),
                ('gender', models.CharField(default='0', max_length=20)),
                ('master', parler.fields.TranslationsForeignKey(editable=False, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='translations', to='KidsStepShop.gender')),
            ],
            options={
                'verbose_name': 'gender Translation',
                'db_table': 'KidsStepShop_gender_translation',
                'db_tablespace': '',
                'managed': True,
                'default_permissions': (),
                'unique_together': {('language_code', 'master')},
            },
            bases=(parler.models.TranslatedFieldsModelMixin, models.Model),
        ),
        migrations.CreateModel(
            name='FootwearTranslation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('language_code', models.CharField(db_index=True, max_length=15, verbose_name='Language')),
                ('name', models.CharField(max_length=100)),
                ('master', parler.fields.TranslationsForeignKey(editable=False, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='translations', to='KidsStepShop.footwear')),
            ],
            options={
                'verbose_name': 'footwear Translation',
                'db_table': 'KidsStepShop_footwear_translation',
                'db_tablespace': '',
                'managed': True,
                'default_permissions': (),
                'unique_together': {('language_code', 'master')},
            },
            bases=(parler.models.TranslatedFieldsModelMixin, models.Model),
        ),
        migrations.CreateModel(
            name='ColorTranslation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('language_code', models.CharField(db_index=True, max_length=15, verbose_name='Language')),
                ('name_color', models.CharField(max_length=15)),
                ('master', parler.fields.TranslationsForeignKey(editable=False, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='translations', to='KidsStepShop.color')),
            ],
            options={
                'verbose_name': 'color Translation',
                'db_table': 'KidsStepShop_color_translation',
                'db_tablespace': '',
                'managed': True,
                'default_permissions': (),
                'unique_together': {('language_code', 'master')},
            },
            bases=(parler.models.TranslatedFieldsModelMixin, models.Model),
        ),
    ]
