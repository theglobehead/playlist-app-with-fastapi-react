from __future__ import annotations

from functools import wraps
from typing import Callable

from flask import session, redirect, url_for, Response


def login_required(f: Callable) -> Callable:
    @wraps(f)
    def decorated_function(*args: list, **kwargs: dict) -> Response | dict:
        result = None
        user = session.get("user", None)
        if user:
            result = f(*args, **kwargs)
        else:
            result = redirect(url_for("login.login"))
        return result

    return decorated_function
