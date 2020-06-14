from decimal import Decimal


"""Groups"""
ROLE_ADMIN = 'Admin'
ROLE_MANAGEMENT = 'Management'
ROLE_STAFF = 'Staff'
ROLE_SUPPLIER = 'Supplier'
ROLE_GUEST = 'Guest'


"""Rates"""
ADVANCE = Decimal('0.9')
RETENTION = Decimal('0.1')

"""Environments"""
LOCAL = 'LOCAL'
PRODUCTION = 'PRODUCTION'
STAGING = 'STAGING'
DEMO = 'DEMO'
TESTING = 'TESTING'
