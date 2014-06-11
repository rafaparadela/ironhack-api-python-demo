# -*- coding: utf-8 -*-

from django.http import HttpResponse
import json

# Create your views here.

def default(request):
    """ Metodo default pruebas """
    data=json.dumps({'status': 'failed', 'response':'How cool is that'})
    return HttpResponse(data, content_type="application/json")