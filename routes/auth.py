from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required, current_user
from extensions import db
from models import User

auth_bp = Blueprint('auth', __name__)


@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))

    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        email = request.form.get('email', '').strip()
        password = request.form.get('password', '')
        confirm_password = request.form.get('confirm_password', '')
        role = request.form.get('role', 'customer')

        if not username or not email or not password:
            flash('Ju lutem plotësoni të gjitha fushat.', 'danger')
            return render_template('auth/register.html')

        if password != confirm_password:
            flash('Fjalëkalimet nuk përputhen.', 'danger')
            return render_template('auth/register.html')

        if len(password) < 6:
            flash('Fjalëkalimi duhet të ketë të paktën 6 karaktere.', 'danger')
            return render_template('auth/register.html')

        if User.query.filter_by(username=username).first():
            flash('Ky emër përdoruesi ekziston tashmë.', 'danger')
            return render_template('auth/register.html')

        if User.query.filter_by(email=email).first():
            flash('Ky email ekziston tashmë.', 'danger')
            return render_template('auth/register.html')

        if role not in ('customer', 'professional'):
            role = 'customer'

        user = User(username=username, email=email, role=role)
        user.set_password(password)
        db.session.add(user)
        db.session.commit()

        flash('Regjistrimi u krye me sukses! Tani mund të kyçeni.', 'success')
        return redirect(url_for('auth.login'))

    return render_template('auth/register.html')


@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))

    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '')

        user = User.query.filter_by(username=username).first()

        if user and user.check_password(password):
            login_user(user)
            next_page = request.args.get('next')
            if user.role == 'professional' and not user.professional:
                flash('Ju lutem krijoni profilin tuaj profesional.', 'info')
                return redirect(url_for('professional.create_profile'))
            return redirect(next_page or url_for('main.index'))

        flash('Emri i përdoruesit ose fjalëkalimi janë gabim.', 'danger')

    return render_template('auth/login.html')


@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Jeni çkyçur me sukses.', 'success')
    return redirect(url_for('main.index'))
