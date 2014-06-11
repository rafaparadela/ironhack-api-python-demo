# -*- coding: utf-8 -*-

from django.http import HttpResponse
import json
from api.models import *


def add(request):
    try:
        student=Ironhackers()
        student.name=request.POST['name']
        student.email=request.POST['email']
        student.save()
        data=json.dumps({'status': 'success', 'response':'added', 'data':{'id':student.id}})
    
    except Exception as e:
        data = json.dumps({ 'status':'failed', 'response': e.args[0] })

    return HttpResponse(data, content_type="application/json")
    
    
def delete(request):
    try:
        student=Ironhackers.objects.get(id=request.POST["id"])
        student.delete()
        data=json.dumps({'status': 'success', 'response':'deleted'})
    
    except Exception as e:
        data = json.dumps({ 'status':'failed', 'response': e.args[0] })

    return HttpResponse(data, content_type="application/json")
    
    
def list(request):
    try:
        students=Ironhackers.objects.all()
        
        list_students=[]
        for student in students:
            list_students.append({'id':student.id, 'name':student.name, 'email':student.email })
        
        data=json.dumps({'status': 'success', 'response':'list', 'data': list_students });
    
    except Exception as e:
        data = json.dumps({ 'status':'failed', 'response': e.args[0] })

    return HttpResponse(data, content_type="application/json")
    
    
def orphans(request):
    try:
        students=Ironhackers.objects.filter(team__isnull=True)
        
        list_students=[]
        for student in students:
            list_students.append({'id':student.id, 'name':student.name, 'email':student.email })
        
        data=json.dumps({'status': 'success', 'response':'orphans', 'data': list_students });
    
    except Exception as e:
        data = json.dumps({ 'status':'failed', 'response': e.args[0] })

    return HttpResponse(data, content_type="application/json")
    

def link_to_team(request):
    try:
        student=Ironhackers.objects.get(id=request.POST["student_id"])
        team = Teams.objects.get(id=request.POST["team_id"])
        student.team = team
        student.save()
        
        data=json.dumps({'status': 'success', 'response':'linked'})
    
    except Exception as e:
        data = json.dumps({ 'status':'failed', 'response': e.args[0] })

    return HttpResponse(data, content_type="application/json")
    
    
    
    