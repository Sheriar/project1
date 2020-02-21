from flask import render_template, redirect, url_for, request
from application import app, db, bcrypt
from application.models import Active_cases, Members
from application.forms import CaseForm, RegistrationForm, LoginForm, UpdateAccountForm
from flask_login import login_user, current_user, logout_user, login_required

@app.route('/post', methods=['GET', 'POST'])
@login_required
def post():
	form=CaseForm()
	if form.validate_on_submit():
		postData = Active_cases(Animal_name_type = form.Animal_name_type.data,
		Animal_description = form.description.data,
		Member_id = current_user )
		db.session.add(postData)
		db.session.commit()
		return redirect(url_for('home'))
	else:
		print(form.errors)
	return render_template('post.html', title='Post', form=form)

@app.route('/')
@app.route('/home')
def home():
	postData = Active_cases.query.all()
	for post in postData:
		print(post.__dict__)
	return render_template('home.html', title='Home', posts = postData )

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
	account = Member.query.filter_by(id=user).first()
	posts = Active_cases.query.filter_by(user_id=user).all()
	logout_user()
	for post in posts:
		db.session.delete(post)
	db.session.delete(account)
	db.session.commit()
	return redirect(url_for('register'))

