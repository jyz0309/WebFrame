from app import App,View,session
import json


class Index(View):
    def GET(self,request,x):
        #session['hello'] = 2
        return x
    def POST(self,request):
        print(json.dumps(request.form['color']))
        return json.dumps({'1':'hello'})

class Test(View):
    def GET(self,request):
        # print(session['hello1'])
        return 'test'
    def POST(self,request):
        return json.dumps({'2':'hello'})


urls = {'/<x>':Index, #动态路由
        '/test':Test}

app = App()
app.secret_key = 'password'
app.add_url_rule(urls)
app.run()
