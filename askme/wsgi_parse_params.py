# curl -X GET 'http://127.0.0.1:8081?a=1&b=2'
# curl -X POST 'http://127.0.0.1:8081' -H "Content-Type: application/x-www-form-urlencoded;charset=UTF-8" -d "object=type&char=a"

def application(environ, start_response):
    source = environ['QUERY_STRING']
    if environ['REQUEST_METHOD'] == 'POST':
        source = environ['wsgi.input'].read().decode('utf-8')

    params = ', '.join(
        [param for param in source.split('&')]
    )

    data = b'Request handled:\n' \
           + f'{environ["REQUEST_METHOD"]}\n'.encode() \
           + f'{params}\n'.encode()

    start_response('200 OK', (
        ('Content-Type', 'text/plain'),
        ('Content-Length', str(len(data)))
    ))
    return [data]
