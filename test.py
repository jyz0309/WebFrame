from app import App,View,session
import json
from app import *
from werkzeug.utils import redirect

class Index(View):
    def GET(self,request,x):
        # session['hello'] = 2
        # return redirect(url_for())
        return 'helloer'
    def POST(self,request):
        print(json.dumps(request.form['color']))
        return json.dumps({'1':'hello'})

class Test(View):
    def GET(self,request):
        # print(session['hello1'])
        print(redirect('/R'))
        return redirect('/R')
    def POST(self,request):
        return json.dumps({'2':'hello'})

class R(View):
    def GET(self,request):
        return 'R'

urls = {'/<x>':Index,
        '/test':Test,
        '/R':R}

app = App()
app.secret_key = 'password'
app.add_url_rule(urls)
app.run()
