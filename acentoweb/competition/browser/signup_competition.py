from AccessControl import Unauthorized
from Products.Five.browser import BrowserView

from Products.CMFPlone import PloneMessageFactory as _
from Products.CMFCore.utils  import getToolByName


class SignUp(BrowserView):
    def __call__(self):

        form = self.request.form
        signup_button = form.get('form.button.signup', None) is not None

        if signup_button:

            # security checks
            if not self.request.get('REQUEST_METHOD','GET') == 'POST':
                raise Unauthorized

            authenticator = self.context.restrictedTraverse('@@authenticator', None) 
            if not authenticator.verify():
                raise Unauthorized

            mt = getToolByName(self.context, 'portal_membership')
            member = mt.getAuthenticatedMember()
            userid = member.getId()

            if 'Competitor' not in self.context.get_local_roles_for_userid(userid):
                self.context.manage_setLocalRoles(userid, ['Competitor',])

                self.context.plone_utils.addPortalMessage(_(u"You've just signed up in the competition!"))

            else:
                self.context.plone_utils.addPortalMessage(_(u"You've already signed up in the competition!"))

        return self.request.RESPONSE.redirect(self.context.absolute_url())
