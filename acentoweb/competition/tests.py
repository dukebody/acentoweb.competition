import unittest
from zope.testing import doctest

from Testing import ZopeTestCase as ztc

from Products.Five import fiveconfigure, zcml
from Products.Five.testbrowser import Browser
from Products.PloneTestCase import PloneTestCase as ptc
from Products.PloneTestCase.layer import onsetup

from Products.CMFCore.utils import getToolByName


def createUser(site, username, fullname=None, email=None, passwd=None):
    """
    Utility function which performs the actual creation, role and permission magic.
    """

    # portal_registrations manages new user creation
    regtool = getToolByName(site, 'portal_registration')

    # Default password to the username
    # ... don't do this on the production server!
    if passwd == None:
        passwd = username

    if fullname == None:
        fullname = username

    if email == None:
        email = username + '@domain.tld'

    # Only lowercase allowed
    username = username.lower()

    username = str(username)

    # This is minimum required information set
    # to create a working member
    properties = {
        'username' : username,
        # Full name must be always as utf-8 encoded
        'fullname' : fullname.encode("utf-8"),
        'email' : email,
    }

    regtool.addMember(username, passwd, properties=properties)


@onsetup
def setup_acentoweb_competition():
            fiveconfigure.debug_mode = True
            import acentoweb.competition
            zcml.load_config('configure.zcml', acentoweb.competition)
            fiveconfigure.debug_mode = False

            ztc.installPackage('acentoweb.competition')

setup_acentoweb_competition()
ptc.setupPloneSite(products=['acentoweb.competition'])


class TestSetup(ptc.PloneTestCase):
    def test_wf_exists(self):
        """Check that our custom workflows are present.
        """
        wt = self.portal.portal_workflow
        self.failUnless('competition_item_workflow' in wt.objectIds())
        self.failUnless('competition_workflow' in wt.objectIds())


    def test_competitionwf_bindings(self):
        """Check that the Competition types is binded to the
        competition_workflow.
        """
        wt = self.portal.portal_workflow
        self.failUnless('competition_workflow' in wt.getChainForPortalType('Competition'))


    def test_competitionitemwf_bindings(self):
        """Check that the Photo and Video types are binded to the
        competition_item_workflow.
        """
        wt = self.portal.portal_workflow
        self.failUnless('competition_item_workflow' in wt.getChainForPortalType('Photo'))
        self.failUnless('competition_item_workflow' in wt.getChainForPortalType('Video'))
        self.failUnless('competition_item_workflow' in wt.getChainForPortalType('Story'))


    def test_phoneno_exist(self):
        """Check that the Phone Number property is among the member properties.
        """
        md = self.portal.portal_memberdata
        self.failIf(md.getProperty('phone_no') is None)

    def test_skinlayers_exist(self):
        """Check that our custom skin layers are registered."""
        ps = self.portal.portal_skins
        self.failUnless('competition_templates' in ps.objectIds())


OPTIONFLAGS = (doctest.ELLIPSIS |
               doctest.NORMALIZE_WHITESPACE)

class CompetitionFunctionalTestCase(ptc.FunctionalTestCase):
    """Base class for functional test cases..
    """

    def afterSetUp(self):
        """
        Show errors in console by monkey patching site error_log service
        """

        ptc.FunctionalTestCase.afterSetUp(self)

        self.browser = Browser()
        self.browser.handleErrors = False # Don't get HTTP 500 pages


        self.portal.error_log._ignored_exceptions = ()

        def raising(self, info):
            import traceback
            traceback.print_tb(info[2])
            print info[1]

        from Products.SiteErrorLog.SiteErrorLog import SiteErrorLog
        SiteErrorLog.raising = raising

        # create competitors
        for i in range(1,3):
            createUser(self.portal, 'competitor%s' % i)

        createUser(self.portal, 'judge')


    def loginAsAdmin(self):
        """ Perform through-the-web login as admin.

        Simulate going to the login form and logging in.
        """
        from Products.PloneTestCase.setup import portal_owner, default_password

        # Go admin
        browser = self.browser
        browser.open(self.portal.absolute_url() + "/logout")
        browser.open(self.portal.absolute_url() + "/login_form")
        browser.getControl(name='__ac_name').value = portal_owner
        browser.getControl(name='__ac_password').value = default_password
        browser.getControl(name='submit').click()

    def loginAsUser(self, username):
        """ Perform through-the-web login as an user.

        Simulate going to the login form and logging in as the selected
        user.
        """
        browser = self.browser
        browser.open(self.portal.absolute_url() + "/logout")
        browser.open(self.portal.absolute_url() + "/login_form")
        browser.getControl(name='__ac_name').value = username
        browser.getControl(name='__ac_password').value = username
        browser.getControl(name='submit').click()

def test_suite():
    return unittest.TestSuite([
        unittest.makeSuite(TestSetup),
        ztc.FunctionalDocFileSuite('functional.txt',
                               optionflags=OPTIONFLAGS,
                               test_class=CompetitionFunctionalTestCase
                               )
        ])

if __name__ == '__main__':
    unittest.main(defaultTest='test_suite')
