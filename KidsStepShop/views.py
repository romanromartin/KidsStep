from django.shortcuts import render, redirect, get_object_or_404
import xml.etree.ElementTree as ET
from .models import Gender, Type, Footwear, Color, Size, \
    AdvSlider, Order, StatusOrder, Profile, Brend, TypePrw, Image, Product
from django.contrib.auth import authenticate, login, logout, models
from KidsStepShop.forms import SignUpForm, LogInForm, ResetPasswordForm, OrderForm
from django.conf import settings
from Base.settings import CART_SESSION_ID
import random
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.utils.translation import ugettext as _
import os
import psycopg2
from PIL import Image as ImagePIL
from urllib.request import urlopen
import KidsStepShop.db_handler as handler
from django.contrib.auth.models import User

gender = Gender.objects.all()
types = Type.objects.all()
supplier = {'berni.com.ua': 'b-'}


def index(request):
    gender = Gender.objects.all()
    fw_pop = Footwear.objects.all().order_by('-popular')
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
                  context={'gender': gender, 'popular': popular_footwear, 'adv': adv, 'dots_start': dots_start,
                           'dots_end': dots_end})


def type(request, id_gender):
    gender = Gender.objects.all()
    print('!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!', id_gender)
    prw_list = TypePrw.objects.filter(prw_gender=id_gender)
    return render(request, 'type.html',
                  context={'gender': gender, 'nav_gender': navigation_gender(id_gender), 'prw_list': prw_list})


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
                           'nav_gender': navigation_gender(id_gender), 'nav_type': navigation_type(id_type),
                           'dots_start': dots_start, 'dots_end': dots_end})


def footwear_detail(request, id_gender, id_type, id):
    gender = Gender.objects.all()
    err = ''
    fw_sel = Footwear.objects.get(id=id)
    fw_sel.popular += 1
    fw_sel.save()

    fw_quantity = list(range(2, 11))
    if request.method == 'POST':
        if request.POST.get("add_to_cart"):
            if request.POST.get("size") is None:
                err = 'Не выбран размер '
            else:
                foo = [[id, id_gender, id_type, request.POST.get("size"), request.POST.get("quantity")]]
                if request.session.get(CART_SESSION_ID):
                    request.session[CART_SESSION_ID] += foo
                else:
                    request.session[CART_SESSION_ID] = foo
                return redirect('basket')
    return render(request, 'footwear_detail.html',
                  context={'gender': gender, 'types': types, 'nav_type': navigation_type(id_type),
                           'nav_gender': navigation_gender(id_gender),
                           'form_error': err, 'fw_sel': fw_sel, 'fw_quantity': fw_quantity})


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
    total_price, user_product = make_product_list(request)
    if request.method == 'POST':
        if request.POST.get("delete"):
            request.session.get(CART_SESSION_ID).pop(int(request.POST.get("delete")))
            request.session[CART_SESSION_ID] = request.session.get(CART_SESSION_ID)
            return redirect('basket')
        if request.POST.get("to_order"):
            return redirect('order')
    return render(request, 'basket.html', context={'user_product': user_product, 'total': total_price})


def make_product_list(request):
    total_price = 0
    ind = 0
    user_product = []
    if request.session.get(CART_SESSION_ID):
        for prod in request.session.get(CART_SESSION_ID):
            product = Footwear.objects.get(id=prod[0])
            total_price += product.price * int(prod[4])
            user_product.append([ind, prod[1], prod[2], product, prod[3], prod[4]])
            ind += 1
    return total_price, user_product


def anonimus(request):
    us = User()
    us.username = 'dhsdw2342sdfsf'
    us.password = 'anonimus'
    us.save()
    return render(request, 'registration/anonimus.html')


def randomizer(inputQuery):
    new_num = 0
    num_list = []
    while new_num == 0:
        number = random.randrange(1000, 9999)
        for article_in_use in inputQuery:
            num_list.append(article_in_use.article)
            if number not in num_list:
                new_num = number
    return new_num


def order(request):
    err = ''
    total_price, user_product = make_product_list(request)
    if request.method == 'POST':
        orderForm = OrderForm(request.POST)
        if request.POST.get("done"):
            orderSet = Order()
            if request.user.is_authenticated:
                orderSet.user_order = request.user.username
            else:
                new_num = 0
                while new_num == 0:
                    number = random.randrange(1000, 9999)
                    for user in User.objects.all():
                        if user != 'anonimus_' + str(number):
                            new_num = number
                us = User.objects.create(first_name=orderForm['username'].data,
                                         username='anonimus_' + str(new_num),
                                         password='anonimus')
                us.save()
                us.refresh_from_db()
                us.profile.phone = orderForm['phone'].data
                us.save()
                orderSet.user_order = us.username
            orderSet.delivery = orderForm['delivery'].data \
                                + ', ' + orderForm['city'].data \
                                + ', ' + orderForm['department'].data
            # orderSet.status = StatusOrder.objects.get(status='В работе')
            new_article = 0
            article_in_use_list = []
            for article_in_use in Order.objects.all():
                article_in_use_list.append(article_in_use.article)
            while new_article == 0:
                number = random.randrange(1000, 9999)
                if number not in article_in_use_list:
                    new_article = number
            orderSet.article = new_article
            orderSet.status = StatusOrder.objects.get(id_status_order='new_order')
            orderSet.save()

            for prod in user_product:
                print(prod)
                product_in_order = Product()
                product_in_order.order = Order.objects.get(article=orderSet.article)
                product_in_order.product = prod[3]
                product_in_order.size = Size.objects.get(size=prod[4])
                product_in_order.quantity = prod[5]
                product_in_order.save()

            request.session[CART_SESSION_ID] = request.session.get(CART_SESSION_ID).clear()
            return redirect('order_done', new_article)
    else:
        orderForm = OrderForm()
    return render(request, 'order.html',
                  context={'user_product': user_product, 'total': total_price, 'form_error': err, 'form': orderForm,
                           'anonimus_name': '', 'anonimus_phone': ''})





def profile(request):
    return render(request, 'registration/profile.html')


def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        print(request.POST)
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



def order_done(request, article):
    ord = Order.objects.get(article=article)
    total_price = 0
    for n in ord.product_set.all():
        total_price += n.quantity*n.product.price

    print(total_price)
    return render(request, 'order_done.html',
                  context={'article': article, 'order': ord, 'total_price': total_price})


def managment(request):
    orders = Order.objects.all()
    stat = StatusOrder.objects.all()
    for ord in orders:
        if ord.product_set.all().count() < 1:
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
            new_status = StatusOrder.objects.get(translations__status=request.POST.get("change_status"))
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
    paginator = Paginator(s_f, 16)
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
    return render(request, 'search.html',
                  context={'search': s_f, 'gender': gender, 'types': types,
                           'dots_start': dots_start, 'dots_end': dots_end, 'footwear_selected': page_footwear,})


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
        elif request.POST.get("refresh_status_order"):
            handler.drop_status_order()
            handler.add_status_order()
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
            print(handler.translate_string('Добавить Нижний Колонтитул на каждой странице с текстом', from_lang='ru', to_lang='en'))

    return render(request, 'db_handler.html')


id_cat = []
brend_list = []
size_list = []
tree = ET.parse('static/xml/index.xml')
cat = tree.findall("shop/categories/category[@parentId='1137']")
cat += tree.findall("shop/categories/category[@parentId='1139']")
