from django.shortcuts import render, redirect
import xml.etree.ElementTree as ET
from .models import Gender, Type, Footwear, Product, Color, Size, \
    AdvSlider, Order, StatusOrder, StatusProduct, Profile, Brend, TypePrw, Image
from django.contrib.auth import authenticate, login, logout, models
from KidsStepShop.forms import SignUpForm, LogInForm, ResetPasswordForm
from django.conf import settings
import random
import os
import psycopg2
from PIL import Image as ImagePIL
from urllib.request import urlopen

conn = psycopg2.connect(dbname='d5peu9b3fqs423', host='ec2-44-196-146-152.compute-1.amazonaws.com', port='5432',
                        user="lhwlclorbernre",
                        password="5e9ba3c98c99ee19ed23d0e825a240d3e85be4fba2d44bf74abbc010a9f543a9")
cur = conn.cursor()

gender = Gender.objects.all()
types = Type.objects.all()

supplier = {'berni.com.ua': 'b-'}
gender_dict = {'girl': 'Для девочек', 'boy': 'Для мальчиков'}
type_dict = {'boots': 'Ботинки', 'shoes': 'Туфли', 'sneakers': 'Кроссовки', 'high_boots': 'Сапоги',
             'sandals': 'Сандалии', 'moccasins': 'Мокасины', 'low_shoes': 'Полуботинки', 'ankle_boots': 'Ботильоны',
             'rubber_boots': 'Резиновые сапоги', 'clogs': 'Сабо', 'slates': 'Сланцы', 'slipons': 'Слипоны',
             'slippers': 'Тапочки', 'flip_flops': 'Шлепки', 'other': 'Другое'}
color_dict = {'Черный': 'black', 'Фиолетовый': 'violet', 'Хаки': 'khaki', 'Синий': 'blue', 'Серый': 'grey',
              'Серебряный': 'silver', 'Розовый': 'pink', 'Персиковый': 'peach', 'Оранжевый': 'orange',
              'Мультиколор': 'multicolor', 'Молочный': 'milk', 'Малиновый': 'crimson', 'Красный': 'red',
              'Коричневый': 'brown', 'Зеленый': 'green', 'Желтый': 'yellow', 'Голубой': 'light_blue',
              'Бирюзовый': 'turquoise', 'Белый': 'white', 'Бежевый': 'beige', 'Золотой': 'gold'}




def index(request):
    fw_pop = Footwear.objects.all().order_by('-popular')[:30]
    adv = AdvSlider.objects.all()
    return render(request, 'index.html', context={'gender': gender, 'popular': fw_pop, 'adv': adv})


def type(request, id_gender):
    prw_list = TypePrw.objects.filter(prw_gender=id_gender)
    return render(request, 'type.html',
                  context={'gender': gender,   'nav_gender': navigation_gender(id_gender), 'prw_list': prw_list})


def footwear(request, id_gender, id_type):
    footwear = Footwear.objects.filter(footwear_gender__id_gender=id_gender, footwear_type__id_type=id_type)
    return render(request, 'footwear.html',
                  context={'gender': gender, 'types': types, 'footwear_selected': footwear,
                           'nav_gender': navigation_gender(id_gender), 'nav_type': navigation_type(id_type)})


def footwear_detail(request, id_gender, id_type, id):
    err = ''
    fw_sel = Footwear.objects.get(id=id)
    if request.method == 'POST':
        if request.user.is_authenticated:
            if request.POST.get("size") is None:
                err = 'Не выбран размер '
            else:
                prod = Product()
                prod.user_name = request.user.username
                prod.product = fw_sel
                prod.size = Size.objects.get(size=request.POST.get("size"))
                prod.prod_status = StatusProduct.objects.get(status='Корзина')
                prod.save()
                return redirect('basket')
        else:
            return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))
    return render(request, 'footwear_detail.html',
                  context={'gender': gender, 'types': types, 'nav_type': navigation_type(id_type),
                           'nav_gender': navigation_gender(id_gender),
                           'form_error': err, 'fw_sel': fw_sel})


def navigation_gender(id_gender):
    nav_gender = gender.get(id_gender=id_gender)
    return nav_gender


