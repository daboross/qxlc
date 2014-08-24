from datetime import datetime
from sqlalchemy import MetaData, create_engine, Table, Column, String, select

from sqlalchemy.orm import sessionmaker
from sqlalchemy.sql.sqltypes import Integer, DateTime

from qxlc import config

db_path = config.get('database')
db_engine = create_engine(db_path)
db_session = sessionmaker(bind=db_engine)
metadata = MetaData()

data_table = Table(
    "qxlc_data",
    metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("type", Integer),
    Column("data", String),
    Column("upload", DateTime),
    Column("access", DateTime)
)

if not data_table.exists(db_engine):
    data_table.create(db_engine)

type_id_to_name = {0: "url", 1: "paste", 2: "image"}
type_name_to_id = {'url': 0, "paste": 1, "image": 2}


def type_id(_type_name):
    return type_name_to_id[_type_name]


def type_name(_type_id):
    return type_id_to_name[_type_id]

# ---------------
# URL ID Encoding
# ---------------

valid_digits = "Q9TGiDx3eaRnvEgpHWqAmVIjzX14JsfcLl6SZ7b0YFuw2Kk8O5CBrNohyPtdUM"
# valid_digits is actually `string.ascii_letters + string.digits`,
# just shuffled so it looks random
len_digits = len(valid_digits)
# 238328 is the first id with a 4-digit encoded url, so we just add 238328 to all internal ids before encoding them,
# in order to have only 4-digit urls
minimum_id = 238328


def encode_id(x):
    x += minimum_id
    result = []
    while x != 0:
        x, remainder = divmod(x, len_digits)
        result.append(valid_digits[remainder])
    return "".join(result)


def decode_id(s):
    x = 0
    for c in s[::-1]:
        x = x * len_digits + valid_digits.index(c)
    # 3844 is the first 4-digit id, so the id '1' is mapped to the first possible four-digit URL
    return x - minimum_id


# --------------------------------
# External database access methods
# --------------------------------

class DataNotFound(ValueError):
    pass


def store_data(data_type, data):
    """
    Stores data in the database under type = data_type. Returns the integer id, which can then be encoded with
    encode_id()
    :type data_type: str | int
    :type data: str
    :rtype: int
    """
    if isinstance(data_type, str):
        data_type = type_id(data_type)

    db = db_session()
    insert_result = None
    select_result = None
    try:
        select_result = db.execute(select([data_table.c.id]).where(data_table.c.type == data_type)
                                   .where(data_table.c.data == data))
        row = select_result.fetchone()
        if row is not None:
            # we should have only one row, and we only select for one column, so just use fetchone()[0]
            return row[0]
        else:
            time = datetime.utcnow()
            insert_result = db.execute(data_table.insert().values(type=data_type, data=data, upload=time, access=time))
            db.commit()
            return insert_result.inserted_primary_key[0]
    finally:
        if select_result is not None:
            select_result.close()
        if insert_result is not None:
            insert_result.close()
        db.close()


def get_data(data_id):
    """
    Gets data stored under the given id. Returns the integer type, and the data stored
    :type data_id: int
    :rtype: (int, str)
    """

    db = db_session()
    select_result = None
    try:
        select_result = db.execute(select([data_table.c.type, data_table.c.data]).where(data_table.c.id == data_id))

        row = select_result.fetchone()

        if row is not None:
            db.execute(data_table.update().where(data_table.c.id == data_id).values(access=datetime.utcnow()))
            # First is type, second is data. This is specified above.
            return row[0], row[1]
        else:
            raise DataNotFound
    finally:
        if select_result is not None:
            select_result.close()
        db.commit()
        db.close()
