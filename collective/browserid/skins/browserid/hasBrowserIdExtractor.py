## Script (Python) "hasBrowserIdExtractor"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind subpath=traverse_subpath
##parameters=openid_url=""
##title=Does the current site have a BrowserID extractor plugin? 
##

from Products.CMFCore.utils import getToolByName

from collective.browserid.config import PLUGIN_META_TYPE

acl=getToolByName(context, "acl_users")
return bool(acl.objectIds(PLUGIN_META_TYPE))