from flask import Flask

app = Flask(__name__)
app.debug = True
app.config['SERVER_NAME'] = 'localserver:5000'

@app.route('/', subdomain="<api>", methods=['GET'])
def sub_index(api):
    return "hello {}".format(api)

@app.route("/",methods=['GET','POST'])
def index():
    return "Index..."

if __name__ == '__main__':
    app.run(debug=True)
