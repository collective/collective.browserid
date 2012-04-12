import logging

from AccessControl.Permissions import manage_users as ManageUsers
from Products.PluggableAuthService.PluggableAuthService import registerMultiPlugin
from zope.i18nmessageid import MessageFactory

from collective.browserid import config

_ = CollectiveBrowserIdMessageFactory = MessageFactory('collective.browserid')


if not config.HAS_SSL:
    logger=logging.getLogger("Plone")
    logger.info("Python does not have SSL support. BrowserID support not available")
else:
    from collective.browserid.plugins import browserid
    registerMultiPlugin(browserid.BrowserIdPlugin.meta_type)



def initialize(context):
    if config.HAS_SSL:
        context.registerClass(browserid.BrowserIdPlugin,
                                permission=ManageUsers,
                                constructors=
                                        (browserid.manage_addBrowserIdPlugin,
                                         browserid.addBrowserIdPlugin),
                                visibility=None,
                                icon="www/browserid.gif")

