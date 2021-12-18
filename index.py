from flask import render_template, request, redirect, url_for, session
from PhongKhamTu import app, login
from flask_login import login_user, logout_user, login_required
from PhongKhamTu.models import UserRole
import utils


@app.route("/")
def home():
    return render_template('index.html')


@app.route('/admin-login', methods=['post'])
def signin_admin():
    username = request.form['username']
    password = request.form['password']

    user = utils.check_user(username=username, password=password, role=UserRole.ADMIN)
    if user:
        login_user(user=user)

    return redirect('/admin ')


@app.route('/login', methods=['get', 'post'])
def signin():
    error_msg = ""
    if request.method.__eq__('POST'):
        try:
            username = request.form['username']
            password = request.form['password']

            user = utils.check_user(username=username, password=password)
            if user:
                login_user(user=user)

                next = request.args.get('next', 'home')
                return redirect(url_for(next))
            else:
                error_msg = "Chuong trinh dang co loi! Vui long quay lai sau!"

        except Exception as ex:
            error_msg = str(ex)

    return render_template('login.html', error_msg=error_msg)


@app.route('/logout')
def signout():
    logout_user()

    return redirect(url_for('signin'))


@app.route('/logout-admin')
def signout_admin():
    logout_user()

    return redirect(url_for('signin'))


@login.user_loader
def load_user(user_id):
    return utils.get_user_by_id(user_id=user_id)


if __name__ == "__main__":
    from PhongKhamTu.admin import *

    app.run(debug=True)
