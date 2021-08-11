import os
from PIL import Image

path = 'converter'
inc = path + '/incoming'
webp = path + '/webp'
to_png = path + '/to_png'

if not os.path.exists(inc):
    os.mkdir(inc)
if not os.path.exists(to_png):
    os.mkdir(to_png)
if not os.path.exists(webp):
    os.mkdir(webp)

for file in os.listdir(path):
    full_path = path + '/' + file
    if os.path.isfile(full_path):
        try:
            im = Image.open(full_path)
            if os.path.splitext(file)[1] == '.webp':
                im.save(to_png + '/' + os.path.splitext(file)[0] + '.png')
            else:
                im.save(webp + '/' + os.path.splitext(file)[0] + '.webp')
        except:
            print('incorrect format  ' + file)
        finally:
            os.rename(full_path, inc + '/' + file)

