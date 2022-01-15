from flask import render_template, request, redirect, url_for, session, jsonify
from PhongKhamTu import app, login
import cloudinary.uploader
from PhongKhamTu.admin import *
from flask_login import login_user, logout_user, login_required, current_user
from PhongKhamTu.models import UserRole


@app.route("/")
def home():
    return render_template('index.html')

@app.route("/confirm")
def confirm():
    return render_template('confirm.html')

@app.route("/service")
def service():
    return render_template('service.html')

@app.route("/pay", methods=['get', 'post'])
def pay():
    mc = utils.read_Medicalcertificate()
    tienkham = utils.get_tienkham()
    pk_id = request.args.get('pk')
    pk = utils.get_mc_by_id(pk_id=pk_id)
    tienthuoc = utils.tienthuoc(pk_id=pk_id)
    sum = 0
    for t in tienthuoc:
        sum = sum + t[0] * t[1]
    if request.method == 'POST':
        utils.add_bill(mc_id = pk_id, tt = sum, tk= tienkham.value)
        pk_id = None
    return render_template('pay.html', mc = mc, pk = pk, tienkham= tienkham, sum = sum, pk_id=pk_id)

@app.route("/medical-list", methods=['get', 'post'])
def medical_list():
    err_msg = ""
    kw = request.args.get("date")
    mr = utils.get_patient_by_day(registerdate=kw)

    return render_template('medicallist.html', Medicalregister = mr, kw = kw)

@app.route("/medicalcertificate", methods=['get', 'post'])
def medicalcertificate():
    p = utils.read_patient();
    m = utils.read_medicine();

    patient_id = request.args.get('patient_id')
    patient = utils.get_patient_by_id(patient_id= patient_id)
    symptom = None
    guess = None
    mdcal = None
    medical = None
    if request.method == 'POST':
        symptom = request.form.get('symptom')
        guess = request.form.get('guess')
        if symptom and guess:
            mdcal = utils.add_medical(patient_id = patient_id, symptom= symptom, guess=guess)
        medicien_id = request.form.get('medicine_id')
        quantity = request.form.get('quantily')
        user_manual = request.form.get('user_manual')
        medical = int(utils.get_mc_by_doctorid_last(current_user.id))
        if quantity and user_manual:
            utils.add_medicine(medicine_id=medicien_id,mc_id = medical, quantily=quantity, user_manual=user_manual)
    return render_template('medicalcertificate.html', p = p, m = m, patient = patient, symptom = symptom, guess = guess, mdcal = mdcal, mc_id= medical)


@app.route('/medical-register', methods=['get', 'post'])
def medical_register():
    err_msg = ""
    count = 0
    if request.method.lower() == 'post':
            name = request.form.get('name')
            birth = int(request.form.get('birth'))
            phone = request.form.get('phone')
            address = request.form.get('address')
            gt = request.form.get('gt')
            c_id = request.form.get('c_id')
            registerdate = request.form.get('registerdate')
            count = utils.count_patient_in_day(registerdate=registerdate)
            if(count) < 30:
                if len(phone)!=10:
                    err_msg = "Số điện thoại không đúng"
                elif len(c_id) != 13:
                    err_msg = "Số CCCD không hợp lệ"
                else:
                    if utils.get_patient_by_Cid(c_id=c_id) == None:
                        utils.add_register(name=name, birth=birth, address=address, c_id=c_id, phone=phone, gt = gt)
                    p = utils.get_patient_by_Cid(c_id=c_id)
                    utils.add_patient_register(p_id = p.id, register_date=registerdate)
                    err_msg = "Đăng ký thành công"
            else:
                err_msg = "Số bệnh nhân đăng ký đã đầy"
    return render_template('medicalregister.html', err_msg=err_msg, count=count)

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
            err_msg = 'USERNAME hoặc PASSWORD không chính xác!!! '

    return render_template('login.html', err_msg=err_msg)

@app.route("/register", methods= ['get', 'post'])
def user_register():
    err_msg = ""
    if request.method.lower() == 'post':
        name = request.form.get('name')
        birth = int(request.form.get('birth'))
        username = request.form.get('username')
        password = request.form.get('password')
        email = request.form.get('email')
        avatar_path = None
        confirm = request.form.get('confirm')
        try:
            if password.strip().__eq__(confirm.strip()):
                avatar = request.files.get('avatar')
                if avatar:
                    res = cloudinary.uploader.upload(avatar)
                    avatar_path = res['secure_url']
                utils.add_user(name=name, username=username, password=password, email=email, birth= birth,avatar=avatar_path)
                return redirect(url_for('user_signin'))
            else:
                err_msg = "Mật khẩu không khớp"
        except Exception as ex:
            err_msg = "Lỗi hệ thống: " + str(ex)
    return render_template('register.html', err_msg= err_msg)
@app.route('/admin-login', methods=['post', 'get'])
def signin_admin():
    username = request.form['username']
    password = request.form['password']
    error = ""
    user = utils.check_admin(username=username, password=password, role=UserRole.ADMIN)
    if user:
        login_user(user=user)
        error = 'Vui lòng đăng nhập bằng tài khoản ADMIN!!! '
    else:
        error = 'USERNAME hoặc PASSWORD không chính xác!!! '
    return redirect('/admin')



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

@app.route('/api/add_to_note', methods = ['post'])
def add_to_note():

    try:
        data = request.json

        id = str(data.get('id'))
        name = data.get('name')
        gioitinh = data.get('gioitinh')
        yearofbirth = data.get('yearofbirth')
        address = data.get('address')
        ngay = data.get('ngay')
        note = session.get('note')
        if not note:
            note = {}
        if id in note:
            pass
        else:
            note[id] = {
                'id': id,
                'name': name,
                'gioitinh' : gioitinh,
                'yearofbirth' : yearofbirth,
                'address' : address,
                'ngay' : ngay
             }
            session['note'] = note
            return jsonify({
                'code': 200
            })
    except:
        return jsonify({'code': 404})

    return jsonify({'code': 200})

@app.route('/api/save', methods=['post'])
def save():
    try:
        utils.add_MedicalExaminationList(session.get('note'))
        del session['note']
    except:
        return jsonify({'code': 400})

    return jsonify({'code': 200})
@app.route('/api/delete-note/<p_id>', methods=['delete'])
def delete_note(p_id):
    note = session.get('note')
    err_msg = ''
    if note:
        if p_id in note:
            del note[p_id]
            session['note'] = note
            return jsonify({
                'code': 200
            })
    else:
        err_msg = 'Chua co danh sach!'

    return jsonify({
        'code': 404,
        'err_msg': err_msg
    })

if __name__ == "__main__":

    app.run(debug=True)