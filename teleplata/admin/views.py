import flask_admin as admin
from flask import g, redirect, url_for, request
from flask_admin import expose
from flask_admin.contrib.sqla import ModelView

from teleplata.main.common import MODEL_FIELDS


class AuthMixin:
    @property
    def is_authenticated(self):
        if g.user:
            return True
        else:
            return False


class MyAdminIndexView(AuthMixin, admin.AdminIndexView):
    @expose('/')
    def index(self):
        if not self.is_authenticated:
            return redirect(url_for('main.login'))
        return super(MyAdminIndexView, self).index()


class MyModelView(AuthMixin, ModelView):
    column_searchable_list = MODEL_FIELDS
    form_excluded_columns = ('pub_date',)
    can_export = True

    def is_accessible(self):
        return self.is_authenticated

    def inaccessible_callback(self, name, **kwargs):
        # redirect to login page if user doesn't have access
        return redirect(url_for('main.login', next=request.url))


admin = admin.Admin(index_view=MyAdminIndexView())
