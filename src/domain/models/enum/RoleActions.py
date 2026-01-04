from enum import Enum


class RoleActions(str, Enum):
    # Generic
    ADMIN = '*'
    # padrão
    GET = 'g'
    POST = 'p'
    UPDATE = 'u'
    DELETE = 'd'
