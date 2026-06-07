from flask import Blueprint, render_template, request
from models import Professional, CATEGORIES
from sqlalchemy import or_

main_bp = Blueprint('main', __name__)


@main_bp.route('/')
def index():
    top_professionals = Professional.query.filter_by(approved=True).all()
    # Sort by average rating descending
    top_professionals.sort(key=lambda p: p.average_rating, reverse=True)
    top_professionals = top_professionals[:6]

    return render_template('main/index.html',
                           categories=CATEGORIES,
                           top_professionals=top_professionals)


@main_bp.route('/search')
def search():
    query = request.args.get('q', '').strip()
    category = request.args.get('category', '').strip()
    city = request.args.get('city', '').strip()

    professionals = Professional.query.filter_by(approved=True)

    if query:
        professionals = professionals.filter(
            or_(
                Professional.first_name.ilike(f'%{query}%'),
                Professional.last_name.ilike(f'%{query}%'),
                Professional.category.ilike(f'%{query}%'),
                Professional.description.ilike(f'%{query}%'),
            )
        )

    if category:
        professionals = professionals.filter_by(category=category)

    if city:
        professionals = professionals.filter_by(city=city)

    results = professionals.all()

    return render_template('main/search.html',
                           professionals=results,
                           query=query,
                           category=category,
                           city=city,
                           categories=CATEGORIES)


@main_bp.route('/category/<category_slug>')
def category(category_slug):
    professionals = Professional.query.filter_by(
        approved=True, category=category_slug
    ).all()

    category_name = dict(CATEGORIES).get(category_slug, category_slug)

    return render_template('main/search.html',
                           professionals=professionals,
                           query='',
                           category=category_slug,
                           city='',
                           categories=CATEGORIES,
                           category_name=category_name)
