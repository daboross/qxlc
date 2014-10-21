import codecs
import hashlib
import os

import magic
import sys

if 'pastes' in sys.argv:
    while True:
        try:
            line = input()
        except EOFError:
            break
        _id, md5 = line.split('|')
        filename = os.path.join("data", "pastes", _id)
        with codecs.open(filename, 'r', encoding='utf-8') as f:
            realmd5 = hashlib.md5(f.read().strip().encode()).hexdigest()
        if realmd5 != md5:
            print("UPDATE qxlc_data SET data = '{}' where id = {};".format(realmd5, _id))
elif 'images' in sys.argv:
    with magic.Magic(flags=magic.MAGIC_MIME_TYPE) as m:
        while True:
            try:
                line = input()
            except EOFError:
                break
            _id, md5 = line.split('|')
            if ':' in md5:
                image_type, md5 = md5.split(':')
            else:
                image_type = None
            filename = os.path.join("data", "images", _id)
            with codecs.open(filename, 'rb') as f:
                realmd5 = hashlib.md5(f.read()).hexdigest()
            real_image_type = m.id_filename(filename)
            if realmd5 != md5 or real_image_type != image_type:
                print("UPDATE qxlc_data SET data = '{}:{}' where id = {};".format(real_image_type, realmd5, _id))
else:
    print("Usage: {} pastes|images".format(sys.argv[0]))
