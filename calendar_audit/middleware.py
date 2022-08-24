import jwt
from django.contrib.auth.models import User


class JWTMiddleware:
    # TODO: verify id_token for auth endpoints
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if "HTTP_AUTHORIZATION" in request.META:
            id_token = request.META["HTTP_AUTHORIZATION"]

            decoded = jwt.decode(
                id_token,
                algorithms=["RS256"],
                options={"verify_signature": False},
            )
            sub = decoded["sub"]

            request.id_token = id_token
            request.username = sub
            request.user = User.objects.filter(username=request.username).first()

        response = self.get_response(request)

        return response
