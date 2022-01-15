import os
from PhongKhamTu.models import *
from flask_login import current_user
from sqlalchemy import func
from sqlalchemy.sql import extract
import hashlib

def get_user_by_id(user_id):
    return User.query.get(user_id)

def check_login(username, password):
    if username and password:
        password = str(hashlib.md5(password.strip().encode('utf-8')).hexdigest())

        return User.query.filter(User.username.__eq__(username.strip()),
                                 User.password.__eq__(password)).first()

def check_admin(username, password, role):
    if username and password:
        password = str(hashlib.md5(password.strip().encode('utf-8')).hexdigest())

        return User.query.filter(User.username.__eq__(username.strip()),
                                 User.password.__eq__(password)).first()

def drugfrequency_stats(kwtt=None, kwdv=None, kwsld=None):
    p = db.session.query(Medicine.name, Unit.name, func.sum(MedicalCertificateDetail.quantily), func.count(MedicalCertificateDetail.medicine_id))\
    .join(Unit)\
    .join(MedicalCertificateDetail, MedicalCertificateDetail.medicine_id.__eq__(Medicine.id), isouter=True)\
    .join(MedicalCertificate, MedicalCertificate.id.__eq__(MedicalCertificateDetail.mc_id))\
    .group_by(Medicine.id, Medicine.name)

    if kwtt:
        p = p.filter(Medicine.name.contains((kwtt)))
    if kwdv:
        p = p.filter(Unit.name.contains(kwdv))
    if kwsld:
        p = p.filter(func.count(MedicalCertificateDetail.medicine_id).__eq__(kwsld))

    return p.all()

def drugfrequency_stats_month(year, kwtt=None, kwdv=None, kwsld=None):
    p = db.session.query(Medicine.name, Unit.name, func.sum(MedicalCertificateDetail.quantily),
                         func.count(MedicalCertificateDetail.medicine_id), extract('month', MedicalCertificate.healthcheck_date)) \
        .join(Unit) \
        .join(MedicalCertificateDetail, MedicalCertificateDetail.medicine_id.__eq__(Medicine.id), isouter=True) \
        .join(MedicalCertificate, MedicalCertificate.id.__eq__(MedicalCertificateDetail.mc_id)) \
        .filter(extract('year',MedicalCertificate.healthcheck_date) == year)\
        .group_by(Medicine.id, Medicine.name) \
        .group_by(extract('month', MedicalCertificate.healthcheck_date)) \
        .order_by(extract('month', MedicalCertificate.healthcheck_date))

    if kwtt:
        p = p.filter(Medicine.name.contains((kwtt)))
    if kwdv:
        p = p.filter(Unit.name.contains(kwdv))
    if kwsld:
        p = p.filter(func.count(MedicalCertificateDetail.medicine_id).__eq__(kwsld))
    return p.all()

def mclist_view(kwds = None, kwyt = None,kwbn =None, from_date = None, to_date = None):
    p = db.session.query(MedicalExaminationList.id, MedicalExaminationList.nurse_id,\
                         MedicalExaminationList.mc_date, MedicalExaminationPatient.patient_id, PATIENT.name)\
        .join(MedicalExaminationPatient, MedicalExaminationPatient.mc_id.__eq__(MedicalExaminationList.id), isouter = True)\
        .join(PATIENT, PATIENT.id.__eq__(MedicalExaminationPatient.patient_id))\
        .group_by(MedicalExaminationList.id, MedicalExaminationList.nurse_id,\
                    MedicalExaminationList.mc_date, MedicalExaminationPatient.patient_id, PATIENT.name)

    if kwds:
        p = p.filter(MedicalExaminationList.id.__eq__(kwds))
    if kwyt:
        p = p.filter(MedicalExaminationList.nurse_id.__eq__(kwyt))
    if kwbn:
        p = p.filter(PATIENT.id.__eq__(kwbn))
    if from_date:
        p = p.filter(MedicalExaminationList.mc_date.__ge__(from_date))
    if to_date:
        p = p.filter(MedicalExaminationList.mc_date.__le__(to_date))

    return p.all()

def patient_view(kwname =None, kwy = None, kwslk = None):
    p = db.session.query(PATIENT.id, PATIENT.name,PATIENT.yearofbirth, func.count(MedicalExaminationPatient.mc_id))\
                        .join(MedicalExaminationPatient, MedicalExaminationPatient.patient_id.__eq__(PATIENT.id), isouter = True)\
                        .group_by(PATIENT.id, PATIENT.name,PATIENT.yearofbirth)

    if kwname:
        p = p.filter(PATIENT.name.contains(kwname))
    if kwy:
        p = p.filter(PATIENT.yearofbirth.__eq__(kwy))
    if kwslk:
        pass
    return p.all()


def count_patient_in_day(registerdate):
    return MedicalRegister.query.filter(MedicalRegister.register_date == registerdate).count()

def add_register(name, birth, address, c_id, phone, gt):
    p = PATIENT(name = name
                , yearofbirth = birth
                , address = address,
                citizen_identification = c_id,
                gioitinh = gt,
                phone = phone,)
    db.session.add(p)
    db.session.commit()

def add_user(name, username, password,birth, **kwargs):
    password = str(hashlib.md5(password.strip().encode('utf-8')).hexdigest())
    user = User(name = name,username=username,password=password,
                yearofbirth = birth,
                email = kwargs.get('email'),
                avatar = kwargs.get('avatar'))

    db.session.add(user)
    db.session.commit()


