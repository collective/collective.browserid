====================
collective.browserid
====================

collective.browserid provides both a PAS plugin for the
`BrowserID <https://browserid.org/>`_ authentication system and
integrates it into Plone in a similar way to 
`plone.openid <http://github.com/plone/plone.openid>`_ and 
`plone.app.openid <http://github.com/plone/plone.app.openid>`_.

When installed, a new portlet is added to the site on all pages except
the login and registration forms, with the option to log in using
BrowserID. The login form is also customized to add a log in using
BrowserID tab.

BrowserID-authenticated users are not full members. Specifically they
do not get the Members role. This is done to prevent all OpenID users
from being able to see non-public content or make changes.

One can give BrowserID users extra roles through the standard Plone
user management configuration screens.

Installation
============
Add the ``collective.browserid`` egg to your buildout configuration,
and install using the portal quickinstaller.

Removal
=======
Uninstall using the portal quickinstaller.