import json
import logging
from urllib import urlencode
from urllib2 import urlopen
import urlparse

from AccessControl.SecurityInfo import ClassSecurityInfo
from Acquisition import aq_parent
from Products.CMFCore.utils import getToolByName
from Products.PageTemplates.PageTemplateFile import PageTemplateFile
from Products.PluggableAuthService.plugins.BasePlugin import BasePlugin
from Products.PluggableAuthService.utils import classImplements
from Products.PluggableAuthService.interfaces.plugins import IAuthenticationPlugin
from Products.PluggableAuthService.interfaces.plugins import IExtractionPlugin
from Products.PluggableAuthService.interfaces.plugins import IUserEnumerationPlugin

from collective.browserid.config import DEFAULT_HOST
from collective.browserid.config import DEFAULT_TIMEOUT
from collective.browserid.config import PLUGIN_META_TYPE


manage_addBrowserIdPlugin = PageTemplateFile("../www/browseridAdd", globals(), 
                __name__="manage_addBrowserIdPlugin")

logger = logging.getLogger("PluggableAuthService")


def addBrowserIdPlugin(self, id, title='', host=None, timeout=None, REQUEST=None):
    """Add a BrowserID plugin to a Pluggable Authentication Service.
    """
    p=BrowserIdPlugin(id, title)
    self._setObject(p.getId(), p)

    if REQUEST is not None:
        REQUEST["RESPONSE"].redirect("%s/manage_workspace"
                "?manage_tabs_message=BrowserID+plugin+added." %
                self.absolute_url())


class BrowserIdPlugin(BasePlugin):
    """BrowserID authentication plugin.
    """

    meta_type = PLUGIN_META_TYPE
    security = ClassSecurityInfo()

    def __init__(self, id, title=None, host=None, timeout=None):
        self._setId(id)
        self.title=title
        self._host = host or DEFAULT_HOST
        self._timeout = timeout or DEFAULT_TIMEOUT

    def getAudience(self):
        pas=self._getPAS()
        site=aq_parent(pas)
        url = site.absolute_url()
        audience = urlparse.urlunparse(list(urlparse.urlparse(url))[:2] + [''] * 4)
        return audience

    # IExtractionPlugin implementation
    def extractCredentials(self, request):
        """This method performs the PAS credential extraction.

        It takes either the zope cookie and extracts BrowserID credentials
        from it, or a redirect from an OpenID server.
        """
        creds={}
        assertion=request.form.get("__ac_browserid_assertion", None)
        if assertion is not None and assertion != "":
            data = urlencode({
                'assertion': assertion,
                'audience': self.getAudience()
                })
            resp = urlopen(self._host, data, self._timeout)
            
            creds = json.load(resp)
        
        return creds

    # IAuthenticationPlugin implementation
    def authenticateCredentials(self, credentials):
    
        if credentials['extractor'] != self.getId():
            return None
        
        if credentials.get('status') == 'okay':
            return (credentials['email'], credentials['email'])
        
        return None

    # IUserEnumerationPlugin implementation
    def enumerateUsers(self, id=None, login=None, exact_match=False,
            sort_by=None, max_results=None, **kw):
        """Slightly evil enumerator.

        This is needed to be able to get PAS to return a user which it should
        be able to handle but who can not be enumerated.

        We do this by checking for the exact kind of call the PAS getUserById
        implementation makes
        """
        if id and login and id!=login:
            return None

        if (id and not exact_match) or kw:
            return None

        key=id and id or login
        
        reg_tool = getToolByName(self, 'portal_registration')
        if not reg_tool.isValidEmail(key):
            return None

        return [ {
                    "id" : key,
                    "login" : key,
                    "pluginid" : self.getId(),
                } ]


classImplements(BrowserIdPlugin,
                IExtractionPlugin,
                IAuthenticationPlugin,
                IUserEnumerationPlugin)