from zope.publisher.browser import BrowserView
from zope.component import getAdapter

from contentratings.interfaces import IUserRating


class Results(BrowserView):

    def __getitem__(self, key):
        return self.index.macros[key]

    def getUserRatings(self):
        """Return the list of works submitted to the competition with
        their ratings info.
        """
        works = self.context.getFolderContents(contentFilter={'review_state':'published'}, full_objects=True)
        return sorted([getAdapter(w, IUserRating, name=u'competition_items_rating') for w in works], cmp=lambda x, y: cmp(x.averageRating, y.averageRating) , reverse=True)
