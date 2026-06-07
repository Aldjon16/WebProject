from flask import Blueprint, redirect, url_for, flash, request
from flask_login import login_required, current_user
from extensions import db
from models import Review, Professional

review_bp = Blueprint('review', __name__)


@review_bp.route('/review/<int:prof_id>', methods=['POST'])
@login_required
def add_review(prof_id):
    professional = Professional.query.get_or_404(prof_id)

    if current_user.role != 'customer':
        flash('Vetëm klientët mund të lënë vlerësime.', 'danger')
        return redirect(url_for('professional.view_profile', prof_id=prof_id))

    # Check if user already reviewed this professional
    existing = Review.query.filter_by(
        professional_id=prof_id, user_id=current_user.id
    ).first()

    if existing:
        flash('Ju keni lënë tashmë një vlerësim për këtë profesionist.', 'warning')
        return redirect(url_for('professional.view_profile', prof_id=prof_id))

    rating = request.form.get('rating', type=int)
    comment = request.form.get('comment', '').strip()

    if not rating or rating < 1 or rating > 5:
        flash('Ju lutem jepni një vlerësim nga 1 deri në 5.', 'danger')
        return redirect(url_for('professional.view_profile', prof_id=prof_id))

    review = Review(
        professional_id=prof_id,
        user_id=current_user.id,
        rating=rating,
        comment=comment
    )
    db.session.add(review)
    db.session.commit()

    flash('Vlerësimi juaj u shtua me sukses!', 'success')
    return redirect(url_for('professional.view_profile', prof_id=prof_id))
