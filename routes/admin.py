from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from functools import wraps
from extensions import db
from models import User, Professional, Review, CATEGORIES

admin_bp = Blueprint('admin', __name__, url_prefix='/admin')


def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or current_user.role != 'admin':
            flash('Nuk keni akses në këtë faqe.', 'danger')
            return redirect(url_for('main.index'))
        return f(*args, **kwargs)
    return decorated_function


@admin_bp.route('/')
@login_required
@admin_required
def dashboard():
    users_count = User.query.count()
    professionals_count = Professional.query.count()
    pending_count = Professional.query.filter_by(approved=False).count()
    reviews_count = Review.query.count()

    return render_template('admin/dashboard.html',
                           users_count=users_count,
                           professionals_count=professionals_count,
                           pending_count=pending_count,
                           reviews_count=reviews_count)


@admin_bp.route('/users')
@login_required
@admin_required
def manage_users():
    users = User.query.all()
    return render_template('admin/users.html', users=users)


@admin_bp.route('/users/delete/<int:user_id>', methods=['POST'])
@login_required
@admin_required
def delete_user(user_id):
    user = User.query.get_or_404(user_id)
    if user.id == current_user.id:
        flash('Nuk mund të fshini veten.', 'danger')
        return redirect(url_for('admin.manage_users'))

    db.session.delete(user)
    db.session.commit()
    flash('Përdoruesi u fshi me sukses.', 'success')
    return redirect(url_for('admin.manage_users'))


@admin_bp.route('/professionals')
@login_required
@admin_required
def manage_professionals():
    professionals = Professional.query.all()
    return render_template('admin/professionals.html', professionals=professionals)


@admin_bp.route('/professionals/approve/<int:prof_id>', methods=['POST'])
@login_required
@admin_required
def approve_professional(prof_id):
    professional = Professional.query.get_or_404(prof_id)
    professional.approved = True
    db.session.commit()
    flash(f'Profili i {professional.full_name} u aprovua me sukses.', 'success')
    return redirect(url_for('admin.manage_professionals'))


@admin_bp.route('/professionals/reject/<int:prof_id>', methods=['POST'])
@login_required
@admin_required
def reject_professional(prof_id):
    professional = Professional.query.get_or_404(prof_id)
    professional.approved = False
    db.session.commit()
    flash(f'Profili i {professional.full_name} u refuzua.', 'warning')
    return redirect(url_for('admin.manage_professionals'))


@admin_bp.route('/professionals/delete/<int:prof_id>', methods=['POST'])
@login_required
@admin_required
def delete_professional(prof_id):
    professional = Professional.query.get_or_404(prof_id)
    db.session.delete(professional)
    db.session.commit()
    flash('Profili profesional u fshi me sukses.', 'success')
    return redirect(url_for('admin.manage_professionals'))


@admin_bp.route('/reviews')
@login_required
@admin_required
def manage_reviews():
    reviews = Review.query.order_by(Review.created_at.desc()).all()
    return render_template('admin/reviews.html', reviews=reviews)


@admin_bp.route('/reviews/delete/<int:review_id>', methods=['POST'])
@login_required
@admin_required
def delete_review(review_id):
    review = Review.query.get_or_404(review_id)
    db.session.delete(review)
    db.session.commit()
    flash('Vlerësimi u fshi me sukses.', 'success')
    return redirect(url_for('admin.manage_reviews'))


@admin_bp.route('/categories')
@login_required
@admin_required
def manage_categories():
    return render_template('admin/categories.html', categories=CATEGORIES)
