from PhongKhamTu import db, app
from PhongKhamTu.models import *
from flask_admin.contrib.sqla import ModelView
from flask_admin import BaseView, expose, Admin
from flask_login import current_user, logout_user
from flask import redirect, request
from flask_admin import AdminIndexView
from datetime import datetime
import utils

class AuthenticatedModelView(ModelView):
    def is_accessible(self):
        return current_user.is_authenticated and current_user.user_role == UserRole.ADMIN

class MedicineView(AuthenticatedModelView):
    column_display_pk = True
    can_view_details = True
    can_export = True
    column_labels = {'name': 'Tên thuốc', 'price': 'Gía tiền', 'unit_id': 'Đơn vị'}
    column_filters = ['name', 'price']
    column_searchable_list = ['name']
    column_exclude_list = ['id']

class MedicalCertificateView(AuthenticatedModelView):
    column_display_pk = True
    can_view_details = True
    can_export = True
    column_labels = {'doctor_id': 'Mã bác sĩ', 'healthcheck_date': 'Ngày khám', 'symptom': 'Triệu chứng', 'guess': 'Dự đoán bệnh', 'patient_id': 'Bệnh nhân'}
    column_filters = ['doctor_id', 'healthcheck_date', 'patient_id']
    column_searchable_list = ['id']
    column_exclude_list = ['id', 'details', 'bills']

class PATIENTView(AuthenticatedModelView):
    column_display_pk = True
    can_view_details = True
    can_export = True
    column_labels = {'id': 'ma BN','name': 'Tên Bệnh Nhân', 'yearofbirth': 'Năm sinh', 'address': 'Địa chỉ'}
    column_searchable_list = ['yearofbirth', 'address']
    column_exclude_list = ['id']
    edit_modal = True
    details_modal = True
    create_modal = True

class PATIENTView(AuthenticatedModelView):
    column_display_pk = True
    can_view_details = True
    can_export = True
    column_labels = {'id': 'ma BN','name': 'Tên Bệnh Nhân', 'yearofbirth': 'Năm sinh', 'address': 'Địa chỉ'}
    column_searchable_list = ['yearofbirth', 'address']
    column_exclude_list = ['id']
    edit_modal = True
    details_modal = True
    create_modal = True

class MedicalCertificateDetailView(AuthenticatedModelView):
    column_display_pk = True
    can_view_details = True
    can_export = True
    column_labels = {'quantily': 'Số Lượng', 'medicine': 'Tên Thuốc', 'medicalcertificate': 'Mã Phiếu Khám'}

class UnitView(AuthenticatedModelView):
    column_display_pk = True
    can_view_details = True
    can_export = True
    column_labels = {'name': 'Loại THuốc', 'id': 'Mã Loại Thuốc'}

class MesicalRView(AuthenticatedModelView):
    column_filters = ["name", "yearofbirth", "register_date"]
    column_searchable_list = ["name"]
    can_view_details = True
    edit_modal = True
    details_modal = True
    create_modal = True

class UserView(AuthenticatedModelView):
    can_view_details = True
    edit_modal = True
    details_modal = True
    create_modal = True

class MedicalExaminationPatientView(AuthenticatedModelView):
    can_view_details = True
    edit_modal = True
    details_modal = True
    create_modal = True
    column_searchable_list = ['mc_id']

class MedicalExaminationListView(AuthenticatedModelView):
    edit_modal = True
    details_modal = True
    create_modal = True
    column_filters = ['nurse_id', 'mc_date']

class StatsView(BaseView):
    @expose('/')
    def index(self):
        return self.render('admin/stats.html', stats=utils.drugfrequency_stats())

    def is_accessible(self):
        return current_user.is_authenticated and current_user.user_role == UserRole.ADMIN


class LogoutView(BaseView):
    @expose('/')
    def index(self):
        logout_user()
        return redirect('/admin')

    def is_accessible(self):
        return current_user.is_authenticated


class MyAdminIndexView(AdminIndexView):
    @expose('/')
    def index(self):
        kwname = request.args.get('kwname')
        kwy = request.args.get('kwy')
        kwslk = request.args.get('kwslk')
        kwds = request.args.get('kwds')
        kwyt = request.args.get('kwyt')
        kwbn = request.args.get('kwbn')
        from_date = request.args.get('from_date')
        to_date = request.args.get('to_date')
        return self.render('admin/index.html', stats=utils.drugfrequency_stats(),patient = utils.patient_view(kwname=kwname, kwy=kwy, kwslk=kwslk), mclist = utils.mclist_view(kwds=kwds, kwyt=kwyt,kwbn=kwbn, from_date=from_date, to_date=to_date))



admin = Admin(app=app, name='Phong Kham Tu', template_mode='bootstrap4', index_view=MyAdminIndexView())

admin.add_view(MedicalCertificateView(MedicalCertificate, db.session, name='Phiếu Khám'))
admin.add_view(MedicineView(Medicine, db.session, name='Danh Sách Thuốc'))
admin.add_view(PATIENTView(PATIENT, db.session, name='Bệnh Nhân'))
admin.add_view(MedicalCertificateDetailView(MedicalCertificateDetail, db.session, name='Thêm Thuốc Vào Phiếu khám'))
admin.add_view(UnitView(Unit, db.session, name='Đơn Vị'))
admin.add_view(UserView(User, db.session, name='User'))
admin.add_view(MesicalRView(MedicalRegister, db.session, name='DS đăng ký khám'))
admin.add_view(MedicalExaminationPatientView(MedicalExaminationPatient, db.session, name ='BN Kham Benh'))
admin.add_view(MedicalExaminationListView(MedicalExaminationList, db.session, name='DanhSKham'))
admin.add_view(StatsView(name='Stats'))
admin.add_view(LogoutView(name='Logout'))