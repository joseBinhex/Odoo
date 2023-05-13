import xmlrpc.client
url = 'http://10.1.0.50/' # odoo instance url
database = 'jmendezDB' # database name
user = 'j.mendez@binhex.es' # username
password = 'df871f178c766afcf65236fcf2a60ee080d7ecaf' 
common = xmlrpc.client.ServerProxy('{}/xmlrpc/2/common'.format(url))
uid = common.authenticate(database, user, password, {})

model = xmlrpc.client.ServerProxy('{}/xmlrpc/2/object'.format(url))

sessions_name = model.execute_kw(database, uid, password, 'openacademy.courses', 'search_read',[[['name','!=', False]]])
for x in sessions_name:
    print(x)


args = {
    'name' : "Course with xmlrpc",
    'finish_date' : '2023-03-23',
    'duration': 100,
    'max_seats': 30,
    'number_seats': 23,
    'instructor': "",
    'course_name': 1,
    'date_start': '2023-03-23',
    'attendees_count': 7,
    'taken_seats': 7,
}

sessions_create = model.execute(database, uid, password, 'openacademy.sessions', 'create', args)

sessions_name = model.execute_kw(database, uid, password, 'openacademy.sessions', 'search_read',[[['name','!=', False]]], {'fields': ['name', 'taken_seats']})
for x in sessions_name:
    print(x)