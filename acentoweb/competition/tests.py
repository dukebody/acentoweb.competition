import unittest

#from zope.testing import doctestunit
#from zope.component import testing
from Testing import ZopeTestCase as ztc

from Products.Five import fiveconfigure, zcml
from Products.PloneTestCase import PloneTestCase as ptc
from Products.PloneTestCase.layer import onsetup


@onsetup
def setup_acentoweb_competition():
            fiveconfigure.debug_mode = True
            import acentoweb.competition
            zcml.load_config('configure.zcml', acentoweb.competition)
            fiveconfigure.debug_mode = False

            ztc.installPackage('acentoweb.competition')

setup_acentoweb_competition()
ptc.setupPloneSite(products=['acentoweb.competition'])


class TestWorkflow(ptc.PloneTestCase):
    def test_wf_exists(self):
        wt = self.portal.portal_workflow
        self.failUnless('competition_item_workflow' in wt.objectIds())

    def test_competitionitemwf_bindings(self):
        """Check that the Photo and Video types are binded to the
        competition_item_workflow.
        """
        wt = self.portal.portal_workflow
        self.failUnless('competition_item_workflow' in wt.getChainForPortalType('Photo'))
        self.failUnless('competition_item_workflow' in wt.getChainForPortalType('Video'))


class TestMemberData(ptc.PloneTestCase):
    def test_phoneno_present(self):
        """Check that the Phone Number property is among the member properties.
        """
        md = self.portal.portal_memberdata
        self.failIf(md.getProperty('phone_no') is None)


def test_suite():
    return unittest.TestSuite([
            unittest.makeSuite(TestWorkflow),
            unittest.makeSuite(TestMemberData),
        ])

if __name__ == '__main__':
    unittest.main(defaultTest='test_suite')
