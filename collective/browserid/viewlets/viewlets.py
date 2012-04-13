from plone.app.layout.viewlets.common import ViewletBase


class JavascriptViewlet(ViewletBase):
    
    def index(self):
        if getattr(self.context, 'hasBrowserIdExtractor', lambda: False)():
            return '<script type="text/javascript" src="https://browserid.org/include.js"></script>'
        
        return ''