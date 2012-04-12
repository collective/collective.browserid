from StringIO import StringIO
from Products.CMFCore.utils import getToolByName

from collective.browserid.config import PLUGIN_META_TYPE


def hasBrowserIdPlugin(portal):
    acl=getToolByName(portal, "acl_users")
    return bool(acl.objectIds(PLUGIN_META_TYPE))


def createBrowserIdPlugin(portal, out):
    print >>out, "Adding a BrowserId plugin"
    acl=getToolByName(portal, "acl_users")
    acl.manage_addProduct["collective.browserid"].addBrowserIdPlugin(
            id="browserid", title="BrowserId authentication plugin")


def removeBrowserIdPlugins(portal, out):
    print >>out, "Adding a BrowserId plugin"
    acl=getToolByName(portal, "acl_users")
    browserid_pas = acl.objectIds(PLUGIN_META_TYPE)
    for id_ in browserid_pas:
        acl._delObject(id_)


def activatePlugin(portal, out, plugin):
    acl=getToolByName(portal, "acl_users")
    plugin=getattr(acl, plugin)
    interfaces=plugin.listInterfaces()

    activate=[]

    for info in acl.plugins.listPluginTypeInfo():
        interface=info["interface"]
        interface_name=info["id"]
        if plugin.testImplements(interface):
            activate.append(interface_name)
            print >>out, "Activating interface %s for plugin %s" % \
                    (interface_name, info["title"])

    plugin.manage_activateInterfaces(activate)


def deactivatePlugins(portal, out, plugin_meta_type):
    acl=getToolByName(portal, "acl_users")
    for plugin in acl.objectValues(plugin_meta_type):
        plugin=getattr(acl, plugin)
        for info in acl.plugins.listPluginTypeInfo():
            interface=info["interface"]
            interface_name=info["id"]
            if plugin.testImplements(interface):
                print >>out, "Deactivating interface %s for plugin %s" % \
                        (interface_name, info["title"])
    
        plugin.manage_activateInterfaces([])


def installVarious(context):
    # Only run step if a flag file is present (e.g. not an extension profile)
    if context.readDataFile('browserid.txt') is None:
        return

    site = context.getSite()
    out = StringIO()
    if not hasBrowserIdPlugin(site):
        createBrowserIdPlugin(site, out)
        activatePlugin(site, out, "browserid")


def uninstallVarious(context):
    # Only run step if a flag file is present (e.g. not an extension profile)
    if context.readDataFile('browserid-uninstall.txt') is None:
        return

    site = context.getSite()
    out = StringIO()
    if hasBrowserIdPlugin(site):
        deactivatePlugins(site, out, PLUGIN_META_TYPE)
        removeBrowserIdPlugins(site, out)