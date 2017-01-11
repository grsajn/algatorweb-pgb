from django.db import models

# Create your models here.

class Entities(models.Model):
    type = models.IntegerField() #1 - projekt, #2 - algoritem, #3 - testset
    name = models.CharField(max_length=250)
    parent_id = models.ForeignKey("self", null=True, related_name="parent_entity")


#Tabela
#entitete:
#- ID
#- type(projekt, algoritem, testset)
#- name
#- parent_ID