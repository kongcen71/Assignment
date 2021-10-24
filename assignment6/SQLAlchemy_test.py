from app import *

user = User.query.filter_by(id = 5).first()
print(user)
admin = user.admin
print(admin)
notes = Note.query.all()
print(notes)