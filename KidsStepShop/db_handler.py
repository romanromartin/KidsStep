import random
from urllib.request import urlopen
import os
import psycopg2
import xml.etree.ElementTree as ET
from PIL import Image as ImagePIL
from .models import Gender, Type, Footwear, Product, Color, Size, \
    AdvSlider, Order, StatusOrder,  Profile, Brend, TypePrw, Image
# from KidsStepShop.translator import make_translation, get_string
from googletrans import Translator

conn = psycopg2.connect(dbname='d5r03h83qnqmr6', host='ec2-54-155-254-112.eu-west-1.compute.amazonaws.com', port='5432',
                        user="meyvttuswnhyil",
                        password="b88d8d4e9878150f2013cb77683bdefa2e4cb21f05844124f55b77c3349e4b6d")
cur = conn.cursor()
heroku = False
supplier = {'berni.com.ua': 'b-'}

lang = ['en', 'ru', 'uk']

gender_dict = {'girl': ['For girls', 'Для девочек', 'Для дівчаток'],
               'boy': ['For boys', 'Для мальчиков', 'Для хлопчиків']}

type_dict = {'boots': ['Boots', 'Ботинки', 'Черевики'],
             'shoes': ['Shoes', 'Туфли', 'Туфлі'],
             'sneakers': ['Sneakers', 'Кроссовки', 'Кросівки'],
             'high_boots': ['High boots', 'Сапоги', 'Чоботи'],
             'sandals': ['Sandals', 'Сандалии', 'Сандалії'],
             'moccasins': ['Moccasins', 'Мокасины', 'Mокасини'],
             'low_shoes': ['Low shoes', 'Полуботинки', 'Напівчеревики'],
             'ankle_boots': ['Ankle_boots', 'Ботильоны', 'Ботильйони'],
             'rubber_boots': ['Rubber boots', 'Резиновые сапоги', 'Гумові чоботи'],
             'clogs': ['Clogs', 'Сабо', 'Сабо'],
             'slates': ['Slates', 'Сланцы', 'Сланці'],
             'slipons': ['Slipons', 'Слипоны', 'Сліпони'],
             'slippers': ['Slippers', 'Тапочки', 'Капці'],
             'flip_flops': ['Flip flops', 'Шлепки', 'Шльопанці'],
             'other': ['Other', 'Другое', 'Інше'],
             }

color_dict = {'black': ['Black', 'Черный', 'Чорний'],
              'violet': ['Violet', 'Фиолетовый', 'Фіолетовий'],
              'khaki': ['Khaki', 'Хаки', 'Хакi'],
              'blue': ['Blue', 'Синий', 'Синiй'],
              'grey': ['Grey', 'Серый', 'Сірий'],
              'silver': ['Silver', 'Серебряный', 'Срібний'],
              'pink': ['Pink', 'Розовый', 'Рожевий'],
              'peach': ['Peach', 'Персиковый', 'Персиковий'],
              'orange': ['Orange', 'Оранжевый', 'Помаранчевий'],
              'multicolor': ['Multicolor', 'Мультиколор', 'Мультиколор'],
              'milk': ['Milk', 'Молочный', 'Молочний'],
              'crimson': ['Crimson', 'Малиновый', 'Малиновий'],
              'red': ['Red', 'Красный', 'Червоний'],
              'brown': ['Brown', 'Коричневый', 'Коричневий'],
              'green': ['Green', 'Зеленый', 'Зелений'],
              'yellow': ['Yellow', 'Желтый', 'Жовтий'],
              'light_blue': ['Light blue', 'Голубой', 'Блакитний'],
              'turquoise': ['Turquoise', 'Бирюзовый', 'Бірюзовий'],
              'white': ['White', 'Белый', 'Білий'],
              'beige': ['Beige', 'Бежевый', 'Бежевий'],
              'gold': ['Golden', 'Золотой', 'Золотий'],
              }