def navigation_type(id_type):
    nav_type = types.get(id_type=id_type)
    return nav_type


def navGender(id_gender):
    nav_gender = Gender.objects.filter(id_gender=id_gender)
    return nav_gender


def basket(request):
    total_price = 0
    user_product = Product.objects.filter(user_name=request.user.username, prod_status='Корзина')
    for user_ in user_product:
        total_price += user_.product.price
    if request.method == 'POST':
        if request.POST.get("delete"):
            prod = Product.objects.filter(id_product=request.POST.get("delete"))
            prod.delete()
            return redirect('basket')
    return render(request, 'basket.html', context={'user_product': user_product, 'total': total_price})


def order(request):
    err = ''
    total_price = 0
    user_product = Product.objects.filter(user_name=request.user.username, prod_status='Корзина')

    for user_ in user_product:
        total_price += user_.product.price
    if request.method == 'POST':
        if request.POST.get("name_delivery"):
            return render(request, 'order.html',
                          context={'user_product': user_product, 'total': total_price,
                                   'name_delivery': request.POST.get("name_delivery"), 'form_error': err})
        if request.POST.get("done"):
            if request.POST.get("city-delivery") == '':
                err += 'Не указан город '
                if request.POST.get("done") == 'nova-poshta':
                    if request.POST.get("department-delivery") == '':
                        err += 'и отделение '
                elif request.POST.get("done") == 'ukrposhta':
                    if request.POST.get("index-delivery") == '':
                        err += 'и индекс '
            elif request.POST.get("done") == 'nova-poshta' and request.POST.get("department-delivery") == '':
                err += 'Не указано отделение '
            elif request.POST.get("done") == 'ukrposhta' and request.POST.get("index-delivery") == '':
                err += 'Не указан индекс '
            else:
                new_article = 0
                article_in_use_list = []
                while new_article == 0:
                    number = random.randrange(1000, 9999)
                    for article_in_use in Order.objects.all():
                        article_in_use_list.append(article_in_use.article)
                    if number not in article_in_use_list:
                        new_article = number
                ord = Order()
                ord.article = new_article
                ord.user_order = request.user.username
                if request.POST.get("done") == 'nova-poshta':
                    ord.delivery = 'Новая почта ' + request.POST.get("city-delivery") + 'Отд.№ ' + request.POST.get(
                        "department-delivery")
                elif request.POST.get("done") == 'ukrposhta':
                    ord.delivery = 'Укрпочта ' + request.POST.get("city-delivery") + 'Отд.№ ' + request.POST.get(
                        "index-delivery")
                ord.status = StatusOrder.objects.get(status='В работе')
                ord.total_price = total_price
                ord.save()
                for pr in user_product:
                    ord.product.add(pr.id_product)
                    pr.prod_status = StatusProduct.objects.get(status='Заказ')
                    pr.save()
                ord.save()
                return redirect('order_done', new_article)
            return render(request, 'order.html', context={'user_product': user_product, 'total': total_price,
                                                          'name_delivery': request.POST.get("done"), 'form_error': err})

    return render(request, 'order.html',
                  context={'user_product': user_product, 'total': total_price, 'form_error': err})


def order_done(request, article):
    ord = Order.objects.get(article=article)
    return render(request, 'order_done.html', context={'article': article, 'order': ord})


def profile(request):
    return render(request, 'registration/profile.html')


def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.refresh_from_db()  # load the profile instance created by the signal
            user.profile.phone = form.cleaned_data.get('phone')
            user.save()
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=user.username, password=raw_password)
            login(request, user)
            return redirect('index')

    else:
        form = SignUpForm()
    return render(request, 'registration/signup.html', {'form': form})


def loginUser(request):
    if request.method == 'POST':
        form = LogInForm(data=request.POST)
        if request.method == 'POST':
            if form.is_valid():
                user = authenticate(username=form.cleaned_data.get('username'),
                                    password=form.cleaned_data.get('password'))
                login(request, user)
                return redirect(request.GET['next'])
    else:

        form = LogInForm()
    return render(request, 'registration/login.html', {'form': form, })


