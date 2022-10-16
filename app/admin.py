from functools import wraps

from app.models import Admin
from app.auth import AuthSession
from app.error import APIError


def admin_required(f):
    @wraps(f)
    def decorator(*args, **kwargs):
        session: AuthSession = kwargs['session']

        admin: Admin = Admin.query.filter_by(
            user=session.user_id
        ).first()

        if admin is None:
            raise APIError(
                code=400,
                message="해당 계정은 관리자가 아닙니다."
            )

        return f(*args, **kwargs)

    return decorator
