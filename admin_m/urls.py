from django.urls import re_path
from django.contrib.auth.decorators import login_required

from .views import AdminMIndexView, AdminMImportView, AdminMImportInfoView, AdminMExportView

app_name = 'admin_m'

urlpatterns = [
    re_path(r'^$', login_required(AdminMIndexView.as_view(), login_url="/admin/login/"), name='admin_m_home'),
    re_path(r'^import/$', login_required(AdminMImportView.as_view(), login_url="/admin/login/"), name='admin_m_import'),
    re_path(r'^import/(?P<import_info_slug>[-\w]+)/$', login_required(AdminMImportInfoView.as_view(), login_url="/admin/login/"), name='import_info'),
    re_path(r'^export/$', login_required(AdminMExportView.as_view(), login_url="/admin/login/"), name='admin_m_export'),
]