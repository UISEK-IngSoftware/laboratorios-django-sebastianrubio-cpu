# catalog/views/auth_view.py
import json
from django.http import HttpResponse
from django.contrib.auth import get_user_model
from oauth2_provider.views import TokenView
from oauth2_provider.models import AccessToken

class CustomTokenView(TokenView):
    def post(self, request, *args, **kwargs):
        url, headers, body, status = self.create_token_response(request)
        
        if status == 200:
            body_data = json.loads(body)
            grant_type = request.POST.get('grant_type')
            User = get_user_model()
            
            if grant_type == 'password':
                username = request.POST.get('username')
                try:
                    user = User.objects.get(username=username)
                    body_data['is_staff'] = user.is_staff
                except User.DoesNotExist:
                    body_data['is_staff'] = False
                    
            elif grant_type == 'refresh_token':
                try:
                    new_access_token = body_data.get('access_token')
                    token_obj = AccessToken.objects.select_related('user').get(token=new_access_token)
                    body_data['is_staff'] = token_obj.user.is_staff if token_obj.user else False
                except AccessToken.DoesNotExist:
                    body_data['is_staff'] = False
            else:
                body_data['is_staff'] = False
                
            body = json.dumps(body_data)
            
        return HttpResponse(content=body, status=status, headers=headers)