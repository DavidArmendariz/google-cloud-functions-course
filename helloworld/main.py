def hello_world(request):
    request_args = request.args
    request_json = request.get_json(silent=True)
    if request_args and 'name' in request_args and 'lastname' in request_args:
        name = request_args['name']
        lastname = request_args['lastname']
    elif request_json and 'name' in request_json and 'lastname' in request_json:
        name = request_json['name']
        lastname = request_json['lastname']
    else:
        name = 'World'
        lastname = ''
    return f'Hello {name} {lastname}'
