from flask import redirect, session, url_for
from functools import wraps

import settings


def authenticated(f):
    """Check if user is logged in"""
    @wraps(f)
    def decorated(*args, **kwargs):
        if not session.get('snapshots_email'):
            return redirect(url_for('main'))
        return f(*args, **kwargs)
    return decorated