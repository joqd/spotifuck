from pony import orm
from datetime import datetime
from . import db

class User(db.Entity):
    id = orm.PrimaryKey(int, size=64)
    name = orm.Required(str)
    last_request_at = orm.Optional(datetime)
    joined_at = orm.Required(datetime)