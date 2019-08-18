import os
from werkzeug.wrappers import BaseRequest, BaseResponse
from werkzeug.exceptions import HTTPException, MethodNotAllowed, \
     NotImplemented, NotFound
from werkzeug.serving import run_simple
from jinja2 import Environment,FileSystemLoader

def render_template(template_name,**context):
    '''
    :param template_name:模板名字
    :param context: 传递给模板的字典参数
    :return: template
    '''
    template_path = os.path.join(os.getcwd(), 'templates')
    jinja_env = Environment(loader=FileSystemLoader(template_path), autoescape=True)
    return jinja_env.get_template(template_name).render(context)


class Request(BaseRequest):
    """Encapsulates a request."""


class Response(BaseResponse):
    """Encapsulates a response."""


class View(object):
    """Baseclass for our views."""
    def __init__(self):
        self.methods_meta = {
            'GET': self.GET,
            'POST': self.POST,
            'PUT': self.PUT,
            'DELETE': self.DELETE,
        }
    def GET(self):
        raise MethodNotAllowed()
    POST = DELETE = PUT = GET

    def HEAD(self):
        return self.GET()
    def dispatch_request(self, request, *args, **options):
        if request.method in self.methods_meta:
            return self.methods_meta[request.method](request, *args, **options)
        else:
            return '<h1>Unsupported require method</h1>'

    @classmethod
    def get_func(cls):
        def func(*args, **kwargs):
            obj = func.view_class()
            return obj.dispatch_request(*args, **kwargs)
        func.view_class = cls
        return func

class App(object):
    def __init__(self):
        self.url_map = {}
        # self.view_functions = {}

    def wsgi_app(self,environ,start_response):
        req = Request(environ)
        response = self.dispatch_request(req)
        if response:#如果可以找到正确的匹配项
            response = Response(response, content_type='text/html; charset=UTF-8')
        else:#找不到，返回404NotFound
            response = Response('<h1>404 Not Found<h1>', content_type='text/html; charset=UTF-8', status=404)
        return response(environ, start_response)

    def __call__(self, environ, start_response):
        return self.wsgi_app(environ, start_response)

    def dispatch_request(self, req):
        try:
            url = req.path
            view = self.url_map.get(url,None)
            if view:
                response = view(req)
            else:
                response = None
        except HTTPException as e:
            response = e
        return response
    def add_url_rule(self,urls):
         for url in urls:
             self.url_map[url] = urls[url].get_func()
             # self.url_map[url['url']] = url['func'].get_func()


    def run(self, port=8090, ip='127.0.0.1', debug=True):
        run_simple(ip, port, self, use_debugger=debug, use_reloader=True)
