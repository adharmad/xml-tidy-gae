import os
from xml.dom import minidom
from xml.parsers.expat import ExpatError

from google.appengine.ext.webapp import template
from google.appengine.api import users
from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app

class MainPage(webapp.RequestHandler):
    def get(self):
        if users.get_current_user():
            url = users.create_logout_url(self.request.uri)
            url_linktext = 'Logout'
        else:
            url = users.create_login_url(self.request.uri)
            url_linktext = 'Login'

        template_values = { }
        path = os.path.join(os.path.dirname(__file__), 'index.html')
        self.response.out.write(template.render(path, template_values))

    def post(self):
        untidyxml = self.request.get('untidyxml')
        tidyxml = format(untidyxml)

        template_values = { 
            'untidyxml' : htmlEncode(untidyxml),
            'tidyxml' : htmlEncode(tidyxml)
        }
        
        path = os.path.join(os.path.dirname(__file__), 'index.html')
        self.response.out.write(template.render(path, template_values))

def htmlEncode(s):
    s = s.replace('&', '&amp;')
    s = s.replace('<', '&lt;')
    s = s.replace('>', '&gt;')
    s = s.replace('"', '&quot;')
    return s

def format(buf):
    buf1 = unicode(buf).encode("UTF-8")
    try:
        xmldoc = minidom.parseString(buf1)
    except ExpatError, e:
        return 'XML Formatting error', e
    pretty_xml_as_string = xmldoc.toprettyxml(indent='  ')
    return pretty_xml_as_string

application = webapp.WSGIApplication(
                                     [('/', MainPage)],
                                     debug=True)

def main():
    run_wsgi_app(application)

if __name__ == "__main__":
    main()

