
from app import App,View
import json
class Index(View):
    def GET(self,request):
        return "hello world"
    def POST(self,request):
        # print(json.dumps(request.form['color']))
        return json.dumps({'1':'hello'})

class Test(View):
    def GET(self,request):
        return "test"
    def DELETE(self,request):
        return json.dumps({'2':'hello'})
urls = {'/':Index,
        '/test':Test}



app = App()
app.add_url_rule(urls)
app.run()
