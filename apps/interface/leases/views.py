from django.http import HttpResponse

def index(request):
    message = "Hello, world. You're at the leases index."

    return HttpResponse(message)
