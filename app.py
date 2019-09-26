import os
from werkzeug.wrappers import Request, Response
from werkzeug.exceptions import HTTPException, MethodNotAllowed, \
     NotImplemented, NotFound
from werkzeug.routing import Map, Rule
from werkzeug.serving import run_simple
from werkzeug.utils import redirect
from werkzeug.local import LocalStack,LocalProxy
from jinja2 import Environment,FileSystemLoader
from werkzeug.contrib.securecookie import SecureCookie


class Request(Request):
    """Encapsulates a request."""


class Response(Response):
    """Encapsulates a response."""

class _RequestContext(object):
    """请求上下文（request context）包含所有请求相关的信息。它会在请求进入时被创建，
    然后被推送到_request_ctx_stack，在请求结束时会被相应的移除。它会为提供的
    WSGI环境创建URL适配器（adapter）和请求对象。
    """
    def __init__(self, app, environ):
        self.app = app
        self.url_adapter = app.url_map.bind_to_environ(environ) # url适配器
        self.request = Request(environ)
        self.session = app.open_session(self.request)

    def __enter__(self):
        # print(self.test)
        _request_stk.push(self)

    def __exit__(self, exc_type, exc_value, tb):
        # 在调试模式（debug mode）而且有异常发生时，不要移除（pop）请求堆栈。
        # 这将允许调试器（debugger）在交互式shell中仍然可以获取请求对象。
        if tb is None or not self.app.debug:
            _request_stk.pop()


def render_template(template_name,**context):
    '''
    :param template_name:模板名字
    :param context: 传递给模板的字典参数
    :return: template
    '''
    template_path = os.path.join(os.getcwd(), 'templates')
    jinja_env = Environment(loader=FileSystemLoader(template_path), autoescape=True)
    return jinja_env.get_template(template_name).render(context)


def url_for(endpoint, **values):
    '''
    :param endpoint:url地址
    :param context: 传递给url的字典参数
    '''
    print(_request_ctx_stack.top.url_adapter.build(endpoint, values))
    # return _request_stk.top.url_adapter.build(endpoint.get_func(),values)


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
    # 如果设置了密钥，加密组件可以使用它来作为cookies或其他东西的签名。
    secret_key = None
    debug = True
    def __init__(self):
        self.url_map = Map()
        self.view = {}

    def request_context(self,environ):
        return _RequestContext(self,environ)

    def process_response(self,response):
        session = _request_stk.top.session
        if session is not None:
            self.save_session(session,response)
        return response

    def make_response(self, rv):
        # 判断rv的类型
        if isinstance(rv, Response):
            return rv
        if isinstance(rv, str):
            return Response(rv)
        if isinstance(rv, tuple):
            return Response(*rv)
        return Response.force_type(rv, request.environ)

    def wsgi_app(self,environ,start_response):
        with self.request_context(environ):
            req = Request(environ)
            response = self.dispatch_request(req)
            # print(type(response))
            if response:#如果可以找到正确的匹配项
                # response = Response(response, content_type='text/html; charset=UTF-8')
                response = self.make_response(response)
                response = self.process_response(response)
            else:#找不到，返回404NotFound
                response = Response('<h1>404 Not Found<h1>', content_type='text/html; charset=UTF-8', status=404)

            return response(environ, start_response)


    def open_session(self, request):#
        """创建或打开一个新的session，默认的实现是存储所有的session数据到一个签名的cookie中，前提是secret_key属性被设置
        :param request: Request实例
        """
        key = self.secret_key
        if key is not None:
            return SecureCookie.load_cookie(request, 'session', secret_key=key)

    def save_session(self, session, response):
        #print(response)
        if session is not None:
             session.save_cookie(response)

    def __call__(self, environ, start_response):
        return self.wsgi_app(environ, start_response)

    def dispatch_request(self, req):
        adapter = self.url_map.bind_to_environ(req.environ)
        self.url_map.bind_to_environ(req.environ)
        try:
            endpoint, value = adapter.match()
            return self.view[endpoint](req, **value)
        except HTTPException as e:
            response = e
        return response

    def add_url_rule(self,urls):
        #for url in urls:
            #self.url_map[url] = urls[url].get_func()
        for url in urls:
            self.url_map.add(Rule(url,endpoint=str(urls[url])))
            self.view[str(urls[url])] = urls[url].get_func()

    def run(self, port=8090, ip='127.0.0.1', debug=True):
        run_simple(ip, port, self, use_debugger=debug, use_reloader=True)


_request_stk = LocalStack()
current_app = LocalProxy(lambda: _request_stk.top.app)
request = LocalProxy(lambda: _request_stk.top.request)
session = LocalProxy(lambda: _request_stk.top.session)
