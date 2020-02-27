from application import db
from application import login_manager
from flask_login import UserMixin
from datetime import datetime


class Members(db.Model, UserMixin):
	id = db.Column(db.Integer, primary_key=True)
	first_name = db.Column(db.String(30), nullable=False)
	last_name = db.Column(db.String(30), nullable=False)
	email = db.Column(db.String(150), nullable=False, unique=True)
	password = db.Column(db.String(200), nullable=False)
	active_case = db.relationship('Active_cases', backref='Member_id', lazy=True)
	Comments = db.relationship('Comments', backref='Member_id', lazy=True)

	def __repr__(self):
		return ''.join([str(self.id), '\r\n', 'Email: ',self.email, '\r\n','name: ', self.first_name, ' ',self.last_name ])

	@login_manager.user_loader
	def load_user(id):
		return Members.query.get(int(id))

class Active_cases(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
	member_id = db.Column(db.Integer, db.ForeignKey('members.id'), nullable=False)
	Animal_name_type = db.Column(db.String(100), nullable=False, unique=True)
	Animal_description = db.Column(db.String(1000), nullable=False, unique=True)
	ACTIVE_CASES = db.relationship('Comments', backref='Case_ID', lazy=True)

	def __repr__(self):
		return ''.join([ 'member_id', str(self.member_id), '\r\n', 'Animal_name_type: ', self.Animal_name_type, '\r\n', self.Animal_description])

class Comments(db.Model, UserMixin):
	id = db.Column(db.Integer, primary_key=True)
	member_ID = db.Column(db.Integer, db.ForeignKey('members.id'), nullable=False)
	case_id = db.Column(db.Integer, db.ForeignKey('active_cases.id'), nullable=False)
	comments = db.Column(db.String(1000), nullable=False)

	def __repr__(self):
		return '',join([ 'MemberID: ', str(self.member_ID), '\r\n ', 'CASE_ID: ', self.case_id, '\r\n', 'Comment: ', self.comments])

