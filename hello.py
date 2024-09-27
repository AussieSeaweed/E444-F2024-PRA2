from os import getenv

from dotenv import load_dotenv
from flask_bootstrap import Bootstrap
from flask import flash, Flask, redirect, render_template, session, url_for
from flask_moment import Moment
from flask_wtf import FlaskForm
from wtforms import EmailField, StringField, SubmitField
from wtforms.validators import DataRequired

app = Flask(__name__)
bootstrap = Bootstrap(app)
moment = Moment(app)


class UofTForm(FlaskForm):
    name = StringField('What is your name?', validators=[DataRequired()])
    email = EmailField(
        'What is your UofT Email address?',
        validators=[DataRequired()],
    )
    submit = SubmitField('Submit')


@app.route('/', methods=['GET', 'POST'])
def index():
    form = UofTForm()

    if form.validate_on_submit():
        previous_name = session.get('name')
        session['name'] = form.name.data

        if previous_name is not None and previous_name != session['name']:
            flash('Looks like you have changed your name!')

        previous_email = session.get('email')
        session['email'] = form.email.data

        if previous_email is not None and previous_email != session['name']:
            flash('Looks like you have changed your email!')

        return redirect(url_for('index'))

    return render_template(
        'index.html',
        form=form,
        name=session.get('name'),
        email=session.get('email'),
    )


@app.route('/user/<name>')
def user(name):
    return render_template('user.html', name=name)


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500


def main():
    load_dotenv()

    app.config['SECRET_KEY'] = getenv('FLASK_SECRET_KEY')

    app.run(debug=True)


if __name__ == '__main__':
    main()