def logoutUser(request):
    logout(request)
    return redirect(request.GET['next'])


def managment(request):
    orders = Order.objects.all()
    stat = StatusOrder.objects.all()
    for ord in orders:
        if ord.product.count() < 1:
            ord.delete()
    orders = Order.objects.all()
    users_ = models.User.objects.all()
    prof = Profile.objects.all()
    if request.method == 'POST':
        if request.POST.get("delete"):
            prod = Product.objects.get(id_product=request.POST.get("delete"))
            order_price_change = Order.objects.get(id_order=request.POST.get("order_id"))
            order_price_change.total_price -= prod.product.price
            order_price_change.save()
            prod.delete()
            return redirect('managment')
        if request.POST.get("delete_order"):
            order_to_delete = Order.objects.filter(id_order=request.POST.get("delete_order"))
            order_to_delete.delete()
            return redirect('managment')
        if request.POST.get("change_status"):
            order_status_change = Order.objects.get(id_order=request.POST.get("order_id"))
            new_status = StatusOrder.objects.get(status=request.POST.get("change_status"))
            order_status_change.status = new_status
            order_status_change.save()
            return redirect('managment')
    if request.user.is_staff:
        return render(request, 'managment.html',
                      context={'orders': orders, 'users': users_, 'prof': prof, 'stat': stat})
    else:
        return render(request, 'access_denied.html')


def search(request):
    s_f = []
    # search_footwear = Footwear.objects.filter(Q(name__icontains=request.POST.get("search") ))
    for foot in Footwear.objects.all():
        if request.POST.get("search").lower() in foot.name.lower():
            s_f.append(foot)
        elif request.POST.get("search").lower() in str(foot.footwear_brend).lower():
            s_f.append(foot)
    print(s_f)
    return render(request, 'search.html', context={'search': s_f, 'gender': gender, 'types': types, })


