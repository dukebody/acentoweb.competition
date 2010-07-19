import unittest

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


    def test_phoneno_exist(self):
        """Check that the Phone Number property is among the member properties.
        """
        md = self.portal.portal_memberdata
        self.failIf(md.getProperty('phone_no') is None)

    def test_skinlayers_exist(self):
        """Check that our custom skin layers are registered."""
        ps = self.portal.portal_skins
        self.failUnless('competition_templates' in ps.objectIds())


def test_suite():
    return unittest.TestSuite([
            unittest.makeSuite(TestSetup),
        ])

if __name__ == '__main__':
    unittest.main(defaultTest='test_suite')