def get_patient_by_Cid(c_id):
    p = PATIENT.query.filter(PATIENT.citizen_identification.__eq__(c_id)).first();
    return p


def add_patient_register(p_id, register_date):
    mg = MedicalRegister(patient_id = p_id, register_date = register_date)
    db.session.add(mg)
    db.session.commit()

def get_patient_by_day(registerdate):
    p = db.session.query(PATIENT.id, PATIENT.name, PATIENT.yearofbirth, PATIENT.gioitinh, PATIENT.address, MedicalRegister.register_date).\
        join(MedicalRegister, MedicalRegister.patient_id.__eq__(PATIENT.id), isouter = True).\
        group_by(PATIENT.id, PATIENT.name, PATIENT.yearofbirth, PATIENT.gioitinh, PATIENT.address, MedicalRegister.register_date)
    if registerdate:
        p = p.filter(MedicalRegister.register_date == registerdate)
    return p.all()

def add_MedicalExaminationList(note):
    if note:
        for i in note.values():
            ngay = i['ngay']
            break;

        MEL = MedicalExaminationList(user = current_user, mc_date = ngay)
        db.session.add(MEL)

        for n in note.values():
            d = MedicalExaminationPatient(medicalexaminationlist = MEL, patient_id = n['id'])
            db.session.add(d)

        db.session.commit()


def read_Medicalcertificate():
    return MedicalCertificate.query.all()

def get_mc_by_id(pk_id):
    p = db.session.query(MedicalCertificate.healthcheck_date, PATIENT.name).\
        join(PATIENT, PATIENT.id.__eq__(MedicalCertificate.patient_id),  isouter = True).\
        group_by(MedicalCertificate.healthcheck_date, PATIENT.name)
    if(pk_id):
        p = p.filter(MedicalCertificate.id.__eq__(pk_id))
    return p.all()
def get_tienkham():
    return Regulation.query.get(1)

def tienthuoc(pk_id = None):
    p = db.session.query(Medicine.price, MedicalCertificateDetail.quantily).\
        join(Medicine, Medicine.id.__eq__(MedicalCertificateDetail.medicine_id), isouter = True).\
        group_by(Medicine.price, MedicalCertificateDetail.quantily)
    if pk_id:
        p = p.filter(MedicalCertificateDetail.mc_id.__eq__(pk_id))
    return p.all()

# def total_money(pk_id):
#     tt = tienthuoc(pk_id)
#     total = 0;
#     for t in tt:
#         total += t[0] * t[1]
#     tk = get_tienkham()
#     return total + tk.value;
#
# def get_phieukham_id():
#     return db.session.query(MedicalCertificate.id).all()
#
# def tongdoanhthu(Date = None):
#     dt = 0
#     id = get_phieukham_id()
#     for i in id:
#         dt += total_money(i[0])
#     return dt
#
# def doanhthu_day(Day):
#     p = db.session.query(MedicalCertificate.healthcheck_date, tongdoanhthu(MedicalCertificate.healthcheck_date))
#     if Day:
#         p = p.filter(MedicalCertificate.healthcheck_date.__eq__(Day))
#
#     return p.all();
#
# def day():
#     return db.session.query(MedicalCertificate.healthcheck_date).all()
# def thongke():
#     p =db.session.query(MedicalCertificate.healthcheck_date, func.count(MedicalCertificate.id))\
#     .group_by(MedicalCertificate.healthcheck_date)
#     return p.all()
#
# def total_money_stats(pk_id):
#     tt = db.session.query(Medicine.price, MedicalCertificateDetail.quantily, Regulation.value).\
#         join(Medicine, Medicine.id.__eq__(MedicalCertificateDetail.medicine_id), isouter = True).\
#         group_by(Medicine.price, MedicalCertificateDetail.quantily)
#     if pk_id:
#         tt = tt.filter(MedicalCertificateDetail.mc_id.__eq__(pk_id))
#     return tt.all()

def add_bill(mc_id = None, tk = None, tt = None):
    if mc_id:
      b = Bill(user = current_user ,mc_id = mc_id, healthCheck_price = tk, drug_money = tt)
      db.session.add(b)
    db.session.commit()

def read_patient():
    return PATIENT.query.all()
def read_medicine():
    return Medicine.query.all()
def get_patient_by_id(patient_id):
    return PATIENT.query.get(patient_id)

def get_medicine_by_id(medicine_id):
    return Medicine.query.get(medicine_id)
def add_medical(patient_id = None, symptom = None, guess = None):
    if symptom:
        m = MedicalCertificate(user =current_user, patient_id = patient_id, symptom = symptom, guess = guess)
        db.session.add(m)
    db.session.commit()

def get_mc_by_doctorid_last(doctor_id):
    mc_id = None
    p = MedicalCertificate.query.filter(MedicalCertificate.doctor_id.__eq__(doctor_id))
    for i in p:
        mc_id = i.id
    return mc_id

def add_medicine(medicine_id, mc_id, quantily, user_manual):
    if medicine_id:
        mdcine = MedicalCertificateDetail(medicine_id = medicine_id, mc_id = mc_id, quantily = quantily, user_manual = user_manual)

        db.session.add(mdcine)
    db.session.commit()
