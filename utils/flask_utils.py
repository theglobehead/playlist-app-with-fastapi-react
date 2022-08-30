from __future__ import annotations

from functools import wraps
from typing import Callable

from flask import session, redirect, url_for, Response, render_template




def login_required(f: Callable) -> Callable:
    @wraps(f)
    def decorated_function(*args: list, **kwargs: dict) -> Response | dict:
        result = None
        user_id = session.get("user_id", None)
        if user_id:
            result = f(*args, **kwargs)
        else:
            result = redirect(url_for("login.login"))
        return result

    return decorated_function
