from plone.portlets.interfaces import IPortletDataProvider
from plone.app.portlets.portlets import base
from Products.CMFCore.utils import getToolByName
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from zope.component import getMultiAdapter
from zope.interface import implements

from collective.browserid.plugins.browserid import BrowserIdPlugin
from collective.browserid import _


class ILoginPortlet(IPortletDataProvider):
    """A portlet which can render an OpenID login form.
    """


class Assignment(base.Assignment):
    implements(ILoginPortlet)

    title = _(u'BrowserID login')


class Renderer(base.Renderer):

    def __init__(self, context, request, view, manager, data):
        base.Renderer.__init__(self, context, request, view, manager, data)

        self.portal_state = getMultiAdapter((context, request), name=u'plone_portal_state')
        self.acl = getToolByName(context, "acl_users")

    @property
    def available(self):
        if not self.portal_state.anonymous():
            return False
        if not self.acl.objectIds(BrowserIdPlugin.meta_type):
            return False
        page = self.request.get('URL', '').split('/')[-1]
        return page not in ('login_form', '@@register')

    def login_form(self):
        return '%s/login_form' % self.portal_state.portal_url()


    render = ViewPageTemplateFile('login.pt')


class AddForm(base.NullAddForm):

    def create(self):
        return Assignment()