def db_handler(request):
    if request.method == 'POST':
        if request.POST.get("refresh_ge_ty"):
            query_clear = 'TRUNCATE TABLE "KidsStepShop_gender" CASCADE; ' \
                          'TRUNCATE TABLE "KidsStepShop_type" CASCADE; ' \
                          'TRUNCATE TABLE "KidsStepShop_typeprw" CASCADE; '
            cur.execute(query_clear)
            conn.commit()
            Gender.objects.all().delete()
            Type.objects.all().delete()
            TypePrw.objects.all().delete()
            for t in type_dict:
                query_add_type = 'INSERT INTO "KidsStepShop_type" ( "id_type", "type") ' \
                                 + "VALUES ('" + t + "', '" + type_dict[t] + "');"
                cur.execute(query_add_type)
                conn.commit()
                type = Type()
                type.id_type = t
                type.type = type_dict[t]
                type.save()
            for g in gender_dict:
                query_add_gender = 'INSERT INTO "KidsStepShop_gender" ( "id_gender", "gender") ' \
                                 + "VALUES ('" + g + "', '" + gender_dict[g] + "');"
                cur.execute(query_add_gender)
                conn.commit()
                gender = Gender()
                gender.id_gender = g
                gender.gender = gender_dict[g]
                gender.save()
                for t in Type.objects.all():
                    img = ''
                    prw = TypePrw()
                    prw.prw_gender = Gender.objects.get(id_gender=g)
                    prw.prw_type = Type.objects.get(id_type=t.id_type)
                    dir_prw = os.listdir('static/media/images/')
                    for pr in dir_prw:
                        if len(pr.split('.')[0].split('-')) < 2:
                            continue
                        if pr.split('.')[0].split('-')[1] == g and pr.split('.')[0].split('-')[0] == t.id_type:
                            img = 'static/media/images/' + pr
                            break
                        else:
                            img = 'static/media/images/default.webp'
                    prw.prw_image = img
                    prw.save()
                    query_add_typeprw = 'INSERT INTO "KidsStepShop_typeprw" ( "prw_image", "prw_gender_id", "prw_type_id") ' \
                                       + "VALUES ('" + img + "', '" + g + "', '" + t.id_type  + "');"
                    cur.execute(query_add_typeprw)
                    conn.commit()


        elif request.POST.get("refresh_size"):
            query_clear = 'TRUNCATE TABLE "KidsStepShop_size" CASCADE; '
            cur.execute(query_clear)
            conn.commit()
            Size.objects.all().delete()
            for s in range(1, 46):
                query_add_size = 'INSERT INTO "KidsStepShop_size" ("id_size", "size") ' \
                                 + "VALUES ('" + str(s) + "', '" + str(s) + "');"
                cur.execute(query_add_size)
                conn.commit()
                size = Size()
                size.id_size = s
                size.size = s
                size.save()
        elif request.POST.get("refresh_adv_slider"):
            query_clear = 'TRUNCATE TABLE "KidsStepShop_advslider";'
            cur.execute(query_clear)
            conn.commit()
            AdvSlider.objects.all().delete()
            dir_adv = os.listdir('static/media/adv_slider/')
            for adv in dir_adv:
                if adv == 'default.webp':
                    continue
                query_add_adv = 'INSERT INTO "KidsStepShop_advslider" ( "adv_image") ' \
                                + "VALUES ('" + 'static/media/adv_slider/' + adv + "');"
                cur.execute(query_add_adv)
                conn.commit()
                advert = AdvSlider()
                advert.adv_image = 'static/media/adv_slider/' + adv
                advert.save()
        elif request.POST.get("refresh_color"):
            query_clear = 'TRUNCATE TABLE "KidsStepShop_color" CASCADE;'
            cur.execute(query_clear)
            conn.commit()
            Color.objects.all().delete()
            query_add_color = ''
            for c in color_dict:
                query_add_color += 'INSERT INTO "KidsStepShop_color" ("id_color", "name_color") ' \
                                  + "VALUES ('" + color_dict[c] + "', '" + color_dict[c] + "');"
                col = Color()
                col.id_color = color_dict[c]
                col.name_color = color_dict[c]
                col.save()
            cur.execute(query_add_color)
            conn.commit()
        elif request.POST.get("refresh_footwear"):
            query_clear = 'TRUNCATE TABLE "KidsStepShop_footwear" CASCADE; ' \
                          'TRUNCATE TABLE "KidsStepShop_brend" CASCADE; ' \
                          'TRUNCATE TABLE "KidsStepShop_image" CASCADE;' \
                          'TRUNCATE TABLE "KidsStepShop_gender_g_type";'
            cur.execute(query_clear)
            conn.commit()
            Footwear.objects.all().delete()
            Brend.objects.all().delete()
            Image.objects.all().delete()
            for g in Gender.objects.all():
                g.g_type.clear()
            query_vendor = ''
            for b in add_vendor():
                query_vendor += 'INSERT INTO "KidsStepShop_brend" ( "brend") ' + "VALUES ('" + b + "'); "
                br = Brend()
                br.brend = b
                br.save()
            cur.execute(query_vendor)
            conn.commit()
            add_footwear()
    return render(request, 'db_handler.html')


id_cat = []
brend_list = []
size_list = []
tree = ET.parse('static/xml/index.xml')
cat = tree.findall("shop/categories/category[@parentId='1137']")
cat += tree.findall("shop/categories/category[@parentId='1139']")


def add_vendor():
    id_cat = []
    brend_list = []
    for category in cat:
        id_cat.append(category.attrib["id"])
    for id_ in id_cat:
        offer = tree.findall("shop/offers/offer[categoryId='" + id_ + "']")
        for of in offer:
            if not of.find('vendor').text in brend_list:
                brend_list.append(of.find('vendor').text)
    return brend_list


