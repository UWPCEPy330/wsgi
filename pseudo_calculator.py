import pysnooper

"""
This pseudo calculator should support the following operations:

  * Positive
  * Negative

Your users should be able to send appropriate requests and get back
proper responses. For example, if I open a browser to your wsgi
application at `http://localhost:8080/positive/5' then the response
body in my browser should be `true`.

Consider the following URL/Response body pairs as tests:

```
  http://localhost:8080/positive/5  => 'true'
  http://localhost:8080/positive/0  => 'false'
  http://localhost:8080/positive/-5 => 'false'
  http://localhost:8080/negative/0  => 'false'
  http://localhost:8080/negative/-2 => 'true'
```

"""
@pysnooper.snoop()
def func(sign, *args):

    response = ''

    if sign == 'positive':
        for arg in args:
            print('check positive called on ' + arg)
            if int(arg) >= 0:
                response = 'True'
            else:
                response = 'False'
    elif sign == 'negative':
        for arg in args:
            print('check negative called on ' + arg)
            if int(arg) < 0:
                return 'True'
            else:
                return 'False'
    else:
        print('no func called')
        raise NameError

    return response


@pysnooper.snoop()
def resolve_path(path):
    """
    Should return two values: a callable and an iterable of
    arguments, based on the path.
    """

    path = path.strip('/').split('/')
    print(path)

    sign = path[0]
    args = path[1:]

    return sign, args

def application(environ, start_response):
    headers = [('Content-type', 'text/html')]
    try:
        path = environ.get('PATH_INFO', None)
        if path is None:
            raise NameError
        sign, args = resolve_path(path)
        body = func(sign, *args)
        print('body is ' + body)
        status = "200 OK"
    except NameError:
        status = "404 Not Found"
        body = "<h1>Not Found</h1>"
    except Exception:
        status = "500 Internal Server Error"
        body = "<h1> Internal Server Error</h1>"
    finally:
        headers.append(('Content-length', str(len(body))))
        start_response(status, headers)
        return [body.encode('utf8')]

if __name__ == '__main__':
    from wsgiref.simple_server import make_server
    srv = make_server('localhost', 8080, application)
    srv.serve_forever()
