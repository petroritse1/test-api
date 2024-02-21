from flask_smorest import Blueprint,abort
from flask.views import MethodView
from ..schemas.userSchema import UserSchema,PersonSchema,MessageSchema
from flask import request,jsonify
from ..models.user_model import Post,User
from sqlalchemy.exc import IntegrityError,SQLAlchemyError
from ..db import db
from flask_jwt_extended import create_access_token,jwt_required,get_jwt,create_refresh_token,get_jwt_identity
from blocklist import BLOCKLIST
import os,requests
from sqlalchemy import or_
from tasks import send_user_registration_email
from flask import current_app


blp = Blueprint("user",__name__,description="Users blue print")



 

 
 

@blp.route("/user")
class Users(MethodView):
    @blp.response(200,UserSchema(many=True))
    def get(self):
        return User.query.all()
    

    # @jwt_required()
    @blp.arguments(UserSchema)
    @blp.response(201,UserSchema)
    def post(self,user_data):
        if User.query.filter(or_(User.email== user_data["email"],User.name == user_data["name"])).first():
            abort(409,message="A user with that username or email already exists.")
        user_data["password"]= User.set_password(self,user_data["password"])
        new_user = User(**user_data)
        try:
            db.session.add(new_user)
            db.session.commit()

            body =f"Welcome {user_data['name']} to petesroy testing applications!🎉"
            subject = "Account created!"
            current_app.queue.enqueue(send_user_registration_email,user_data["email"],user_data["name"])
            # send_user_registration_email(user_data["email"],user_data["name"])
        except IntegrityError:
            abort(400,message="Name already exists!")
        except SQLAlchemyError:
            # db.session.rollback()
            abort(500,message="An error occurred while inserting the item.")
         
        return jsonify({"messagge":f"New user {new_user.name} has been added successfully!🎉"})
   

 
@blp.route("/user/<int:id>")
class UserData(MethodView):
    def get(self,id):
       
        user = User.query.get_or_404(id)
        return {"message":f"{user.name} is registered!"}
    

    @jwt_required()
    @blp.arguments(UserSchema)
    @blp.response(201,UserSchema)
    def put( self,person_data,id):
        user = User.query.get_or_404(id)
        person_data = person_data
        try:
             
            if user:
                user.name = person_data["name"]
                user.email = person_data["email"]
                user.password = User.set_password(self, person_data["password"])
  
            user=User(**person_data,id=id)

            db.session.add(user)
            db.session.commit()
        except IntegrityError:
            abort(400,message="Name already exists!")


        return {"message":"user info has been updated!"}
    
    @jwt_required()
    def delete(self,id):
        jwt = get_jwt()
        
        # if not jwt.get("is_admin"):
        #     abort(401,message="Admin privilege required")
        user = User.query.get_or_404(id)
        db.session.delete(user)
        db.session.commit()
        return {"message": f"{user.name} has been deleted "},200


@blp.route("/login")
class Login(MethodView):
    @blp.arguments(PersonSchema)
    @blp.response(201,PersonSchema)
    def post(self,person_data):
        user = User.query.filter(User.name == person_data["name"]).first()
       
        if user and user.check_password(person_data["password"]):
            access_token = create_access_token(identity=user.id,fresh=True)
            refresh_token = create_refresh_token(identity=user.id)
            return jsonify({"message":access_token})
            
        abort(401,message="Invalid credentials!")

@blp.route("/logout")
class Logout(MethodView):
    @jwt_required()
    def post(self):
        jti = get_jwt()["jti"]
        BLOCKLIST.add(jti)
        return {"message": "Successfully logged out"}, 200


@blp.route("/refresh")
class RefreshToken(MethodView):
    @jwt_required(refresh=True)
    def post(self):
        current_user = get_jwt_identity()
        new_token = create_access_token(identity=current_user,fresh=False)
        jti = get_jwt()["jti"]
        BLOCKLIST.add(jti)
        return {"access_token": new_token}, 200

@blp.route("/community")
class Social(MethodView):
#
    @jwt_required(fresh=True)
    @blp.arguments(MessageSchema)
    @blp.response(201,MessageSchema)
    def post(self,message_data):
      
        new_message = message_data 
 
        return new_message