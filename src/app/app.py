from flask import Flask, render_template, request, session, redirect  # 各種Flaskモジュール
import datetime  # 天気アプリ現在時刻
from datetime import timedelta  # ログイン時間制限用
import mysql.connector  # MySQLとFlaskのコネクター
import re  # 文字数制限
import requests  # weather情報取得


# Flaskのインスタンス生成
app = Flask(__name__)

# secret_keyの準備
app.config['SECRET_KEY'] = 'fh7342ttl284c'

# security code
SECURE = '456545'


# MySQLとFlaskのコネクタ設定
def cdb():
    db = mysql.connector.connect(
        user='root',
        password='password',  # MySQL root password
        host='database',
        database='app'
    )
    return db


# パスワードなどの文字数制限
def register_interface(type, words, limit_words):
    if type == "name":
        if len(words) < limit_words:
            return False
        else:
            return True
    elif type == "password":  # passwordは指定文字数以上か
        if len(words) < limit_words:
            return False
    is_match = [0, 0, 0]  # 大文字、小文字、数字なら各要素に1をセット
    for c in words:
        if re.match(r'[A-Z]', c):
            is_match[0] = 1
        elif re.match(r'[a-z]', c):
            is_match[1] = 1
        elif re.match(r'[0-9]', c):
            is_match[2] = 1
        else:
            return False   # それ以外はだめ
    return sum(is_match) == 3  # すべてを含む


# ホーム画面に遷移
@app.route('/')
def top():
    return render_template("index.html")


# ログイン時の処理
@app.route('/login/', methods=['GET', 'POST'])
def login():
    msg = ""
    times_now = 0  # ログイン回数格納 

    # ログイン情報は安全か、フォームに情報は記入されているか(情報入力後)
    if request.method == 'POST' \
        and 'email' in request.form \
        and 'password' in request.form:
        
        # ログイン情報をPOSTで受け取る
        email = request.form['email']
        password = request.form['password']
        
        # ログイン情報は、データベースの情報と一致するか確認
        cnx = cdb()
        cursor = cnx.cursor(buffered=True)  # 一件ずつデータを取る仕組みの構築
        cursor.execute('SELECT * FROM Profiles WHERE email=%s AND password=%s', 
                        (email, password,))  # メールアドレスとパスワードは一致しているか、過去に登録したことがあるか
        account = cursor.fetchone()  # 実際にrecord取得(一件ずつ)してタプル化

        # ログイン回数更新
        times_now = account[5]
        times_now += 1
        cursor.execute("UPDATE Profiles set times=%s where email=%s AND password=%s", (times_now, email, password,))
        cnx.commit()
        
        # 本人確認が正しいときの処理
        if account:
            app.permanent_session_lifetime = timedelta(minutes=3)  # 3分ログイン状態保持  
            session.permanent = True # 仮にブラウザを閉じても状態保持
            session.modified = True # session変更をブラウザに登録しない
            return redirect('/if_contents')  # どの紹介ページを選択したかで表示変更
        else:
            msg = 'incorrect username or password'  # エラー表示
            return render_template("login.html", msg=msg)  # 再度ログイン

    else: # ログイン画面を開いたばかりで、何も入力していない(情報入力前)
        if 'refrigerator' in request.form:
            session['contents'] = 'refrigerator'  # 冷蔵庫アプリの選択保持
        elif 'company' in request.form:
            session['contents'] = 'company'  # プライオールサイトの選択保持
        elif 'weather' in request.form:
            session['contents'] = 'weather'  # 天気アプリの選択保持
        elif 'management' in request.form:
            session['contents'] = 'management'  # 管理者ページの選択保持
        else:
            session['contents'] = None  # 何の選択も保持しない

        if session['contents'] == 'management':
            return redirect('/login_management')  # ログインページ遷移(management)
        else:
            return render_template("login.html")  # ログインページ遷移(normal)


# 管理者用ログイン処理
@app.route('/login_management', methods=['GET', 'POST'])
def login_management():

    msg = ""
    times_now = 0  # ログイン回数格納 

    # ログイン情報は安全か、フォームに情報は記入されているか(情報入力後)
    if request.method == 'POST' \
        and 'email' in request.form \
        and 'password' in request.form \
        and 'security' in request.form:
        
        # ログイン情報をPOSTで受け取る
        email = request.form['email']
        password = request.form['password']
        security = request.form['security']

        # セキュリティコードを確認
        if security != SECURE:
            msg = 'security code is incorrect !'  # エラー表示
            return render_template("login.html", msg=msg)  # 再度ログイン
        
        # ログイン情報は、データベースの情報と一致するか確認
        cnx = cdb()
        cursor = cnx.cursor(buffered=True)  # 一件ずつデータを取る仕組みの構築
        cursor.execute('SELECT * FROM Profiles WHERE email=%s AND password=%s', 
                        (email, password,))  # メールアドレスとパスワードは一致しているか、過去に登録したことがあるか
        account = cursor.fetchone()  # 実際にrecord取得(一件ずつ)してタプル化

        # 本人確認が正しいときの処理
        if account:
            app.permanent_session_lifetime = timedelta(minutes=3)  # 3分ログイン状態保持  
            session.permanent = True # 仮にブラウザを閉じても状態保持
            session.modified = True # session変更をブラウザに登録しない

            # ログイン回数更新
            times_now = account[5]
            times_now += 1
            cursor.execute("UPDATE Profiles set times=%s where email=%s AND password=%s", (times_now, email, password,))
            cnx.commit()
        
            return redirect('/if_contents')  # どの紹介ページを選択したかで表示変更
        else:
            msg = 'incorrect username or password'  # エラー表示
            return render_template("login_management.html", msg=msg)  # 再度ログイン

    else: # ログイン画面を開いたばかりで、何も入力していない(情報入力前)
        return render_template("login_management.html")  # ログインページ遷移


