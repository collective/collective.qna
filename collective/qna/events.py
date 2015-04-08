def IndexParent(object, event):
    """Index object's parent
    """
    object.__parent__.reindexObject()

def DontInheritLocalRoles(object, event):
    """Turn inheritance of roles off
    """
    object.__ac_local_roles_block__ = True
    object.reindexObjectSecurity()
