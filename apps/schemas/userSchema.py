from marshmallow import fields,Schema



class UserSchema(Schema):
    id= fields.Integer(dump_only=True)
    name = fields.Str(required=True)
    email = fields.Email(required=True)
    password = fields.Str(required= True,load_only=True)

class PersonSchema(Schema):
    id =  fields.Integer(dump_only=True)
    name = fields.Str(required=True)
    password = fields.Str(required=True)


class MessageSchema(Schema):
    id =  fields.Integer(dump_only=True)
    message = fields.Str(required=True)
     

