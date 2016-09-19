from flask import Flask

app = Flask(__name__)
app.debug=True
app.config['SERVER_NAME'] = 'localserver:5000'


# prints "var is <invalid>"
@app.route('/', subdomain="<var>", methods=['GET'])
def index(var):
        print "var is %s" % var
        return "Hello World %s" % var

@app.route('/', methods=['GET'])
def index_sub():
        return "Nothin here"

# This 404s
@app.route('/login/', methods=['GET'])
def login():
    return "Login Here!"

if __name__ == '__main__':
    app.run(debug=True)
