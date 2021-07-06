from flask import Flask
from flask import request, render_template, url_for, redirect, flash, jsonify
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
import connectSql

app = Flask(__name__)
app.config['SECRET_KEY'] = 'myKey'

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'
login_manager.login_message = '請先登入'

users = {'Me': {'password': 'myself'}}

class User(UserMixin):
    pass

@login_manager.user_loader
def user_loader(account):
    print("account: " + account)
    if account == None:
        return

    if connectSql.checkUser(account) == False:
        return

    user = User()
    user.id = account
    return user

@login_manager.request_loader
def request_loader(request):
    account = request.form.get('account')
    if account == None:
        return

    if connectSql.loginUser(request.form['account'], request.form['password']):
        return

    user = User()
    user.id = account
    return user

@app.route("/")
@login_required
def home():
    return render_template("index.html")

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template("login.html")
    
    
    account = request.form['account']
    print(account)
    if connectSql.loginUser(request.form['account'], request.form['password']):
        user = User()
        user.id = account
        login_user(user)
        flash(f'{account}！登入成功')
        return redirect(url_for('home'))

    flash('登入失敗了...')
    return render_template('login.html')

@app.route('/regist', methods=['POST'])
def regist():
    if connectSql.registUser(request.form['account'], request.form['password']):
        return render_template('regist_success.html')
    else:
        return render_template('regist_faild.html')

@app.route('/logout')
def logout():
    account = current_user.get_id()
    logout_user()
    return render_template('login.html')

@app.route('/search', methods=["get"])
def search():
    from_date = request.args.get('from_date')
    from_time = request.args.get('from_time')
    from_usec = request.args.get('from_usec')
    to_date = request.args.get('to_date')
    to_time = request.args.get('to_time')
    to_usec = request.args.get('to_usec')
    source_ip = request.args.get('sourceip')
    fqdn = request.args.get('fqdn')

    return jsonify(connectSql.searchBetweenTime(from_date, from_time, from_usec, to_date, to_time, to_usec, source_ip, fqdn))
    # if to_date == "" and to_time == "" and to_usec == "":
    #     return jsonify(connectSql.searchTime(from_date, from_time, from_usec, source_ip, fqdn))

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)

    