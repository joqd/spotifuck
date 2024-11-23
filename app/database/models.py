from pony import orm
from datetime import datetime
from . import db

class User(db.Entity):
    id = orm.PrimaryKey(int, size=64)
    name = orm.Required(str)
    joined_at = orm.Required(datetime)