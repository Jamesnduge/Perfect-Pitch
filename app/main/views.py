from flask import render_template,request,redirect,url_for,abort
from . import main
from ..models import Review, User
from .forms import ReviewForm
from flask_login import login_required
from .. import db

@main.route('/')
def index():

    '''
    View root page function that returns the index page and its data
    '''
    title = '----Perfect-Pitch----'
    return render_template('index.html',title =title)

@main.route('/user/<uname>')
def profile(uname):
    user = User.query.filter_by(username = uname).first()

    if user is None:
        abort(404)

    return render_template("pitch.html", user = user)

@main.route('/user/home/category/<category>')
@login_required
def new_pitch(category):
    '''

    '''
    pitch = ReviewForm()
    title = f'{title}'
    reviews = Review.get_reviews(pitch_id)
    return render_template('pitch.html', reviews= reviews)

@main.route('/user/home/category/review/new/<int:id>', methods = ['GET','POST'])
@login_required
def new_review(id):
    form = ReviewForm()
    movie = get_movie(id)

    if form.validate_on_submit():
        title = form.title.data
        review = form.review.data
        new_review = Review(pitch_id,title,pitch,review)
        new_review.save_review()
        return redirect(url_for('pitch',id = pitch_id ))

    title = f'{movie.title} review'
    return render_template('review.html',title = title, review_form=form, pitch=pitch)
