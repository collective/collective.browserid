from Testing import ZopeTestCase
from plone.session.tests.sessioncase import PloneSessionTestCase

from collective.browserid.plugins.browserid import BrowserIdPlugin
from collective.browserid.tests.layer import PloneBrowserId


class BrowserIdTestCase(PloneSessionTestCase):

    layer = PloneBrowserId

    def afterSetUp(self):
        PloneSessionTestCase.afterSetUp(self)
        self.app.folder = self.folder

        if self.folder.pas.hasObject("browserid"):
            self.app.folder.pas._delObject("browserid")

        self.app.folder.pas._setObject("browserid", BrowserIdPlugin("browserid"))

class FunctionalBrowserIdTestCase(ZopeTestCase.Functional, BrowserIdTestCase):
    pass
