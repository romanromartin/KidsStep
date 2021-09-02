from django.shortcuts import render, redirect
import xml.etree.ElementTree as ET
from .models import Gender, Type, Footwear, Product, Color, Size, \
    AdvSlider, Order, StatusOrder, StatusProduct, Profile, Brend, TypePrw, Image
from django.contrib.auth import authenticate, login, logout, models
from KidsStepShop.forms import SignUpForm, LogInForm, ResetPasswordForm
from django.conf import settings
import random
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.utils.translation import ugettext as _
import os
import psycopg2
from PIL import Image as ImagePIL
from urllib.request import urlopen
import KidsStepShop.db_handler as handler


gender = Gender.objects.all()
types = Type.objects.all()
supplier = {'berni.com.ua': 'b-'}


def index(request):
    gender = Gender.objects.all()
    fw_pop = Footwear.objects.all().order_by('-popular')[:30]
    paginator = Paginator(fw_pop, 16)
    page = request.GET.get('page')
    if not page:
        page = '1'
    dots_start = False
    dots_end = False
    if int(page) > 3:
        dots_start = True
    if int(page) < paginator.num_pages - 2:
        dots_end = True
    try:
        popular_footwear = paginator.page(page)
    except PageNotAnInteger:
        popular_footwear = paginator.page(1)
    except EmptyPage:
        popular_footwear = paginator.page(paginator.num_pages)
    adv = AdvSlider.objects.all()
    return render(request, 'index.html',
                  context={'gender': gender, 'popular': popular_footwear, 'adv': adv, 'dots_start': dots_start, 'dots_end': dots_end})


def type(request, id_gender):
    gender = Gender.objects.all()
    print('!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!',id_gender)
    prw_list = TypePrw.objects.filter(prw_gender=id_gender)
    return render(request, 'type.html',
                  context={'gender': gender,   'nav_gender': navigation_gender(id_gender), 'prw_list': prw_list})


def footwear(request, id_gender, id_type):
    gender = Gender.objects.all()
    footwear = Footwear.objects.filter(footwear_gender__id_gender=id_gender, footwear_type__id_type=id_type)
    paginator = Paginator(footwear, 16)
    page = request.GET.get('page')
    if not page:
        page = '1'
    dots_start = False
    dots_end = False
    if int(page) > 3:
        dots_start = True
    if int(page) < paginator.num_pages - 2:
        dots_end = True

    try:
        page_footwear = paginator.page(page)
    except PageNotAnInteger:
        page_footwear = paginator.page(1)
    except EmptyPage:
        page_footwear = paginator.page(paginator.num_pages)

    return render(request, 'footwear.html',
                  context={'gender': gender, 'types': types, 'footwear_selected': page_footwear,
                           'nav_gender': navigation_gender(id_gender), 'nav_type': navigation_type(id_type),'dots_start': dots_start, 'dots_end': dots_end})


def footwear_detail(request, id_gender, id_type, id):
    gender = Gender.objects.all()
    err = ''
    fw_sel = Footwear.objects.get(id=id)
    fw_sel.popular += 1
    fw_sel.save()
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


conn = handler.conn
cur = handler.cur

def db_handler(request):
    if request.method == 'POST':
        if request.POST.get("refresh_ge_ty"):
            handler.drop_gender_type()
            handler.add_types()
            handler.add_gender_and_typeprw()
        elif request.POST.get("refresh_size"):
            handler.drop_size()
            handler.add_sizes()
        elif request.POST.get("refresh_adv_slider"):
            handler.drop_advslider()
            handler.add_advslider()
        elif request.POST.get("refresh_color"):
            handler.drop_colors()
            handler.add_colors()
        elif request.POST.get("refresh_footwear"):
            handler.drop_footwear()
            handler.add_vendor()
            handler.add_footwear()
        elif request.POST.get("add_footwear"):
            handler.add_footwear()

    return render(request, 'db_handler.html')


id_cat = []
brend_list = []
size_list = []
tree = ET.parse('static/xml/index.xml')
cat = tree.findall("shop/categories/category[@parentId='1137']")
cat += tree.findall("shop/categories/category[@parentId='1139']")






