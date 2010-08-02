from zope.publisher.browser import BrowserView
from zope.component import getAdapter

from Products.CMFCore.utils import getToolByName

from contentratings.interfaces import IUserRating


class RatingsMacros(BrowserView):

    def __getitem__(self, key):
        return self.index.macros[key]

    def getUserRatings(self):
        """Return the list of works submitted to the competition with
        their ratings info.
        """
        works = self.context.listFolderContents()
        return [getAdapter(w, IUserRating, name=u'competition_items_rating') for w in works]
