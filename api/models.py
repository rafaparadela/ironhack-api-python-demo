from django.db import models

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
