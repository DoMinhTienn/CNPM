
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
    column_labels = {'id': 'Mã Thuốc', 'name': 'Tên thuốc', 'price': 'Gía tiền', 'unit': 'Đơn vị'}
    column_filters = ['name', 'price']
    column_searchable_list = ['name']

class BillView(AuthenticatedModelView):
    column_display_pk = True
    can_view_details = True
    can_export = True
    column_labels = ({"id": 'Mã Hóa Đơn', 'nurse_id': "Mã Y Tá", 'healthCheck_price': 'Tiền Khám'})
    column_exclude_list = ['medicalcertificate']



class UnitView(AuthenticatedModelView):
    column_display_pk = True
    can_view_details = True
    can_export = True
    column_labels = {'name': 'Đơn Vị', 'id': 'Mã Đơn Vị'}



class UserView(AuthenticatedModelView):
    can_view_details = True
    edit_modal = True
    details_modal = True
    create_modal = True



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

class Patients(BaseView):
    @expose('/')
    def index(self):
        kwname = request.args.get('kwname')
        kwy = request.args.get('kwy')
        kwslk = request.args.get('kwslk')
        return self.render('admin/patients.html', patient=utils.patient_view(kwname=kwname, kwy=kwy, kwslk=kwslk))


class Medicalcertificate(BaseView):
    @expose('/')
    def index(self):
        pk_id = request.args.get('pk')
        mcd = utils.get_mc_by_id(pk_id=pk_id)
        medicine_list = utils.get_medicine_by_mc_id(mc_id=pk_id)
        return  self.render('admin/MedicalCertificateDetail.html', mc = utils.read_Medicalcertificate(), mdc_list = medicine_list, mcd = mcd, pk_id = pk_id)
class MedicalExaminationList(BaseView):
    @expose('/')
    def index(self):
        stt = 0;
        kwyt = request.args.get('kwyt')
        date = request.args.get('date')
        mcdate = request.args.get('mc_date')
        mclist_p = None
        if mcdate:
            mclist_p = utils.get_mc_by_day(mcdate=mcdate)
        return self.render('admin/MedicalExaminationList.html', mclist=utils.read_mclist(kwyt=kwyt,date= date ), mclist_p = mclist_p, mcdate = mcdate, stt = stt)


class MyAdminIndexView(AdminIndexView):
    @expose('/')
    def index(self):
        kwtt = request.args.get('kwtt')
        kwdv = request.args.get('kwdv')
        kwsld = request.args.get('sl')
        return self.render('admin/index.html', stats=utils.drugfrequency_stats(kwtt=kwtt, kwdv=kwdv, kwsld=kwsld))


admin = Admin(app=app, name='Phong Kham Tu', template_mode='bootstrap4', index_view=MyAdminIndexView())

admin.add_view(MedicalExaminationList(name='Danh Sách Khám Bệnh'))
admin.add_view(Medicalcertificate(name='Phiếu Khám'))
admin.add_view(Patients(name='Bệnh nhân'))
admin.add_view(MedicineView(Medicine, db.session, name='Danh Sách Thuốc'))
admin.add_view(BillView(Bill, db.session, name='Hóa Đơn'))
admin.add_view(UnitView(Unit, db.session, name='Đơn Vị'))
admin.add_view(UserView(User, db.session, name='User'))
admin.add_view(StatsView(name='Thống Kê'))
admin.add_view(LogoutView(name='Đăng Xuất'))