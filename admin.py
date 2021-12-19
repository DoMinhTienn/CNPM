from PhongKhamTu import db, app,  utils
from flask_admin.contrib.sqla import ModelView
from PhongKhamTu.model import User, UserRole, PATIENT, MedicalExaminationPatient, MedicalExaminationList, MedicalRegister, MedicalCertificate\
    , Medicine, MedicalCertificateDetail, Unit, Bill
from  flask_admin import BaseView, expose, Admin, AdminIndexView
from  flask import redirect, request



class MedicineView(ModelView):
    column_display_pk = True
    can_view_details = True
    can_export = True
    column_labels = {'name': 'Tên thuốc', 'price': 'Gía tiền', 'unit_id': 'Đơn vị'}
    column_filters = ['name', 'price']
    column_searchable_list = ['name']
    column_exclude_list = ['id']

class MedicalCertificateView(ModelView):
    column_display_pk = True
    can_view_details = True
    can_export = True
    column_labels = {'doctor_id': 'Mã bác sĩ', 'healthcheck_date': 'Ngày khám', 'symptom': 'Triệu chứng', 'guess': 'Dự đoán bệnh', 'patient_id': 'Bệnh nhân'}
    column_filters = ['doctor_id', 'healthcheck_date', 'patient_id']
    column_searchable_list = ['id']
    column_exclude_list = ['id', 'details', 'bills']

class PATIENTView(ModelView):
    column_display_pk = True
    can_view_details = True
    can_export = True
    column_labels = {'id': 'ma BN','name': 'Tên Bệnh Nhân', 'yearofbirth': 'Năm sinh', 'address': 'Địa chỉ'}
    column_searchable_list = ['yearofbirth', 'address']
    column_exclude_list = ['id']
    edit_modal = True
    details_modal = True
    create_modal = True

class MedicalCertificateDetailView(ModelView):
    column_display_pk = True
    can_view_details = True
    can_export = True
    column_labels = {'quantily': 'Số Lượng', 'medicine': 'Tên Thuốc', 'medicalcertificate': 'Mã Phiếu Khám'}

class UnitView(ModelView):
    column_display_pk = True
    can_view_details = True
    can_export = True
    column_labels = {'name': 'Loại THuốc', 'id': 'Mã Loại Thuốc'}

class MesicalRView(ModelView):
    column_filters = ["name", "yearofbirth", "register_date"]
    column_searchable_list = ["name"]
    can_view_details = True
    edit_modal = True
    details_modal = True
    create_modal = True

class UserView(ModelView):
    can_view_details = True
    edit_modal = True
    details_modal = True
    create_modal = True

class MedicalExaminationPatientView(ModelView):
    can_view_details = True
    edit_modal = True
    details_modal = True
    create_modal = True
    column_searchable_list = ['mc_id']

class MedicalExaminationListView(ModelView):
    edit_modal = True
    details_modal = True
    create_modal = True
    column_filters = ['nurse_id', 'mc_date']

class DanhsachView(BaseView):
    @expose('/')
    def index(self):
        kwds = request.args.get('kwds')
        kwyt = request.args.get('kwyt')
        kwbn = request.args.get('kwbn')
        from_date = request.args.get('from_date')
        to_date = request.args.get('to_date')

        return self.render('admin/Danhsachkham.html', pv = utils.DanhsachView(kwds=kwds, kwyt=kwyt,kwbn=kwbn, from_date=from_date, to_date=to_date))

class BenhnhanView(BaseView):
    @expose('/')
    def index(self):
        kwname = request.args.get('kwname')
        kwy = request.args.get('kwy')
        kwslk = request.args.get('kwslk')
        return self.render('admin/Danhsachbenhnhan.html', bn = utils.BenhnhanView(kwname=kwname, kwy=kwy, kwslk=kwslk))


admin = Admin(app=app, name="My web", template_mode="bootstrap4")
admin.add_view(MedicalCertificateView(MedicalCertificate, db.session, name='Phiếu Khám'))
admin.add_view(MedicineView(Medicine, db.session, name='Danh Sách Thuốc'))
admin.add_view(PATIENTView(PATIENT, db.session, name='Bệnh Nhân'))
admin.add_view(MedicalCertificateDetailView(MedicalCertificateDetail, db.session, name='Thêm Thuốc Vào Phiếu khám'))
admin.add_view(UnitView(Unit, db.session, name='Đơn Vị'))
admin.add_view(UserView(User, db.session, name='User'))
admin.add_view(MesicalRView(MedicalRegister, db.session, name='DS đăng ký khám'))
admin.add_view(MedicalExaminationPatientView(MedicalExaminationPatient, db.session, name ='BN Kham Benh'))
admin.add_view(MedicalExaminationListView(MedicalExaminationList, db.session, name='DanhSKham'))
admin.add_view(DanhsachView(name="Danh sách khám"))
admin.add_view(BenhnhanView(name="Danh sách bệnh nhân"))