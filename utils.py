from PhongKhamTu import app, db
from PhongKhamTu.model import User, UserRole, PATIENT, MedicalExaminationPatient, MedicalExaminationList, MedicalRegister, Medicine, MedicalCertificate,\
            MedicalCertificateDetail, Unit,Bill
from flask_login import current_user
from sqlalchemy import func
import hashlib

def DanhsachView(kwds = None, kwyt = None,kwbn =None, from_date = None, to_date = None):
    p = db.session.query(MedicalExaminationList.id, MedicalExaminationList.nurse_id,\
                         MedicalExaminationList.mc_date, MedicalExaminationPatient.patient_id, PATIENT.name)\
        .join(MedicalExaminationPatient, MedicalExaminationPatient.mc_id.__eq__(MedicalExaminationList.id), isouter = True)\
        .join(PATIENT, PATIENT.id.__eq__(MedicalExaminationPatient.patient_id))

    if kwds:
        p = p.filter(MedicalExaminationList.id.__eq__(kwds))
    if kwyt:
        p = p.filter(MedicalExaminationList.nurse_id.__eq__(kwyt))
    if kwbn:
        p = p.filter(PATIENT.name.contains(kwbn))
    if from_date:
        p = p.filter(MedicalExaminationList.mc_date.__ge__(from_date))
    if to_date:
        p = p.filter(MedicalExaminationList.mc_date.__le__(to_date))

    return p.group_by(MedicalExaminationList.id, MedicalExaminationList.nurse_id,\
                    MedicalExaminationList.mc_date, MedicalExaminationPatient.patient_id, PATIENT.name).all()

def BenhnhanView(kwname =None, kwy = None, kwslk = None):
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
