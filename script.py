import codecs
import hashlib
import os
import sys

while True:
    try:
        line = input()
    except EOFError:
        sys.exit()
    _id, md5 = line.split('|')
    filename = os.path.join("data", "pastes", _id)
    with codecs.open(filename, 'r', encoding='utf-8') as f:
        realmd5 = hashlib.md5(f.read().strip().encode()).hexdigest()
    if realmd5 != md5:
        print("UPDATE qxlc_data SET data = '{}' where id = {};".format(realmd5, _id))
