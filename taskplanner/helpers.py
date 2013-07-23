from taskplanner import app
from taskplanner.model import db, User, Client
from flask import request, session, redirect, url_for, abort
from functools import wraps

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get('user') is None:
            return redirect(url_for('login', next=request.url))
        return f(*args, **kwargs)
    return decorated_function

def getuser():
    if session.get('user'):
        return User.query.filter_by(username=session.get('user')).one()
    else:
        abort(404)
    
def required_roles(*roles):
    def wrapper(f):
        @wraps(f)
        def wrapped(*args, **kwargs):
            user = getuser()
            for role in roles:
                if not user.has_role(role):
                    abort(401)
            return f(*args, **kwargs)
        return wrapped
    return wrapper

def get_client_select_group():
    theClientList = []
    for client in Client.query.order_by('name'):
        nameStr = "{0} ({1})".format(client.name, client.email)
        theClientList.append((client.id, nameStr))
    return theClientList