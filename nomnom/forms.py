from flask_wtf import FlaskForm
from filter import Language
import wtforms as fields
import wtforms.validators as validators
import wtforms.widgets as widgets

language = Language
# Create a poll
class CreateForm(FlaskForm):
    title = fields.StringField('title', validators=[validators.DataRequired(), language])
    description = fields.StringField('description', widget=widgets.TextArea(), validators=[validators.DataRequired(), language])
    submit = fields.SubmitField(label='Create')

# Add response to a poll
class ResponseForm(FlaskForm):
    response = fields.StringField('response', validators=[validators.DataRequired(), language])
    submit = fields.SubmitField(label='Add')