status_dict = {'new_order': ['New order', 'Новый заказ', 'Нове замовлення'],
               'dispatch_pending': ['Dispatch pending', 'Ожидает отправки', 'Очикує відправлення'],
               'order_was_sent': ['Order was sent', 'Заказ отправлен', 'Замовлення відправлено'],
               'order_received': ['Order received', 'Заказ получен', 'Замовлення отримано'],
               'return_order': ['Return order', 'Возврат заказа', 'Повернення замовлення']
               }

status_prod_list = ['in_cart', 'in_order']

status_order_dict = {

}

id_cat = []

size_list = []
tree = ET.parse('static/xml/index.xml')
cat = tree.findall("shop/categories/category[@parentId='1137']")
cat += tree.findall("shop/categories/category[@parentId='1139']")


def drop_gender_type():
    if heroku:
        query_clear = 'TRUNCATE TABLE "KidsStepShop_gender" CASCADE; ' \
                      'TRUNCATE TABLE "KidsStepShop_type" CASCADE; ' \
                      'TRUNCATE TABLE "KidsStepShop_typeprw" CASCADE; '
        cur.execute(query_clear)
        conn.commit()
    Gender.objects.all().delete()
    Type.objects.all().delete()
    TypePrw.objects.all().delete()



def add_types():
    query_add_type = ''
    for t in type_dict:
        if heroku:
            query_add_type += 'INSERT INTO "KidsStepShop_type" ( "id_type") ' \
                              + "VALUES ('" + t + "'); "
        # type_to_add = Type(id_type=t, type=type_dict[t])
        type_to_add = Type(id_type=t)
        type_to_add.save()
        for l in lang:
            type_to_add.set_current_language(l)
            type_to_add.type = type_dict[t][lang.index(l)]
            type_to_add.save()
            if heroku:
                query_add_type += 'INSERT INTO "KidsStepShop_type_translation" ( "language_code", "type", "master_id") ' \
                                  + "VALUES ('" + l + "', '" + type_dict[t][lang.index(l)] + "', '" + t + "'); "


    if heroku:
        cur.execute(query_add_type)
        conn.commit()


def add_gender_and_typeprw():
    query_add_gender = ''
    for g in gender_dict:
        if heroku:
            query_add_gender += 'INSERT INTO "KidsStepShop_gender" ( "id_gender") ' \
                                + "VALUES ('" + g + "'); "
        # gender = Gender(id_gender=g, gender = gender_dict[g])
        gender_to_add = Gender(id_gender=g)
        gender_to_add.save()
        for l in lang:
            gender_to_add.set_current_language(l)
            gender_to_add.gender = gender_dict[g][lang.index(l)]
            gender_to_add.save()
            if heroku:
                query_add_gender += 'INSERT INTO "KidsStepShop_gender_translation" ( "language_code", "gender", "master_id") ' \
                                    + "VALUES ('" + l + "', '" + gender_dict[g][lang.index(l)] + "', '" + g + "'); "

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
            if heroku:
                query_add_gender += 'INSERT INTO "KidsStepShop_typeprw" ( "prw_image", "prw_gender_id", "prw_type_id") ' \
                                    + "VALUES ('" + img + "', '" + g + "', '" + t.id_type + "'); "
    if heroku:
        cur.execute(query_add_gender)
        conn.commit()


def drop_size():
    if heroku:
        query_clear = 'TRUNCATE TABLE "KidsStepShop_size" CASCADE; '
        cur.execute(query_clear)
        conn.commit()
    Size.objects.all().delete()

def drop_status_order():
    if heroku:
        query_clear = 'TRUNCATE TABLE "KidsStepShop_statusorder" CASCADE; '
        cur.execute(query_clear)
        conn.commit()
    StatusOrder.objects.all().delete()

def add_status_order():
    query_add_status = ''
    for s in status_dict:
        status_to_add = StatusOrder(id_status_order=s)
        status_to_add.save()
        for l in lang:
            status_to_add.set_current_language(l)
            status_to_add.status = status_dict[s][lang.index(l)]
            status_to_add.save()




