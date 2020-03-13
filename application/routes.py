from flask import render_template, redirect, url_for, request
from application import app, db, bcrypt
from application.models import Members, Profile, Comments
from application.forms import ProfileForm, RegistrationForm, LoginForm, UpdateAccountForm, CommentForm
from flask_login import login_user, current_user, logout_user, login_required
from sqlalchemy import func
import random
import string

@app.route('/post', methods=['GET', 'POST'])
@login_required
def post():
	form=ProfileForm()
	if form.validate_on_submit():
		profileData = Profile(Personality = form.Personality.data,
		Desired_qualities = form.Desired_qualities.data,
		members_id = current_user )
		db.session.add(profileData)
		db.session.commit()
		return redirect(url_for('home'))
	else:
		print(form.errors)
	return render_template('post.html', title='Post', form=form)

@app.route('/')
@app.route('/home')
def home():
	profileData = Profile.query.all()
	return render_template('home.html', title='Home', profiles=profileData )

@app.route('/places')
def places():
	return render_template('places.html', title='Places')

@app.route('/random1')
def randdd():
	random_letter = Profile.query.order_by(func.random()).id=profile.id()
	return render_template('random1.html', title='random1', rand=random_letter)


@app.route('/comments', methods=['GET', 'POST'])
@login_required
def comments():
	comment_form=CommentForm
	all_case = ProfileForm.query.all
	return render_template('comments.html', title='Comments_all',comments=all_case, form=comment_form)


@app.route('/comments/<Profile_ID>', methods=['GET', 'POST'])
@login_required
def comment(Profile_ID):
	comment_form = CommentForm()
	profile = Profile.query.filter_by(id=Profile_ID).first()
	if profile and comment_form.validate_on_submit():
		comment_to_add = Comments(
		member_ID = current_user.id,
		Profile_id = profile.id,
		comments = comment_form.comment.data
		)
		db.session.add(comment_to_add)
		db.session.commit()
	all_comments = Comments.query.all()
	return render_template('comments.html', title='Comments', comments=all_comments, form=comment_form)

@app.route('/login', methods=['GET', 'POST'])
def login():
	if current_user.is_authenticated:
		return redirect(url_for('home'))
	form = LoginForm()
	if form.validate_on_submit():
		user=Members.query.filter_by(email=form.email.data).first()
		if user and bcrypt.check_password_hash(user.password, form.password.data):
			login_user(user, remember=form.remember.data)
			next_page = request.args.get('next')
			if next_page:
				return redirect(next_page)
			else:
				return redirect(url_for('home'))
	return render_template('login.html', title='Login', form=form)

@app.route('/logout')
def logout():
	logout_user()
	return redirect(url_for('login'))

@app.route('/register', methods=['GET', 'POST'])
def register():
	if current_user.is_authenticated:
		return redirect(url_for('home'))
	form = RegistrationForm()
	if form.validate_on_submit():
		hash_pw = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
		user = Members(first_name=form.first_name.data,last_name=form.last_name.data,email = form.email.data, password = hash_pw)

		db.session.add(user)
		db.session.commit()

		return redirect(url_for('login'))
	return render_template('register.html', title='Register', form=form)

@app.route('/about')
def about():
        return render_template('about.html', title='About')

@app.route('/account', methods=['GET', 'POST'])
@login_required
def account():
	form = UpdateAccountForm()
	if form.validate_on_submit():
		current_user.first_name = form.first_name.data
		current_user.last_name = form.last_name.data
		current_user.email = form.email.data
		db.session.commit()
		return redirect(url_for('account'))
	elif request.method == 'GET':
		form.first_name.data = current_user.first_name
		form.last_name.data = current_user.last_name
		form.email.data = current_user.email
		db.session.add(current_user)
		db.session.commit()
	return render_template('account.html', title='Account', form=form)

@app.route("/account/delete", methods=["GET", "POST"])
@login_required
def account_delete():
	user = current_user.id
	account = Members.query.filter_by(id=user).first()
	posts = ProfileForm.query.filter_by(member_id=user).all()
	logout_user()
	for profile in profiles:
		db.session.delete(profile)
	db.session.delete(account)
	db.session.commit()
	return redirect(url_for('register'))

@app.route('/comment/delete/<id>', methods=["GET", "POST"])
@login_required
def comment_delete_by_id(id):
	comment = Comments.query.filter_by(id=id).first()
	db.session.delete(comment)
	db.session.commit()
	return redirect(url_for('home'))
