from rest_framework import permissions

class SraffEditorPermission(permissions.DjangoModelPermissions):
    perms_map = {
        'GET': ['%(app_label)s.view_%(model_name)s'],  #Just adding this list and modifing like this if the staff doesn not have permission to see the Books they wont be able to see the the books with the get http
        'OPTIONS': [],     #And to handle to only the staff is allowed to send get method we add to the permissions_class the permissions.IsAdminUser
        'HEAD': [],
        'POST': ['%(app_label)s.add_%(model_name)s'],
        'PUT': ['%(app_label)s.change_%(model_name)s'],
        'PATCH': ['%(app_label)s.change_%(model_name)s'],
        'DELETE': ['%(app_label)s.delete_%(model_name)s'],
    }

    
    #I rechange this class so i made some modifications in mixins.py the reason is for simplifying when it comes to calling it so i add the isadmin so when i call the SraffEditorPermissionMixin it will cal the isadmin too