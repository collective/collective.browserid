from plone.app.layout.viewlets.common import ViewletBase


class JavascriptViewlet(ViewletBase):
    
    def index(self):
        return '<script type="text/javascript" src="https://browserid.org/include.js"></script>'