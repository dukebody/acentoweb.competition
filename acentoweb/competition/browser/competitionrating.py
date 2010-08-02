from contentratings.browser.basic import BasicUserRatingView


class RatingView(BasicUserRatingView):
    """Rating view for the competition rating.

    The can_read method allows using the can_read manager @property
    from TALES.
    """

    def can_read(self):
        manager = self.context
        return manager.can_read
