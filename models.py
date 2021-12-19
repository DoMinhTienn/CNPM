from PhongKhamTu import db
from sqlalchemy import Column, Integer, String, Float, Enum, DateTime, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from flask_login import UserMixin
from enum import Enum as UserEnum


class BaseModel(db.Model):
    __abstract__ = True

    id = Column(Integer, primary_key=True, autoincrement=True)


class UserRole(UserEnum):
    PATIENT = 1
    DOCTOR = 2
    NURSE = 3
    ADMIN = 4


class User(BaseModel, UserMixin):
    __tablename__ = 'user'
    name = Column(String(50), nullable=False)
    yearofbirth = Column(DateTime)
    address = Column(String(100))
    phone = Column(Integer)
    username = Column(String(50), nullable=False, unique=True)
    password = Column(String(50), nullable=False)
    avatar = Column(String(100))
    email = Column(String(50))
    joined_date = Column(DateTime, default=datetime.now())
    user_role = Column(Enum(UserRole), default=UserRole.PATIENT)
    def __str__(self):
        return self.name


class PATIENT(BaseModel):
    __tablename__ = 'patient'
    name = Column(String(50), nullable=False)
    yearofbirth = Column(Integer, nullable=False)
    address = Column(String(100))
    patientMEP = relationship('MedicalExaminationPatient', backref='patient', lazy=True)
    patientMC = relationship('MedicalCertificate', backref='patient', lazy=True)
    def __str__(self):
        return self.name


# QuyDinh
class Regulation(BaseModel):
    __tablename__ = 'regulations'
    name = Column(String(50), nullable=False)
    value = Column(Integer)
    def __str__(self):
        return self.name


# DonVi
class Unit(BaseModel):
    __tablename__ = 'unit'
    name = Column(String(50), nullable=False)
    units = relationship('Medicine', backref='unit', lazy=True)

    def __str__(self):
        return self.name


# Thuoc
class Medicine(BaseModel):
    __tablename__ = 'medicine'
    name = Column(String(50), nullable=False)
    unit_id = Column(Integer, ForeignKey(Unit.id), nullable=False)
    price = Column(Float, default=0)
    mc_details = relationship('MedicalCertificateDetail', backref='medicine', lazy=True)

    def __str__(self):
        return self.name

# Phieu Kham
class MedicalCertificate(BaseModel):
    __tablename__ = 'medicalcertificate'
    doctor_id = Column(Integer)
    patient_id = Column(Integer, ForeignKey(PATIENT.id), nullable=False)
    healthcheck_date = Column(DateTime, default=datetime.today())
    symptom = Column(String(100))
    guess = Column(String(100))
    details = relationship('MedicalCertificateDetail', backref='medicalcertificate', lazy=True)
    bills = relationship('Bill', backref='medicalcertificate', lazy=True)


# PhieuKham_Thuoc
class MedicalCertificateDetail(db.Model):
    __tablename__ = 'medicalcertìicatedetail'
    medicine_id = Column(Integer, ForeignKey(Medicine.id), nullable=False, primary_key=True)
    mc_id = Column(Integer, ForeignKey(MedicalCertificate.id), nullable=False, primary_key=True)
    quantily = Column(Float, default=0)

# HoaDon
class Bill(BaseModel):
    __tablename__ = 'bill'
    mc_id = Column(Integer, ForeignKey(MedicalCertificate.id), nullable=False)
    nurse_id = Column(Integer)
    healthCheck_price = Column(Float, nullable= False)


# DanhSachKhamBenh
class MedicalExaminationList(BaseModel):
    __tablename__ = 'medicalexaminationlist'
    nurse_id = Column(Integer, nullable=False)
    mc_date = Column(DateTime, default=datetime.today())
    em = relationship('MedicalExaminationPatient', backref='medicalexaminationlist', lazy=True)


# Dang Ky Kham Benh
class MedicalRegister(BaseModel):
    __tablename__ = 'medicalregister'
    name = Column(String(50), nullable=False)
    yearofbirth = Column(Integer, nullable=False)
    address = Column(String(100))
    register_date = Column(DateTime, default=datetime.now(), nullable=False)

# Benh Nhan Kham Benh
class MedicalExaminationPatient(db.Model):
    __tablename__ = 'medicalexaminationpatient'
    mc_id = Column(Integer, ForeignKey(MedicalExaminationList.id), nullable=False, primary_key=True)
    patient_id = Column(Integer, ForeignKey(PATIENT.id), nullable=False, primary_key=True)


if __name__ == '__main__':
    db.create_all()

    # a = [
    #         {
    #             "name": "Nguyễn Văn Trường",
    #             "yearofbirth": "2000-01-05 05:20:00",
    #             "address": "TP Ho Chi Minh",
    #             "phone": 666888,
    #             "username": "admin",
    #             "password":"0CC175B9C0F1B6A831C399E269772661",
    #             "user_role": "ADMIN"
    #
    #         }]
    # for u in a:
    #     Us = User(name=u["name"], yearofbirth=u["yearofbirth"], address=u["address"], username=u['username'], password=u['password'], user_role=u['user_role'])
    #     db.session.add(Us)
    #
    #     db.session.commit()