# 登録時の処理
@app.route('/register', methods=['GET', 'POST'])
def register():
    msg = ''

    # 登録情報は安全か、フォームに情報は記入されているか(記入後)
    if request.method == 'POST' \
        and 'email' in request.form \
        and 'password' in request.form \
        and 'tel' in request.form \
        and 'name' in request.form:

        # フォーム入力情報取得
        email = request.form['email']
        password = request.form['password']
        tel = request.form['tel']
        name = request.form['name']

        # 文字数制限()
        if register_interface("password", password, 8) == False:
            msg = 'A-Z, a-z, 0-9をそれぞれ１字以上を含め、合計8文字以上で入力してください'
            return render_template('register.html', msg=msg)
        if register_interface("name", name, 1) == False:
            msg = 'ネームは1文字以上で入力してください'
            return render_template('register.html', msg=msg)

        # 一度登録しているかどうか確認
        db = cdb()
        cursor = db.cursor(buffered=True)
        cursor.execute('SELECT * FROM Profiles WHERE email=%s AND password=%s AND tel=%s AND name=%s',
                        (email, password, tel, name))
        account = cursor.fetchone()

        # 元々登録されていれば、ログイン画面に遷移
        if account:
            return render_template('login.html')

        # 初めての登録の場合、以下実行
        else:
            cursor = db.cursor(buffered=True)
            cursor.execute("INSERT INTO Profiles (email, password, tel, name) values (%s, %s, %s, %s)",
                        (email, password, tel, name,))
            db.commit() # データベース操作(挿入)を確定させる

            # 新しく挿入したデータを引っ張り出す
            cursor = db.cursor(buffered=True)
            cursor.execute('SELECT * FROM Profiles WHERE email=%s AND password=%s AND tel=%s AND name=%s',
                        (email, password, tel, name))
            account_new = cursor.fetchone()

            app.permanent_session_lifetime = timedelta(minutes=3)
            session.permanent = True
            session.modified = True # session変更をブラウザに登録しない

            return redirect('/if_contents')  # 押されたボタンに対して画面変える
    else: # まだ登録を済ませていない(登録前)
        return render_template('register.html')


# 押されたボタンに対して画面変える処理
@app.route('/if_contents')
def if_contents():
    if session['contents'] == 'refrigerator':
        return render_template('refrigerator.html')  # RMA
    elif session['contents'] == 'company':
        return render_template('company.html')  # プライオール
    elif session['contents'] == 'weather':
        return redirect('/weather')  # 天気アプリ
    elif session['contents'] == 'management':
        return redirect('/management')  # 管理者用サイト
    else:
        session['contents'] = None  # それ以外は何も入れない
        return redirect('/')


# 天気アプリの処理
@app.route('/weather')
def weather():

    # 時刻を取得
    date_info = datetime.datetime.now()

    # 北九州の天気(最高気温・最低気温・天気)
    api = "https://api.openweathermap.org/data/2.5/weather?q=Kitakyushu&appid=abd789da117ee9abcd67a7bd5f2299bb"  # OpenWeatherApi
    json_data = requests.get(api).json() # json取得
    weather = json_data["weather"][0]["main"] # 以下、各情報取得
    max_temp = int(json_data['main']['temp_max'] - 273.15)
    min_temp = int(json_data['main']['temp_min'] - 273.15)

    # 北九州の天気(降水確率)
    url = 'https://www.jma.go.jp/bosai/forecast/data/forecast/400000.json'
    json_data2 = requests.get(url).json()
    rain = json_data2[0]['timeSeries'][1]['areas'][1]['pops'][0]

    return render_template("weather.html", weather=weather, max_temp=max_temp, min_temp=min_temp, 
            rain=rain, date_info=date_info)


# 管理画面用の処理
@app.route('/management')
def management():

    # データベースから、テーブル全ての情報を取り出す
    db = cdb()
    cursor = db.cursor(buffered=True)
    alldata = cursor.execute('SELECT * FROM Profiles')
    alldata = cursor.fetchall()

    return render_template("management.html", alldata=alldata)


# Flask実行
if __name__ == '__main__':
    app.run('0.0.0.0', debug=True)