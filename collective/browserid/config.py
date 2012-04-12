import socket
from AccessControl import ModuleSecurityInfo


HAS_SSL=hasattr(socket, "ssl")
del socket

security = ModuleSecurityInfo('collective.browserid.config')

security.declarePublic('DEFAULT_HOST')
DEFAULT_HOST = 'https://browserid.org/verify'
security.declarePublic('DEFAULT_TIMEOUT')
DEFAULT_TIMEOUT = 15
security.declarePublic('PLUGIN_META_TYPE')
PLUGIN_META_TYPE = "BrowserID plugin"