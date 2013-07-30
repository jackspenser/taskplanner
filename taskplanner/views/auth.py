from taskplanner import app
from taskplanner.model import db, User
from taskplanner.helpers import (login_required,
                                 required_roles,
                                 get_client_select_group)
from taskplanner.forms import LoginForm
from flask import (request,
                   session,
                   redirect,
                   url_for,
                   render_template,
                   flash,
                   abort)

@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    form = LoginForm(request.form)
    if form.validate_on_submit():
        theUser = User.query.filter_by(username=form.username.data).first()
        if not theUser:
            error = 'Invalid username'
        elif not theUser.check_password(form.password.data):
            error = 'Invalid password'
        else:
            session['user'] = theUser.username
            flash('You were logged in')
            if session.get('next'):
                return redirect(session.pop('next'))
            else:
                return redirect(url_for('project_list'))
    else:
        # check for next url
        if request.args.get('next'):
            session['next'] = request.args.get('next')
    return render_template('login.html', error=error, form=form)

@app.route('/logout')
@login_required
def logout():
    session.pop('user', None)
    flash('You were logged out')
    return redirect(url_for('login'))