def add_sizes():
    query_add_size = ''
    for s in range(1, 46):
        if heroku:
            query_add_size += 'INSERT INTO "KidsStepShop_size" ("id_size", "size") ' \
                              + "VALUES ('" + str(s) + "', '" + str(s) + "'); "
        size = Size(id_size=s, size=s)
        size.save()
    if heroku:
        cur.execute(query_add_size)
        conn.commit()


def drop_advslider():
    if heroku:
        query_clear = 'TRUNCATE TABLE "KidsStepShop_advslider";'
        cur.execute(query_clear)
        conn.commit()
    AdvSlider.objects.all().delete()


def add_advslider():
    dir_adv = os.listdir('static/media/adv_slider/')
    query_add_adv = ''
    for adv in dir_adv:
        if adv == 'default.webp':
            continue
        if heroku:
            query_add_adv += 'INSERT INTO "KidsStepShop_advslider" ( "adv_image") ' \
                            + "VALUES ('" + 'static/media/adv_slider/' + adv + "'); "

        advert = AdvSlider(adv_image='static/media/adv_slider/' + adv)
        advert.save()
    if heroku:
        cur.execute(query_add_adv)
        conn.commit()


def drop_colors():
    if heroku:
        query_clear = 'TRUNCATE TABLE "KidsStepShop_color" CASCADE;'
        cur.execute(query_clear)
        conn.commit()
    Color.objects.all().delete()


def add_colors():
    query_add_color = ''
    for c in color_dict:
        if heroku:
            query_add_color += 'INSERT INTO "KidsStepShop_color" ("id_color") ' \
                               + "VALUES ('" + c + "'); "
        col = Color(id_color=c)
        col.save()
        for l in lang:
            col.set_current_language(l)
            col.name_color = color_dict[c][lang.index(l)]
            col.save()
            if heroku:
                query_add_color += 'INSERT INTO "KidsStepShop_color_translation" ("language_code", "name_color", "master_id") ' \
                                   + "VALUES ('" + l + "', '" + color_dict[c][lang.index(l)] + "', '" + c + "'); "

    if heroku:
        cur.execute(query_add_color)
        conn.commit()


def drop_footwear():
    if heroku:
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


def add_vendor():
    query_vendor = ''
    for b in find_vendor():
        if heroku:
            query_vendor += 'INSERT INTO "KidsStepShop_brend" ( "brend") ' + "VALUES ('" + b + "'); "
        br = Brend(brend=b)
        br.save()
    if heroku:
        cur.execute(query_vendor)
        conn.commit()


def find_vendor():
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

translator = Translator()

