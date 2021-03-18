from flask import Flask
from flask import Flask, request, abort, render_template
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
import psycopg2
import json


app = Flask(__name__, template_folder='./templates/')
limiter = Limiter(
    app,
    key_func=get_remote_address,
    default_limits=["1/second"]
)

class sql:
    host =     r""
    database = r""
    user =     r""
    password = r""
    uri =      r""


conn = psycopg2.connect(
    host=sql.host,
    database=sql.database,
    user=sql.user,
    password=sql.password)

ip_ban_list = []
keys = {}
x = json.loads(open("keys.json","r").read())
for i in x:
    keys[i] = x[i]
print(keys)

@app.before_request
def block_method():
    ip = request.environ.get('REMOTE_ADDR')
    if ip in ip_ban_list:
        abort(403)

@app.route('/')
@limiter.limit("1/second")
def index():
    return render_template('index.html')

@app.route('/api/search')
@limiter.limit("1/second")
def search():
    key = request.args.get('apikey')
    print(key)
    try:
        perms = keys[key]
        print(perms)
    except:
        abort(403)
    else:
        if "read" in perms:
            pass
        else:
            abort(403)
    wallet = request.args.get('wallet')
    if wallet.startswith("ban_") == False:
        return "invalid banano address"
    if wallet.replace(" ","") != wallet:
        return "invalid banano address"
    cursor = conn.cursor()
    sql = f"""SELECT * FROM banned WHERE uname LIKE '{str(wallet)}'"""
    cursor.execute(sql)
    d = cursor.fetchall()
    x = []
    for i in d:
        p = {}
        p["type"] = i[1]
        p["reason"] = i[2]
        x.append(p)
    return json.dumps(x)

# ban_1aws637mb3qnuf9j8swzufq3nj3fttuzkixbd817nmmhyms6a6kt1zyptq87
# ban_1aws637mb3qnuf9j8swzufq3nj3fttuzkixbd817nmmhyms6a6kt1zyptq87