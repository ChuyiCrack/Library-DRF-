from rest_framework import permissions
from .permissions import SraffEditorPermission


class SraffEditorPermissionMixin(SraffEditorPermission):
    permission_classes = [permissions.IsAdminUser,SraffEditorPermission]

    def has_permission(self, request, view):
        return super().has_permission(request, view)
    
#This class will filter all the books that the user has create and will show their books that they have created
class UserQuerySetMixin():
    user_field='user'
    def get_queryset(self,*args,**kwargs):
        user = self.request.user
        lookup_data = {}
        lookup_data[self.user_field] = self.request.user     
        queryset= super().get_queryset(*args,**kwargs)     
        if user.is_staff:       #SO when you search books you can only see your own books so if the user is staff he will se all the books
            return queryset
        return queryset.filter(**lookup_data)
    
