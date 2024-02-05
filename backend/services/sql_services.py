from sqlalchemy.orm import object_mapper

def to_dict(obj):
    return {column.key: getattr(obj, column.key) for column in object_mapper(obj).columns}
