from ..db import db
from datetime import datetime
from werkzeug.security import check_password_hash,generate_password_hash


Follow = db.Table("Follow",
                          db.Column("following_id",db.Integer,db.ForeignKey("user.id"),primary_key=True),
                          db.Column("follower_id",db.Integer,db.ForeignKey("user.id"),primary_key=True))

class User(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(100),nullable=False)
    email= db.Column(db.String(256),nullable=False,unique=True)
    password = db.Column(db.String(256),nullable=False)
    date_created = db.Column(db.String(256),default=datetime.utcnow)
    posts = db.relationship("Post",backref="user",cascade="all,delete",lazy="dynamic")
    followers = db.relationship('User', 
                                secondary = Follow, 
                                primaryjoin = (Follow.c.following_id == id),
                                secondaryjoin = (Follow.c.follower_id == id),
                                backref = 'following'
                                )
    def follow(self, user):
        if not self.is_following(user):
            follow = Follow(follower=self, followed=user)
            db.session.add(follow)
            db.session.commit()

    def unfollow(self, user):
        follow = self.following.filter_by(followed_id=user.id).first()
        if follow:
            db.session.delete(follow)
            db.session.commit()

    def is_following(self, user):
        if user.id is None:
            return False
        return self.following.filter_by(followed_id=user.id).first() is not None

    def is_followed_by(self, user):
        return self.followers.filter_by(follower_id=user.id).first() is not None

    #bio
    #updated at
    def check_password(self,data):
        return check_password_hash(self.password,data)
        
    
    def set_password(self,data):
        return  generate_password_hash(data)



 



class Post(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    content = db.Column(db.String)
    email= db.Column(db.String(),nullable=False)
    date_created = db.Column(db.String(),default=datetime.utcnow)
    user_id = db.Column(db.Integer,db.ForeignKey("user.id"),unique=True)