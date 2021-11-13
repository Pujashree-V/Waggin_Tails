from django.shortcuts import render, redirect
##################### Custom Error Handling ##############################

def error_400(request, exception):
        data = {}
        response = render(request,'400.html', data)
        response.status_code = 400
        return response

def error_403(request, exception):
        data = {}
        response = render(request,'403.html', data)
        response.status_code = 403
        return response
    
def error_404(request, exception):
        data = {}
        print('404 called..')
        response = render(request,'404.html', status=404)
        response.status_code = 404
        return response    

def error_500(request):
        data = {}
        response = render(request,'500.html', data)
        response.status_code = 500
        return response