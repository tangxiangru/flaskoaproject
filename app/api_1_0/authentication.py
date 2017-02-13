coding  : utf-8
from flask import g, request,jsonify,Response
import json
from  models import User
from app import  db
from flask_login import login_user, logout_user, current_user, login_required
from app.models import User
from app.decorators import admin_required

登录账户
@api.route('/login',methods=['GET','POST'])
def login() :
    email = request.get_json().get("email")
    password = request.get_json().get("password")
    try :
        user = User.query.filter_by(email=email).first()
    except :
        user = None
        user_id = None
    if user is not None and user.verify_password(password) :
        login_user(user)
        token = user.generate_auth_token(expiration=60*60*6)
        return jsonify ({

            "user_id" : user.id ,
            "token" : token ,
            })

#创建账户
@api.route('/users／register',method='GET','POST')
@admin_required
def register() :
    if request.method == 'POST' :
        email = request.get_json().get("email")
        password = request.get_json().get("password")
        username = request.get_json().get("username")
        user = User ( email=email ,
                     password=password)
                     db.session.add(user)
                     db.session.commit()
                     user_id=User.query.filter_by(email=email).first().id
                     return jsonify({
                                    "created" :  user_id ,})
