from django.contrib.auth.models import User
from django.contrib.auth.backends import RemoteUserBackend


class UWRemoteUserBackend(RemoteUserBackend):
    """
    Checks for the $REMOTE_USER var and if it exists, trusts the user was
    authenticated successfully. If the user is successfully authenticated,
    but doesn't exist it will be created and added to the "Everyone" group,
    to get some default permissions.
    """
    RemoteUserBackend.create_unknown_user = False

    #def configure_user(self, user):
    #    """
    #    Gives the user some default permissions.
    #    """
    #    everyone = Group.objects.get_or_create('Everyone')
    #    user.groups.add(everyone)
    #    return user
