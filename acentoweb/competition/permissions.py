# CMF and Archetypes imports
from Products.Archetypes.atapi import listTypes
from Products.CMFCore.permissions import setDefaultRoles

# Product imports
from config import PROJECTNAME

# Being generic by defining an "Add" permission
# for each content type in the product
ADD_CONTENT_PERMISSIONS = {}
types = listTypes(PROJECTNAME)
for atype in  types:
    permission = "%s: Add %s" % (PROJECTNAME, atype['portal_type'])
    ADD_CONTENT_PERMISSIONS[atype['portal_type']] = permission


# Controls access to the "sharing" page
DelegateRoles = "Sharing page: Delegate roles"
setDefaultRoles(DelegateRoles, ('Manager', 'Editor', 'Reviewer',))
