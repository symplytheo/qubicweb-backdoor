from django.http import HttpResponse


def index(request):
    return HttpResponse("(c) 2025 Qubicweb Backdoor")