def add_footwear():
    id_cat = []
    for category in cat:
        id_cat.append(category.attrib["id"])
    for id_ in id_cat:
        offer = tree.findall("shop/offers/offer[categoryId='" + id_ + "']")
        for of in offer[:10]:
            gender_list = []
            size_list = []
            color_list = []
            param = of.findall('param')
            ins_type = ''
            for par in param:
                if par.attrib['name'] == 'Размер':
                    size_list.append(par.text)
                if par.attrib['name'] == 'Пол':
                    gender = par.text
                    if gender == 'Мальчикам':
                        gender_list.append('boy')
                    elif gender == 'Девочкам':
                        gender_list.append('girl')
                if par.attrib['name'] == 'Цвет':
                    if par.text in color_list:
                        continue
                    color_list.append(par.text)
                if par.attrib['name'] == 'Тип товара':
                    type = par.text
                    if type == 'Кроссовки':
                        ins_type = 'sneakers'
                    elif type == 'Ботинки':
                        ins_type = 'boots'
                    elif type == 'Сапоги':
                        ins_type = 'high_boots'
                    elif type == 'Сандалии':
                        ins_type = 'sandals'
                    else:
                        ins_type = 'other'

            query_add = ''
            id_ = supplier['berni.com.ua'] + of.attrib['id']
            query_id = 'SELECT id FROM "KidsStepShop_brend" WHERE "brend" = ' + "'" + of.find('vendor').text + "';"
            cur.execute(query_id)
            qq = cur.fetchone()[0]
            query_add += 'INSERT INTO "KidsStepShop_footwear" ' \
                                 '( "id", "name", "popular", "price", "footwear_brend_id", "footwear_type_id") ' \
                                 + "VALUES ('" + id_ + "', '" \
                                 + of.find('name').text + "', '" \
                                 + '0' + "', '" \
                                 + of.find('oldprice').text + "', '" \
                                 + str(qq) + "', '" \
                                 + ins_type + "'); "
            foot = Footwear()
            foot.id = id_
            foot.name = of.find('name').text
            foot.popular = 0
            foot.price = of.find('oldprice').text
            foot.footwear_brend = Brend.objects.get(brend=of.find('vendor').text)
            foot.footwear_type = Type.objects.get(id_type=ins_type)
            foot.save()

            for gen in gender_list:
                cur.execute('SELECT * FROM "KidsStepShop_gender_g_type" WHERE "gender_id" =  '
                            + "'" + gen + "'" + ' AND "type_id" = ' + "'" + ins_type + "';")
                qq = cur.fetchone()
                if not qq:
                    query_add += 'INSERT INTO "KidsStepShop_gender_g_type" ( "gender_id", "type_id") ' \
                                 + "VALUES ('" + gen + "', '" + ins_type + "'); "
                gen_type = Gender.objects.get(id_gender=gen)
                gen_type.g_type.add(Type.objects.get(id_type=ins_type))
                foot.footwear_gender.add(gen)
                query_add += 'INSERT INTO "KidsStepShop_footwear_footwear_gender" ( "footwear_id", "gender_id") ' \
                             + "VALUES ('" + id_ + "', '" + gen + "'); "
            for si in size_list:
                query_add += 'INSERT INTO "KidsStepShop_footwear_size" ( "footwear_id", "size_id") ' \
                              + "VALUES ('" + id_ + "', '" + si + "'); "
                foot.size.add(Size.objects.get(id_size=si))
            for co in color_list:
                query_add += 'INSERT INTO "KidsStepShop_footwear_color" ( "footwear_id", "color_id") ' \
                                          + "VALUES ('" + id_ + "', '" + color_dict[co] + "'); "
                foot.color.add(Color.objects.get(name_color=color_dict[co]))

            imid = 1
            pic_list = []
            for pic in of.findall('picture'):
                img = ImagePIL.open(urlopen(pic.text))
                save_path = 'static/media/footwear/' + id_ + '-' + str(imid) + '.webp'
                pic_list.append(save_path)
                img.save(save_path)
                query_add += 'INSERT INTO "KidsStepShop_image" ( "id_image", "image") ' \
                             + "VALUES ('" + id_ + '-' + str(imid) + "', '" + save_path + "'); " \
                             + 'INSERT INTO "KidsStepShop_footwear_image" ( "footwear_id", "image_id") ' \
                             + "VALUES ('" + id_ + "', '" + id_ + '-' + str(imid) + "'); "
                image = Image()
                image.image = save_path
                image.id_image = id_ + '-' + str(imid)
                image.save()
                foot.image.add(Image.objects.get(id_image=id_ + '-' + str(imid)))
                imid += 1
            cur.execute(query_add)
            conn.commit()
