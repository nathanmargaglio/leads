from flask import Flask

app = Flask(__name__)
app.debug=True

# prints "var is <invalid>"
@app.route('/', subdomain="<var>", methods=['GET'])
def index(var):
        return "Hello: {}".format(var)

@app.route('/', methods=['GET'])
def index_sub():
        return "Nothin here"

if __name__ == '__main__':
    app.run(debug=True)
