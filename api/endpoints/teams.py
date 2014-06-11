# -*- coding: utf-8 -*-

from django.http import HttpResponse
import json
from api.models import *


def add(request):
    try:
        team=Teams()
        team.team=request.POST['team']
        team.color=request.POST['color']
        team.save()
        data=json.dumps({'status': 'success', 'response':'added', 'data':{'id':team.id}})
    
    except Exception as e:
        data = json.dumps({ 'status':'failed', 'response': e.args[0] })

    return HttpResponse(data, content_type="application/json")
    
    
def delete(request):
    try:
        team=Teams.objects.get(id=request.POST["id"])
        team.delete()
        data=json.dumps({'status': 'success', 'response':'deleted'})
    
    except Exception as e:
        data = json.dumps({ 'status':'failed', 'response': e.args[0] })

    return HttpResponse(data, content_type="application/json")
    
    
def list(request):
    try:
        teams=Teams.objects.all()
        
        list_teams=[]
        for team in teams:
            list_teams.append({'id':team.id, 'team':team.team, 'color':team.color })
        
        data=json.dumps({'status': 'success', 'response':'list', 'data': list_teams });
    
    except Exception as e:
        data = json.dumps({ 'status':'failed', 'response': e.args[0] })

    return HttpResponse(data, content_type="application/json")
    