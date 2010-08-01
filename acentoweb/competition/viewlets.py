from AccessControl import getSecurityManager
from plone.app.layout.viewlets.content import DocumentBylineViewlet as PloneDocumentBylineViewlet
from plone.memoize.instance import memoize

class DocumentBylineViewlet(PloneDocumentBylineViewlet):
    @memoize
    def show(self):
        if not getSecurityManager().checkPermission('Modify portal content', self.context):
            return False
        return super(DocumentBylineViewlet, self).show()
