# users/authentication.py
import jwt
from django.conf import settings
from rest_framework import exceptions
from rest_framework.authentication import BaseAuthentication
from django.db import connection
from users.models import CustomUser

class SchemaAwareJWTAuthentication(BaseAuthentication):
    """
    Decode Authorization: Bearer <access_token>
    Then load the user using a schema-qualified raw query:
        SELECT * FROM users.custom_user WHERE id = %s
    This bypasses any search_path/table-name issues.
    """

    def authenticate(self, request):
        auth_header = request.headers.get("Authorization")
        if not auth_header:
            return None

        parts = auth_header.split()
        if len(parts) != 2 or parts[0].lower() != "bearer":
            raise exceptions.AuthenticationFailed("Invalid Authorization header format")

        token = parts[1]

        try:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[getattr(settings, "JWT_ALGORITHM", "HS256")])
        except jwt.ExpiredSignatureError:
            raise exceptions.AuthenticationFailed("Token has expired")
        except jwt.InvalidTokenError:
            raise exceptions.AuthenticationFailed("Invalid token")

        # ensure token type is access (if you put type in payload)
        if payload.get("type") and payload.get("type") != "access":
            raise exceptions.AuthenticationFailed("Invalid token type")

        user_id = payload.get("user_id") or payload.get("user") or payload.get("sub")
        if not user_id:
            raise exceptions.AuthenticationFailed("Token missing user identifier")

        # Use raw SQL with fully qualified table name (schema.table)
        # NOTE: table name must match exactly the db_table you used in model Meta
        sql = 'SELECT * FROM users.custom_user WHERE id = %s LIMIT 1'
        try:
            qs = CustomUser.objects.raw(sql, [str(user_id)])
            user = None
            for u in qs:
                user = u
                break
            if user is None:
                raise CustomUser.DoesNotExist()
        except CustomUser.DoesNotExist:
            raise exceptions.AuthenticationFailed("User not found")

        # Optionally check is_active flag if present
        if hasattr(user, "is_active") and not user.is_active:
            raise exceptions.AuthenticationFailed("User inactive")

        return (user, None)
