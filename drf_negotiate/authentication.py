import socket

import base64

import gssapi
from django.contrib.auth import get_user_model
from rest_framework import authentication


class NegotiateAuthentication(authentication.BaseAuthentication):
    principal_name_field = 'principal_name'

    def authenticate(self, request):
        if request.method == 'OPTIONS':
            return
        authorization = request.META.get('HTTP_AUTHORIZATION', '')
        if authorization.startswith('Negotiate '):
            print(request)
            host = request.META['SERVER_NAME']
            service_name = 'HTTP/{}'.format(host)
            service_name = gssapi.Name(service_name)

            # The browser is authenticating using GSSAPI, trim off 'Negotiate ' and decode:
            in_token = base64.b64decode(authorization[10:])

            server_creds = gssapi.Credentials(name=service_name, usage='accept')
            ctx = gssapi.SecurityContext(creds=server_creds)

            # Feed the input token to the context, and get an output token in return
            out_token = ctx.step(in_token)
            if out_token:
                request.negotiate_token = base64.b64encode(out_token).decode()
            if ctx.complete:
                name = str(ctx.initiator_name)
                User = get_user_model()
                user = User.objects.get(**{self.principal_name_field: name})
                return user, None
            else:
                raise HTTPUnauthorized

    def authenticate_header(self, request):
        return 'Negotiate'

