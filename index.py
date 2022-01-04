from flask import render_template, request, redirect, url_for, session
from PhongKhamTu import app, login
import cloudinary.uploader
from flask_login import login_user, logout_user, login_required
from PhongKhamTu.models import UserRole
import utils


@app.route("/")
def home():
    return render_template('index.html')

@app.route("/pay")
def pay():
    return render_template('pay.html')

@app.route("/medical-list")
def medical_list():
    return render_template('medicallist.html')

@app.route("/medicalcertificate")
def medicalcertificate():
    return render_template('medicalcertificate.html')


@app.route('/medical-register')
def medical_register():
    return render_template('medicalregister.html')

@app.route('/user-login', methods=['get', 'post'])
def user_signin():
    err_msg = ''
    if request.method.__eq__('POST'):
        username = request.form.get('username')
        password = request.form.get('password')

        user = utils.check_login(username=username, password=password)
        if user:
            login_user(user=user)

            return redirect(url_for(request.args.get('next', 'home')))
        else:
            err_msg = 'Username hoac password KHONG chinh xac!!!'

    return render_template('login.html', err_msg=err_msg)

@app.route("/register", methods=['get', 'post'])
def register():
    error_msg = ""
    if request.method.__eq__('POST'):
        try:
            # name = request.form['name']
            # username = request.form['username']
            password = request.form['password']
            confirm = request.form['confirm']
            # email = request.form.get('email')

            if password.__eq__(confirm):
                data = request.form.copy()
                del data['confirm']

                file = request.files['avatar']
                if file:
                    res = cloudinary.uploader.upload(file)
                    data['avatar'] = res['secure_url']

                if utils.create_user(**data):
                    redirect(url_for('signin'))
                else:
                    error_msg = "Chuong trinh dang co loi! Vui long quay lai sau!"
            else:
                error_msg = "Mat khau KHONG khop!"
        except Exception as ex:
            error_msg = str(ex)

    return render_template('register.html', error_msg=error_msg)

@app.route('/admin-login', methods=['post'])
def signin_admin():
    username = request.form['username']
    password = request.form['password']

    user = utils.check_admin(username=username, password=password, role=UserRole.ADMIN)
    if user:
        login_user(user=user)

    return redirect('/admin ')



@app.route('/logout')
def signout():
    logout_user()

    return redirect(url_for('user_signin'))


@app.route('/logout-admin')
def signout_admin():
    logout_user()

    return redirect('/admin')


@login.user_loader
def load_user(user_id):
    return utils.get_user_by_id(user_id=user_id)


if __name__ == "__main__":
    from PhongKhamTu.admin import *

    app.run(debug=True)
