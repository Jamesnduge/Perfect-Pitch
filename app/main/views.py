from flask import render_template,request,redirect,url_for,abort
from . import main
from ..models import User, Comment, Upvote, Downvote, Pitch
from .forms import pitchForm, commentForm, upvoteForm, updateProfile
from flask_login import login_required,current_user
from .. import db

@main.route('/')
def index():

    '''
    View root page function that returns the index page and its data
    '''
    title = '--Perfect-Pitch--'
    return render_template('index.html',title =title)

@main.route('/pickup', methods=['GET', 'POST'])
def pickup():

    pitch = Pitch.query.filter_by().first()
    pickuppitch = Pitch.query.filter_by(category="pickuppitch")
    return render_template('pickup.html', pitch=pitch, pickuppitch=pickuppitch)


@main.route('/interview', methods=['GET', 'POST'])
def interview():
    pitch = Pitch.query.filter_by().first()
    interviewpitch = Pitch.query.filter_by(category="interviewpitch")

    return render_template('interview.html', pitch=pitch, interviewpitch=interviewpitch)

@main.route('/product', methods=['GET', 'POST'])
def product():
    techpitch = Pitch.query.filter_by(category="techpitch")
    pitch = Pitch.query.filter_by().first()
    return render_template('product.html', pitch=pitch, techpitch=techpitch)


@main.route('/user/<uname>')
def profile(uname):
    user = User.query.filter_by(username = uname).first()

    if user is None:
        abort(404)

    return render_template("profile/profile.html", user = user)

@main.route('/user/<uname>/update',methods = ['GET','POST'])
@login_required
def update_profile(uname):
    user = User.query.filter_by(username = uname).first()
    if user is None:
        abort(404)

    form = updateProfile()

    if form.validate_on_submit():
        user.bio = form.bio.data

        db.session.add(user)
        db.session.commit()

        return redirect(url_for('.profile',uname=user.username))

    return render_template('profile/update.html',form =form)

@main.route('/user/<uname>/update/pic',methods= ['POST'])
@login_required
def update_pic(uname):
    user = User.query.filter_by(username = uname).first()
    if 'photo' in request.files:
        filename = photos.save(request.files['photo'])
        path = f'photos/{filename}'
        user.profile_pic_path = path
        db.session.commit()
    return redirect(url_for('main.profile',uname=uname))

@main.route('/pitches/new/', methods=['GET', 'POST'])
@login_required
def new_pitch():
    form = pitchForm()
    my_upvotes = Upvote.query.filter_by(pitch_id=Pitch.id)
    if form.validate_on_submit():
        description = form.description.data
        title = form.title.data
        owner_id = current_user
        category = form.category.data
        print(current_user._get_current_object().id)
        new_pitch = Pitch(owner_id=current_user._get_current_object().id, title=title, description=description,
                          category=category)
        db.session.add(new_pitch)
        db.session.commit()

        return redirect(url_for('main.index'))
    return render_template('pitch.html', form=form)

@main.route('/comment/new/<int:pitch_id>', methods=['GET', 'POST'])
@login_required
def new_comment(pitch_id):
    form = commentForm()
    pitch = Pitch.query.get(pitch_id)
    if form.validate_on_submit():
        description = form.description.data

        new_comment = Comment(description=description, user_id=current_user._get_current_object().id, pitch_id=pitch_id)
        db.session.add(new_comment)
        db.session.commit()

        return redirect(url_for('.new_comment', pitch_id=pitch_id))

    all_comments = Comment.query.filter_by(pitch_id=pitch_id).all()
    return render_template('comments.html', form=form, comment=all_comments, pitch=pitch)


@main.route('/pitch/upvote/<int:pitch_id>/upvote', methods=['GET', 'POST'])
@login_required
def upvote(pitch_id):
    pitch = Pitch.query.get(pitch_id)
    user = current_user
    pitch_upvotes = Upvote.query.filter_by(pitch_id=pitch_id)

    if Upvote.query.filter(Upvote.user_id == user.id, Upvote.pitch_id == pitch_id).first():
        return redirect(url_for('main.index'))

    new_upvote = Upvote(pitch_id=pitch_id)
    new_upvote.save_upvotes()
    return redirect(url_for('main.index'))


@main.route('/pitch/downvote/<int:pitch_id>/downvote', methods=['GET', 'POST'])
@login_required
def downvote(pitch_id):
    pitch = Pitch.query.get(pitch_id)
    user = current_user
    pitch_downvotes = Downvote.query.filter_by(pitch_id=pitch_id)

    if Downvote.query.filter(Downvote.user_id == user.id, Downvote.pitch_id == pitch_id).first():
        return redirect(url_for('main.index'))

    new_downvote = Downvote(pitch_id=pitch_id)
    new_downvote.save_downvotes()
    return redirect(url_for('main.index'))
