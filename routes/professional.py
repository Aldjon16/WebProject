import os
import uuid
from flask import Blueprint, render_template, redirect, url_for, flash, request, current_app
from flask_login import login_required, current_user
from extensions import db
from models import Professional, CATEGORIES, CITIES

professional_bp = Blueprint('professional', __name__)


def allowed_file(filename):
    allowed = current_app.config.get('ALLOWED_EXTENSIONS', {'png', 'jpg', 'jpeg', 'gif', 'webp'})
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in allowed


def save_image(file):
    if file and allowed_file(file.filename):
        ext = file.filename.rsplit('.', 1)[1].lower()
        filename = f"{uuid.uuid4().hex}.{ext}"
        filepath = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        return filename
    return None


@professional_bp.route('/professional/create', methods=['GET', 'POST'])
@login_required
def create_profile():
    if current_user.role != 'professional':
        flash('Vetëm profesionistët mund të krijojnë profil.', 'danger')
        return redirect(url_for('main.index'))

    if current_user.professional:
        return redirect(url_for('professional.edit_profile'))

    if request.method == 'POST':
        first_name = request.form.get('first_name', '').strip()
        last_name = request.form.get('last_name', '').strip()
        category = request.form.get('category', '').strip()
        city = request.form.get('city', '').strip()
        phone = request.form.get('phone', '').strip()
        description = request.form.get('description', '').strip()
        experience = request.form.get('experience', '').strip()

        if not all([first_name, last_name, category, city, phone]):
            flash('Ju lutem plotësoni të gjitha fushat e detyrueshme.', 'danger')
            return render_template('professional/create.html',
                                   categories=CATEGORIES, cities=CITIES)

        image_filename = 'default.png'
        if 'image' in request.files:
            file = request.files['image']
            if file.filename:
                saved = save_image(file)
                if saved:
                    image_filename = saved

        professional = Professional(
            user_id=current_user.id,
            first_name=first_name,
            last_name=last_name,
            category=category,
            city=city,
            phone=phone,
            description=description,
            experience=experience,
            image=image_filename,
            approved=False
        )
        db.session.add(professional)
        db.session.commit()

        flash('Profili u krijua me sukses! Profili juaj do të shqyrtohet nga administratori.', 'success')
        return redirect(url_for('professional.dashboard'))

    return render_template('professional/create.html',
                           categories=CATEGORIES, cities=CITIES)


@professional_bp.route('/professional/edit', methods=['GET', 'POST'])
@login_required
def edit_profile():
    if current_user.role != 'professional' or not current_user.professional:
        flash('Nuk keni profil profesional.', 'danger')
        return redirect(url_for('main.index'))

    professional = current_user.professional

    if request.method == 'POST':
        professional.first_name = request.form.get('first_name', '').strip()
        professional.last_name = request.form.get('last_name', '').strip()
        professional.category = request.form.get('category', '').strip()
        professional.city = request.form.get('city', '').strip()
        professional.phone = request.form.get('phone', '').strip()
        professional.description = request.form.get('description', '').strip()
        professional.experience = request.form.get('experience', '').strip()

        if 'image' in request.files:
            file = request.files['image']
            if file.filename:
                saved = save_image(file)
                if saved:
                    # Delete old image if not default
                    if professional.image != 'default.png':
                        old_path = os.path.join(current_app.config['UPLOAD_FOLDER'],
                                                professional.image)
                        if os.path.exists(old_path):
                            os.remove(old_path)
                    professional.image = saved

        db.session.commit()
        flash('Profili u përditësua me sukses!', 'success')
        return redirect(url_for('professional.dashboard'))

    return render_template('professional/edit.html',
                           professional=professional,
                           categories=CATEGORIES,
                           cities=CITIES)


@professional_bp.route('/professional/dashboard')
@login_required
def dashboard():
    if current_user.role != 'professional':
        flash('Kjo faqe është vetëm për profesionistë.', 'danger')
        return redirect(url_for('main.index'))

    if not current_user.professional:
        return redirect(url_for('professional.create_profile'))

    professional = current_user.professional
    reviews = professional.reviews.order_by(db.desc('created_at')).all()

    return render_template('professional/dashboard.html',
                           professional=professional,
                           reviews=reviews)


@professional_bp.route('/professional/<int:prof_id>')
def view_profile(prof_id):
    professional = Professional.query.get_or_404(prof_id)
    reviews = professional.reviews.order_by(db.desc('created_at')).all()

    return render_template('professional/profile.html',
                           professional=professional,
                           reviews=reviews)
