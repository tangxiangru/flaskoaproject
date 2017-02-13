# coding: utf-8

"""
    admin site
    use: Flask-Admin
    -- https://flask-admin.readthedocs.org/en/latest/
    """
import os
import flask_login as login
import flask_admin as admin
from flask_login import current_user
from flask_admin import Admin, BaseView, expose
from flask_admin.contrib.sqla import ModelView
from app import app, db
from app.models import AnonymousUser
from flask import redirect, flash, url_for
from flask_script import Manager, Shell
from flask_migrate import Migrate, MigrateCommand

from app import create_app, db

app = create_app(os.getenv('FLASK_CONFIG') or 'default')
manager = Manager(app)
migrate = Migrate(app, db)



class MyAdminIndexView(admin.AdminIndexView):
    def is_accessible(self):
        return login.current_user.is_admin()

    def inaccessible_callback(self, name, **kwargs):
        return redirect(url_for('auth.login'))
        
admin = Admin(
              app,
              name="admin site",
              template_mode="bootstrap3",
              index_view=MyAdminIndexView(),
              base_template='admin/logout.html'
              )


def make_shell_context():
    return dict(app=app, db=db)
manager.add_command("shell", Shell(make_context=make_shell_context))
manager.add_command('db', MigrateCommand)



# sql models management
from app.models import User
admin.add_view(ModelView(User, db.session))

from app.models import Role
admin.add_view(ModelView(Role, db.session))

if __name__ == '__main__':
    manager.run()

