import os
from PhongKhamTu import app, db
from PhongKhamTu.models import *
from flask_login import current_user
from sqlalchemy import func
from sqlalchemy.sql import extract
import hashlib

def create_user(name, username, password, yearofbith, phone, address=None, email=None, avatar=None):
    password = str(hashlib.md5(password.strip().encode('utf-8')).hexdigest())
    user = User(name=name.strip(),
                yearofbith=yearofbith.strip(),
                address=address,
                phone=phone,
                username=username.strip(),
                password=password,
                email=email.strip() if email else email,
                avatar=avatar)
    db.session.add(user)

    try:
        db.session.commit()
    except:
        return False
    else:
        return True

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