def add_footwear():
    id_cat = []
    for category in cat:
        id_cat.append(category.attrib["id"])
    for id_ in id_cat:
        offer = tree.findall("shop/offers/offer[categoryId='" + id_ + "']")
        for of in offer[:20]:
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
            if heroku:
                query_id = 'SELECT id FROM "KidsStepShop_brend" WHERE "brend" = ' + "'" + of.find('vendor').text + "';"
                cur.execute(query_id)
                qq = cur.fetchone()[0]
                query_add += 'INSERT INTO "KidsStepShop_footwear" ' \
                             '( "id",  "popular", "price", "footwear_brend_id", "footwear_type_id") ' \
                             + "VALUES ('" + id_ + "', '" \
                             + '0' + "', '" \
                             + of.find('oldprice').text + "', '" \
                             + str(qq) + "', '" \
                             + ins_type + "'); "
            foot = Footwear(id=id_,
                            popular=0,
                            price=of.find('oldprice').text,
                            footwear_brend=Brend.objects.get(brend=of.find('vendor').text),
                            footwear_type=Type.objects.get(id_type=ins_type))
            foot.save()

            for l in lang:
                foot.set_current_language(l)
                if l != 'ru':
                    # name = 'name'
                    print('------------!!!', of.find('name').text)
                    name = translator.translate(text=of.find('name').text, dest=l, src='ru').text
                    # name = translate_string(of.find('name').text, from_lang='ru', to_lang=l)
                else:
                    name = of.find('name').text
                if heroku:
                    print(name)
                    edit_name = name.replace("'", "`")
                    query_add += 'INSERT INTO "KidsStepShop_footwear_translation" ("language_code", "name", "master_id") ' \
                                       + "VALUES ('" + l + "', '" + edit_name + "', '" + id_ + "'); "
                foot.name = name
                foot.save()
            # if <param> "Пол" field in XML feed is absent '''''~~``` children`s
            if gender_list == []:
                if of.find('name').text.find('мальч') > 0:
                    gender_list.append('boy')
                elif of.find('name').text.find('девоч') > 0:
                    gender_list.append('girl')
                else:
                    gender_list.append('unknown')
            for gen in gender_list:
                if heroku:
                    cur.execute('SELECT * FROM "KidsStepShop_gender_g_type" WHERE "gender_id" =  '
                                + "'" + gen + "'" + ' AND "type_id" = ' + "'" + ins_type + "';")
                    qq = cur.fetchone()
                    if not qq:
                        query_add += 'INSERT INTO "KidsStepShop_gender_g_type" ( "gender_id", "type_id") ' \
                                     + "VALUES ('" + gen + "', '" + ins_type + "'); "
                gen_type = Gender.objects.get(id_gender=gen)
                gen_type.g_type.add(Type.objects.get(id_type=ins_type))
                foot.footwear_gender.add(gen)
                if heroku:
                    query_add += 'INSERT INTO "KidsStepShop_footwear_footwear_gender" ( "footwear_id", "gender_id") ' \
                                 + "VALUES ('" + id_ + "', '" + gen + "'); "
            for si in size_list:
                if heroku:
                    query_add += 'INSERT INTO "KidsStepShop_footwear_size" ( "footwear_id", "size_id") ' \
                                 + "VALUES ('" + id_ + "', '" + si + "'); "
                foot.size.add(Size.objects.get(id_size=si))
            for co in color_list:
                for egg in color_dict:
                    if co == color_dict[egg][1]:
                        foot.color.add(Color.objects.get(id_color=egg))
                        if heroku:
                            query_add += 'INSERT INTO "KidsStepShop_footwear_color" ( "footwear_id", "color_id") ' \
                                         + "VALUES ('" + id_ + "', '" + egg + "'); "

            imid = 1
            pic_list = []
            for pic in of.findall('picture'):
                img = ImagePIL.open(urlopen(pic.text))
                bg = ImagePIL.new(mode='RGB', size=(800, 800), color=(255, 255, 255))
                if img.width >= img.height:
                    img = img.resize(size=(800, round(800*(img.height/img.width))))
                    bg.paste(im=img, box=(0, round((bg.height - img.height)/2)))
                else:
                    img = img.resize(size=(round(800*(img.height/img.width)), 800 ))
                    bg.paste(im=img, box=(round((bg.width - img.width) / 2), 0))


                save_path = 'static/media/footwear/' + id_ + '-' + str(imid) + '.webp'
                pic_list.append(save_path)
                bg.save(save_path)
                if heroku:
                    query_add += 'INSERT INTO "KidsStepShop_image" ( "id_image", "image") ' \
                                 + "VALUES ('" + id_ + '-' + str(imid) + "', '" + save_path + "'); " \
                                 + 'INSERT INTO "KidsStepShop_footwear_image" ( "footwear_id", "image_id") ' \
                                 + "VALUES ('" + id_ + "', '" + id_ + '-' + str(imid) + "'); "
                image = Image(image=save_path, id_image=id_ + '-' + str(imid))
                image.save()
                foot.image.add(Image.objects.get(id_image=id_ + '-' + str(imid)))
                imid += 1
            if heroku:

                cur.execute(query_add)
                conn.commit()






def translate_string(text, from_lang, to_lang):
    translator = Translator()
    result = translator.translate(text=text, dest=to_lang, src=from_lang)
    return result.text

def count_footwear():
    id_cat = []
    for category in cat:
        id_cat.append(category.attrib["id"])
    for id_ in id_cat:
        offer = tree.findall("shop/offers/offer[categoryId='" + id_ + "']")
        print(len(offer))