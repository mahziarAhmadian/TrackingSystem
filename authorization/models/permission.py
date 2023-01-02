from django.db import models
from django.utils import timezone


class Permission(models.Model):
    title = models.CharField(max_length=255, unique=True)
    description = models.TextField()
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self) -> str:
        return self.title


"""

    system permissions {
    
    # TypePermissions : [AddType , EditType , DeleteType]
    
    # UserPermissions : [EditUser , GetUserDetail , DeleteUser]
    
    # ProjectPermissions :[AddProject, EditProject , DeleteProject,GetProject,GetProjectDocuments,DeleteProjectDocument]
    
    # ModulePermissions : [AddModule , EditModule, DeleteModule,GetModule]
    
    # MetePermissions : [AddMeter,GetMeter,EditMeter,DeleteMeter]
    
    # TruckPermissions : [AddTruck,GetTruck,EditTruck,DeleteTruck]
    
        }

"""
