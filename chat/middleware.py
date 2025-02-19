from channels.db import database_sync_to_async
from account.models import CustomUser
from django.contrib.auth.models import AnonymousUser
from channels.middleware import BaseMiddleware
from channels.db import database_sync_to_async
from urllib.parse import parse_qs
from rest_framework_simplejwt.tokens import UntypedToken
from rest_framework_simplejwt.exceptions import InvalidToken, TokenError


@database_sync_to_async
def get_user(user_id):
    try: 
        return CustomUser.objects.get(id=user_id)
    except CustomUser.DoesNotExist:
        return AnonymousUser()
    
class JWTAuthMiddleWare(BaseMiddleware):
    async def __call__(self, scope, receive, send):
        query_string = scope['query_string'].decode()#decode() converts a byte string to a regular string
        query_params = parse_qs(query_string)#passing query string from a url into a dictionary 
        token = query_params.get('token', [None])[0]

        if token: 
            try: 
                user_id = UntypedToken(token=token)['user_id']#decodinig the jwt token to get the userid
                scope['user'] = await get_user(user_id)

            except (InvalidToken, TokenError) as e:
                scope['user'] = AnonymousUser()
        else:
            scope['user'] = AnonymousUser()

        return await super().__call__(scope, receive, send)