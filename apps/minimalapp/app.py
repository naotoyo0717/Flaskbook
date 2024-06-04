import io,sys
from email_validator import validate_email, EmailNotValidError
import os
from flask_mail import Mail, Message #Flask_mail拡張機能からMailクラスをインポートしている

from flask import(
    Flask,
    render_template,
    request,
    url_for,
    redirect,
    flash,
)

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
app = Flask(__name__) #appというFlaskクラスをインスタンス化する
app.config['SECRET_KEY'] = '2AZSMss3p5QPbcY2hBsJ' #SECRET_KEYを追加、ユーザーのセッション情報を暗号化する

# app.config['MAIL_SERVER'] = os.environ.get('MAIL_SERVER') #メールを送信するためのサーバのアドレス
# app.config['MAIL_PORT'] = os.environ.get('MAIL_PORT') #メールを送信するためのポート番号
# app.config['MAIL_USE_TLS'] = os.environ.get('MAIL_USE_TLS') #セキュアな通信を行うかどうかを示すフラグ。Trueか１であればTLSを使用する。
# app.config['MAIL_USERNAME'] = os.environ.get('MAIL_USERNAME') #メールサーバーにアクセスするための認証情報
# app.config['MAIL_PASSWORD'] = os.environ.get('MAIL_PASSWORD')
# app.config['MAIL_DEFAULT_SENDER'] = os.environ.get('MAIL_DEFAULT_SENDER') #デフォルトのメールサーバーのアドレス。メール送信時にサーバが指定されない場合に使用される。
# #メール送信機能を設定している。具体的には、メール送信に必要な情報をアプリケーションの設定に追加し、それを使ってメールを送信する準備をしている。
app.config['SECRET_KEY'] = '2AZSMss3p5QPbcY2hBsJ' #SECRET_KEYを追加、ユーザーのセッション情報を暗号化する
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] =587
app.config['MAIL_USE_TLS'] = True #セキュアな通信を行うかどうかを示すフラグ。Trueか１であればTLSを使用する。
app.config['MAIL_USE_SSL'] = False
app.config['MAIL_USERNAME'] ='naotech717@gmail.com'
app.config['MAIL_PASSWORD'] = 'eldfncwzilslqyhq'
app.config['MAIL_DEFAULT_SENDER'] = 'Flaskbook <naotech717@gmail.com>'

mail = Mail(app) #最後にFlaskアプリケーションにメール機能を追加している。これでメール送信準備完了。

@app.route('/')
def index():
    return 'Hello, Flaskbook!'

#@app.route('/hello/<name>', #<>で変数を指定
#    methods = ['GET','POST'], #HTTPメソッド名を指定
#    endpoint = 'hello-endpoint') #エンドポイントに名前を付ける。Flask内部の設定値として使われる
#def hello(name):
#    return f'Hello, {name}!'

#@app.route('/name/<name>')
#def show_name(name):
#   return render_template('index.html', name = name) #jinja2を用いてindex.htmlに引数nameを与えて出力

@app.route('/contact') #「問い合わせフォーム」画面
def contact():
    return render_template('contact.html')

@app.route('/contact/complete', methods = ['GET','POST']) #「問い合わせ完了」画面
def contact_complete():
    if request.method == 'POST': #リクエストされたメソッドをチェックする
        username = request.form['username']
        email = request.form['email']
        description = request.form['description']

        is_valid = True

        if not username:
            flash('ユーザー名は必須です')
            is_valid = False

        if not email:
            flash('メールアドレスは必須です')
            is_valid = False

        try:
            validate_email(email) #emailがメールアドレスの形式かどうかをチェックする
        except EmailNotValidError: #形式が不正である場合の処理
            flash('メールアドレスの形式で入力してください')
            is_valid = False

        if not description:
            flash('問い合わせ内容は必須です')
            is_valid = False

        if not is_valid:
            return redirect(url_for('contact')) #is_validフラグがFalseの場合、contactエンドポイントにリダイレクト。
        
        #メールを送る
        send_email(
             email,
             '問い合わせありがとうございました。',
             'contact_mail',
             username=username,
             description=description,
        )#メール送信関数を呼び出す。

        flash('問い合わせありがとうございました。') #問い合わせ完了エンドポイントにリダイレクトする
        return redirect(url_for('contact_complete')) #(POSTの場合)問い合わせが正常に完了した場合、成功メッセージを表示し、再び「contact_complete」エンドポイントにリダイレクト
    
    return render_template('contact_complete.html') #GETの場合は「問い合わせ完了」画面（contact_complete.html）を返す。

# def send_email(to, subject, template, **kwargs):
#     '''メールを送信する関数'''
#     try:
#         msg = Message(subject, recipients=[to])
#         msg.body = 'hello'
#         #msg.html = render_template(template + '.html', **kwargs)
#         mail.send(msg)
#     except Exception as e:
#         print(f'Error sending email: {e}')
#         raise

def send_email(to, subject, template, **kwargs):
    '''メールを送信する関数'''
    try:
        msg = Message(
            subject,
            recipients=[to],
            body=template,  # Use the template as the email body
            charset = 'utf-8'
            )     
        msg.charset = 'utf-8'
        mail.send(msg)
    except Exception as e:
        print(f'Error sending email: {e}')
        raise
#with app.test_request_context(): #url_forを出力する準備。HTTPを使用しない状況で、リクエストコンテキストが必要な操作を行うために使用される。
    #print(url_for('index')) #/
    #print(url_for('hello-endpoint', name='world')) #hello/world
    #print(url_for('show_name', name='ichiro', page='1')) #/name/ichiro?page=ichiro
    #エンドポイントに対応するRuleが変わったとしても、HTMLファイルやViewに記述しているURLを変更する必要がなくなる


#if __name__ == '__main__': #Pythonスクリプトが直接実行されている場合のみ、以下のコードを実行する
#    app.debug = True #デバッグモードをonにする
#    app.run() #Flaskアプリケーションをローカルサーバで実行する


print(app.config['MAIL_SERVER'])
print(app.config['MAIL_PORT'])
print(app.config['MAIL_USE_TLS'])
print(app.config['MAIL_USERNAME'])
print(app.config['MAIL_PASSWORD'])
print(app.config['MAIL_DEFAULT_SENDER'])
