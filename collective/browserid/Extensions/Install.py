# This file exists so that Quickinstaller picks the correct profile for install
# and runs the uninstall profile when the product is uninstalled. There is
# currently no mechanism for it to autodetect an uninstall profile.

from Products.CMFCore.utils import getToolByName


def install(portal, reinstall=False):
    setup_tool = getToolByName(portal, 'portal_setup')
    setup_tool.runAllImportStepsFromProfile('profile-collective.browserid:default')
    return "Ran all uninstall steps."


def uninstall(portal, reinstall=False):
    setup_tool = getToolByName(portal, 'portal_setup')
    setup_tool.runAllImportStepsFromProfile('profile-collective.browserid:uninstall')
    return "Ran all uninstall steps."