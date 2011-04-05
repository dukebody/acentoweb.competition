from Acquisition import aq_inner, aq_parent
from Products.CMFCore.utils import getToolByName

from zope.interface import implements
from zope.app.interface import queryType

from plone.contentratings.category import PloneRatingCategoryAdapter
from contentratings.interfaces import IRatingManager, IRatingType


class RatingManager(PloneRatingCategoryAdapter):
    implements(IRatingManager)

    def __init__(self, category, context):
        super(RatingManager, self).__init__(category, context)

        self.mtool = getToolByName(self.context, 'portal_membership')
        self.wftool = getToolByName(self.context, 'portal_workflow')
        self.competition = aq_parent(aq_inner(self.context))
        self.competition_wf_state = self.wftool.getStatusOf('competition_workflow', self.competition)['review_state']

    @property
    def can_write(self):
        """True if the current user can rate the object.
        """
        # no more ratings if the competition is closed
        if self.competition_wf_state == 'closed':
            return False

        if not self.mtool.checkPermission('Review portal content', self.context):
            return False

        return True

    @property
    def can_read(self):
        """True if the current user can see the existing ratings.
        """
        # ratings are public if the competition is closed
        if self.competition_wf_state == 'closed':
            return True

        member = self.mtool.getAuthenticatedMember()
        userid = member.getId()
        can_modify = self.mtool.checkPermission('Modify portal content', self.context)
        is_owner = 'Owner' in self.context.get_local_roles_for_userid(userid)
        return can_modify and not is_owner

    def remove_rating(self, username):
        """Remove the rating for a given user, checking that the
        user can write first."""
        assert self.can_write
        self.storage.remove_rating(username)

    # Default method without security check
    def __getattr__(self, name):
        """If name is part of our storage interface, return the
        attribute from the storage, checking the read_expr first.
        """
        rating_type = queryType(self, IRatingType)
        # make sure it works even if the rating type isn't set yet
        if rating_type and name in rating_type.names(True):
            return getattr(self.storage, name)
        else:
            raise AttributeError, name
