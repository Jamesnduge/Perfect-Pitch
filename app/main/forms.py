from flask_wtf import FlaskForm
from wtforms import StringField,TextAreaField,SubmitField,SelectField
from wtforms.validators import Required,Email,EqualTo
from wtforms import ValidationError

class pitchForm(FlaskForm):
    category = SelectField('Select category', choices=[('pickuppitch', 'Pick Up Lines'), ('techpitch', 'Product'), ('interviewpitch','Interview')])
    title = StringField('Title of your Pitch')
    description = TextAreaField('Type in your pitch')
    submit = SubmitField('Add Pitch')

class commentForm(FlaskForm):
    description = TextAreaField('Add comment',validators=[Required()])
    submit = SubmitField()

class upvoteForm(FlaskForm):
    submit = SubmitField()


class downvote(FlaskForm):
    submit = SubmitField()

class updateProfile(FlaskForm):
    bio = TextAreaField('Tell us about you.', validators=[Required()])
    submit = SubmitField('Submit')
