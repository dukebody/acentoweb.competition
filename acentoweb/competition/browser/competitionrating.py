from contentratings.browser.basic import BasicUserRatingView
from Products.CMFCore.utils import getToolByName


class RatingView(BasicUserRatingView):
    """Rating view for the competition rating.

    This is a workaround to make the view/write ratings permissions
    work properly, since the contentratings' read_expr and write_expr
    checks implementation appears broken.
    """

    @property
    def can_rate(self):
        manager = self.context
        context = manager.context
        mt = getToolByName(context, 'portal_membership')
        if not mt.checkPermission('Review portal content', context):
            return False
        return super(RatingView, self).can_rate

    @property
    def can_read(self):
        manager = self.context
        context = manager.context
        mt = getToolByName(context, 'portal_membership')
        member = mt.getAuthenticatedMember()
        userid = member.getId()
        can_modify = mt.checkPermission('Modify portal content', context)
        is_owner = 'Owner' in context.get_local_roles_for_userid(userid)
        return can_modify and manager.can_read and not is_owner
