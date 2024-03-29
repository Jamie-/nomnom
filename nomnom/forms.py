from flask_wtf import FlaskForm
import wtforms as fields
import wtforms.validators as validators
import wtforms.widgets as widgets


# Create a poll
class CreateForm(FlaskForm):
    title = fields.StringField('title', validators=[validators.DataRequired()])
    email = fields.StringField('email', validators=[validators.Email(), validators.Optional()])
    image_url = fields.StringField('image-url', validators=[validators.URL(), validators.Optional()])
    description = fields.StringField('description', widget=widgets.TextArea(), validators=[validators.DataRequired()])
    private = fields.BooleanField('privat', validators=[validators.Optional()])
    submit = fields.SubmitField(label='Create')


# Add response to a poll
class ResponseForm(FlaskForm):
    response = fields.StringField('response', validators=[validators.DataRequired()])
    submit = fields.SubmitField(label='Add')


# Check user intends to delete poll
class DeleteForm(FlaskForm):
    submit = fields.SubmitField(label='Delete')
