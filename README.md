#Despliega tu API en Heroku con Python

Crear cuenta en [Heroku](https://id.heroku.com/signup)

Crear la app, por ejemplo: ironhack-api-python-demo, la app estará corriendo en:

[http://ironhack-api-python-demo.herokuapp.com/](http://ironhack-api-python-demo.herokuapp.com/)
###Repositorio GIT
Nos traemos una copia del proyecto (vacío por ahora):

```
> git clone git@heroku.com:ironhack-api-python-demo.git -o heroku
```

####Requisitos
Instalamos heroku toolbelt:

```
> brew install heroku
```
Instalamos python:

```
> brew install python
```
Instalamos pip:

```
> sudo easy_install pip
```

Instalamos virtualenv:

```
> pip install virtualenv
```

Instalamos virtualenvwrapper:

```
> pip install virtualenvwrapper
```

Creamos un virtualenv (por ejemplo con el nombre *api_env*) donde estará nuestra app django:

```
> mkvirtualenv api_env
```
Para activar ese virtualenv:

```
> workon api_env
```
Instalamos django

```
> pip install django
```
Instalamos MySql para Python:

```
> pip install MySQL-python
```

Ahora vamos a instalar una serie de paquetes necearios para Heroku:

```
> pip install dj-database-url
> pip install dj-static
> pip install gunicorn
> pip install static 
```


Guardamos los requisitos para Heroku sepa lo que tiene que instalar:

```
> pip freeze > requirements.txt
```

####Creando projecto Django
Por ejemplo lo llamaré *apidemo*

```
> django-admin.py startproject apidemo .
```

Tenemos que crear un archico `Procfile` para especificar a Heroku que en la máquina va a correr una app django, lo creamos en la raiz del proyecto con este contenido:

```
web: gunicorn apidemo.wsgi
```
Y probamos arrancando la app en local:

```
> python manage.py runserver
```
Si todo ha ido bien, podrás ver el sitio corriendo en http://127.0.0.1:8000/

####Subimos a producción para probar

Subimos los cambios al repositorio:

```
> git add *
> git commit -m 'Django app created'
```
Y hacemos push en producción:

```
> git push heroku master
```
Cuando acabe podremos ver en [http://ironhack-api-python-demo.herokuapp.com/](http://ironhack-api-python-demo.herokuapp.com/) un mensaje alentador: **It worked!**

####Creamos base de datos local
Con nuestro cliente mysql, creamos una base de datos en localhost, llamada por ejemplo: `ironhack-api-demo-test`, luego creamos un usuario con permisos grant para esa base de datos. En el ejemplo el usuario será *ironhackdemo* y contraseña *ironhackdemo*.

Vamos a configurar django para que se conecte a la base de datos, abrimos */apidemo/settings.py* y editamos el contenido del diccionario DATABASES:

```
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql', 
        'NAME': 'ironhack-api-demo-test',     
        'USER': 'ironhackdemo',               
        'PASSWORD': 'ironhackdemo',               
        'HOST': '127.0.0.1',                        
        'PORT': '',                           
    }
}
```
####Creamos la app que será nuestra API
En Django los proyectos los conforman una o varias apps. Vamos a crearnos nuestra app, que se llamará por ejemplo `api`:

```
> python manage.py startapp api
```

Esto crea un nuevo directorio en nuestro proyecto, pero debemos indicarle al proyecto que incluya esta nueva app. Editamos */apidemo/settings.py* de nuevo para añadir a la lista `INSTALLED_APPS` nuestra nueva app:

```
INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'api'
)
```
####Creamos nuestros modelos
Vamos a crean el *api/models.py*  estos dos modelos, *Ironhackers* que representan a los estudiantes del IronHack y *Teams* que representa por ejemplo posibles equipos en los que agruparnos:

```
class Ironhackers(models.Model):
    name = models.CharField(default="",max_length=50)
    email = models.EmailField(max_length=100,default="")
    team = models.ForeignKey('Teams',null=True,blank=True,on_delete = models.SET_NULL)

    def __unicode__(self):
        return self.name

class Teams(models.Model):
    team = models.CharField(default="",max_length=50)
    color = models.CharField(default="",max_length=50)

    def __unicode__(self):
        return self.team
```
Una vez creados los modelos, django se encarga crear las tablas en la base de datos, con el comando:

```
> python manage.py syncdb
```

####Creamos las rutas que servirán de *endpoints* para nuestra API
Las rutas en Django se gestionan desde el archivo *urls.py*, lo abrimos y añadimos por ejemplo estas urls:

```
url(r'^ironhackers/add$', 'api.endpoints.ironhackers.add'),
url(r'^ironhackers/delete$', 'api.endpoints.ironhackers.delete'),
url(r'^ironhackers/list$', 'api.endpoints.ironhackers.list'),
url(r'^ironhackers/orphans$', 'api.endpoints.ironhackers.orphan'),
url(r'^ironhackers/link_to_team$', 'api.endpoints.ironhackers.link_to_team'),
url(r'^teams/add$', 'api.endpoints.ironhackers.add'),
url(r'^teams/delete$', 'api.endpoints.ironhackers.delete'),
url(r'^teams/list$', 'api.endpoints.ironhackers.list'),
```
O sea en este ejemplo estamos añadiendo a nuestra api los métodos `add`, `delete`, `list`, `orphans` y `link_to_team` para *ironhackers* y `add`, `delete` y `list` para *teams*.

####Implementación de los métodos

Para implementar los métodos de *ironhackers*, creamos el archivo */api/endpoints/ironhackers.py*:

**Añadir un ironhacker dados el *name* y el *email*:**

```
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

```


**Eliminar un ironhacker dado su *id*:**

```
def delete(request):
    try:
        student=Ironhackers.objects.get(id=request.POST["id"])
        student.delete()
        data=json.dumps({'status': 'success', 'response':'deleted'})
    
    except Exception as e:
        data = json.dumps({ 'status':'failed', 'response': e.args[0] })

    return HttpResponse(data, content_type="application/json")


```


**Lista de ironhackers:**

```
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


```



**Lista de ironhackers sin equipo asignado:**

```
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


```


**Vincular un ironhacker a un equipo dados el *id* del estudiante y el *id* del equipo:**

```
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
```

-------------

Para implementar los métodos de *teams*, creamos el archivo */api/endpoints/teams*:

**Añadir un equipo dados el *team* y el *color*:**

```
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

```


**Eliminar un equipo dado su *id*:**

```
def delete(request):
    try:
        team=Teams.objects.get(id=request.POST["id"])
        team.delete()
        data=json.dumps({'status': 'success', 'response':'deleted'})
    
    except Exception as e:
        data = json.dumps({ 'status':'failed', 'response': e.args[0] })

    return HttpResponse(data, content_type="application/json")

```


**Lista de equipos:**

```
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


```

Con estas implementaciones tenemos en local estos métodos de nuestra API:

[http://127.0.0.1:8000/ironhackers/add](http://127.0.0.1:8000/ironhackers/add)

[http://127.0.0.1:8000/ironhackers/delete](http://127.0.0.1:8000/ironhackers/delete)

[http://127.0.0.1:8000/ironhackers/list](http://127.0.0.1:8000/ironhackers/list)

[http://127.0.0.1:8000/ironhackers/orphans](http://127.0.0.1:8000/ironhackers/orphans)

[http://127.0.0.1:8000/ironhackers/link_to_team](http://127.0.0.1:8000/ironhackers/link_to_team)

[http://127.0.0.1:8000/teams/add](http://127.0.0.1:8000/teams/add)

[http://127.0.0.1:8000/teams/delete](http://127.0.0.1:8000/teams/delete)

[http://127.0.0.1:8000/teams/list](http://127.0.0.1:8000/teams/list)

#### Configurar la base de datos de producción
En la terminal, creamos una base de datos en producción con el comando:

```
> heroku addons:add cleardb:ignite
```
Para saber los datos de acceso de la base de datos recien creada:

```
> heroku config | grep CLEARDB_DATABASE_URL
```
Con esas credenciales, accedemos desde un cliente mysql e importamos la base de datos local. También cambiamos esas credenciales en el *settings.py* de nuestro proyecto.

###Subimos a producción

Subimos todo a producción:

```
> git add *
> git commit -m 'Django app created'
> git push heroku master
```
Si todo ha udo bien, debériamos tener estos métodos listos para ser usados:


[http://ironhack-api-python-demo-test.herokuapp.com//ironhackers/add](http://ironhack-api-python-demo-test.herokuapp.com//ironhackers/add)

[http://ironhack-api-python-demo-test.herokuapp.com//ironhackers/delete](http://ironhack-api-python-demo-test.herokuapp.com//ironhackers/delete)

[http://ironhack-api-python-demo-test.herokuapp.com//ironhackers/list](http://ironhack-api-python-demo-test.herokuapp.com//ironhackers/list)

[http://ironhack-api-python-demo-test.herokuapp.com//ironhackers/orphans](http://ironhack-api-python-demo-test.herokuapp.com//ironhackers/orphans)

[http://ironhack-api-python-demo-test.herokuapp.com//ironhackers/link_to_team](http://ironhack-api-python-demo-test.herokuapp.com//ironhackers/link_to_team)

[http://ironhack-api-python-demo-test.herokuapp.com//teams/add](http://ironhack-api-python-demo-test.herokuapp.com//teams/add)

[http://ironhack-api-python-demo-test.herokuapp.com//teams/delete](http://ironhack-api-python-demo-test.herokuapp.com//teams/delete)

[http://ironhack-api-python-demo-test.herokuapp.com//teams/list](http://ironhack-api-python-demo-test.herokuapp.com//teams/list)

Para probar, podéis usar [http://www.hurl.it/](http://www.hurl.it/)
