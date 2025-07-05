from django.shortcuts import redirect
from django.utils.deprecation import MiddlewareMixin

class PreventBackMiddleware(MiddlewareMixin):
    def process_request(self, request):
        path = request.path

        # User dashboard protection
        if path.startswith('/DashboardPage/') and not request.session.get('user_id'):
            return redirect('LoginPage')

        # Company dashboard protection
        if path.startswith('/CompDash/') and not request.session.get('company_id'):
            return redirect('Complogin')

    def process_response(self, request, response):
        response['Cache-Control'] = 'no-cache, no-store, must-revalidate'
        response['Pragma'] = 'no-cache'
        response['Expires'] = '0'
        return response