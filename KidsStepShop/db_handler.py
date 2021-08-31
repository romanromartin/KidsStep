import random
from urllib.request import urlopen
import os
import psycopg2
import xml.etree.ElementTree as ET
from PIL import Image as ImagePIL
from .models import Gender, Type, Footwear, Product, Color, Size, \
    AdvSlider, Order, StatusOrder, StatusProduct, Profile, Brend, TypePrw, Image
# from KidsStepShop.translator import make_translation, get_string
from googletrans import Translator

conn = psycopg2.connect(dbname='dd5i5im27p4ds0', host='ec2-52-19-164-214.eu-west-1.compute.amazonaws.com', port='5432',
                        user="numiptpdffecdm",
                        password="48c643d4ed63f9d131276650289414d21eac015f53c4cb958408e61e5f082abe")
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

# color_dict = {'Черный': 'black', 'Фиолетовый': 'violet', 'Хаки': 'khaki', 'Синий': 'blue', 'Серый': 'grey',
#               'Серебряный': 'silver', 'Розовый': 'pink', 'Персиковый': 'peach', 'Оранжевый': 'orange',
#               'Мультиколор': 'multicolor', 'Молочный': 'milk', 'Малиновый': 'crimson', 'Красный': 'red',
#               'Коричневый': 'brown', 'Зеленый': 'green', 'Желтый': 'yellow', 'Голубой': 'light_blue',
#               'Бирюзовый': 'turquoise', 'Белый': 'white', 'Бежевый': 'beige', 'Золотой': 'gold'}

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
            query_add_type += 'INSERT INTO "KidsStepShop_type" ( "id_type", "type") ' \
                              + "VALUES ('" + t + "', '" + type_dict[t] + "'); "
        # type_to_add = Type(id_type=t, type=type_dict[t])
        type_to_add = Type(id_type=t)
        type_to_add.save()
        for l in lang:
            type_to_add.set_current_language(l)
            type_to_add.type = type_dict[t][lang.index(l)]
            type_to_add.save()

    if heroku:
        cur.execute(query_add_type)
        conn.commit()


def add_gender_and_typeprw():
    query_add_gender = ''
    for g in gender_dict:
        if heroku:
            query_add_gender += 'INSERT INTO "KidsStepShop_gender" ( "id_gender", "gender") ' \
                                + "VALUES ('" + g + "', '" + gender_dict[g] + "'); "
        # gender = Gender(id_gender=g, gender = gender_dict[g])
        gender_to_add = Gender(id_gender=g)
        gender_to_add.save()
        for l in lang:
            gender_to_add.set_current_language(l)
            gender_to_add.gender = gender_dict[g][lang.index(l)]
            gender_to_add.save()

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
            query_add_adv = 'INSERT INTO "KidsStepShop_advslider" ( "adv_image") ' \
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
            query_add_color += 'INSERT INTO "KidsStepShop_color" ("id_color", "name_color") ' \
                               + "VALUES ('" + color_dict[c] + "', '" + color_dict[c] + "'); "
        col = Color(id_color=c)
        col.save()
        for l in lang:
            col.set_current_language(l)
            col.name_color = color_dict[c][lang.index(l)]
            col.save()
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


def add_footwear():
    id_cat = []
    for category in cat:
        id_cat.append(category.attrib["id"])
    for id_ in id_cat:
        offer = tree.findall("shop/offers/offer[categoryId='" + id_ + "']")
        for of in offer[:1]:
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
                             '( "id", "name", "popular", "price", "footwear_brend_id", "footwear_type_id") ' \
                             + "VALUES ('" + id_ + "', '" \
                             + of.find('name').text + "', '" \
                             + '0' + "', '" \
                             + of.find('oldprice').text + "', '" \
                             + str(qq) + "', '" \
                             + ins_type + "'); "
            foot = Footwear(id=id_,
                            # name=of.find('name').text,
                            popular=0,
                            price=of.find('oldprice').text,
                            footwear_brend=Brend.objects.get(brend=of.find('vendor').text),
                            footwear_type=Type.objects.get(id_type=ins_type))
            foot.save()

            foot.set_current_language('ru')
            foot.name = of.find('name').text
            foot.save()
            foot.set_current_language('en')
            foot.name = translate_string(of.find('name').text, from_lang='ru', to_lang='en')
            foot.save()
            foot.set_current_language('uk')
            foot.name = translate_string(of.find('name').text, from_lang='ru', to_lang='uk')
            foot.save()
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
                                         + "VALUES ('" + id_ + "', '" + color_dict[co] + "'); "

            imid = 1
            pic_list = []
            for pic in of.findall('picture'):
                img = ImagePIL.open(urlopen(pic.text))
                save_path = 'static/media/footwear/' + id_ + '-' + str(imid) + '.webp'
                pic_list.append(save_path)
                img.save(save_path)
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
