from server.webserver import Webserver, App, Cookie
from server.apps.static import StaticApp


class SkelApp(App):
    """Skeleton app that demonstrates some basic features for templating."""

    def register_routes(self):
        self.add_route("", self.index)
        self.add_route("page2/", self.page2)
        self.add_route("page3/", self.page3)

    def index(self,request, response, pathmatch):
        """The index page."""

        response.send_template('index.tmpl', {
            'title': 'Index',
            'current_user': {'id': 815, 'icon': '&#9752;', 'name': 'Tobias Findeisen'},
            'index': True })

    def page2(self,request, response, pathmatch):
        """The second page."""

        response.send_template('page2.tmpl', {
            'title': 'Page 2',
            'page2':True,
            'magic_number': 42,
            'current_user': {'id': 815, 'icon': '&#9752;', 'name': 'Tobias Findeisen'},
            'author': {'id':42, 'icon':'&#9730;', 'name':'Walter Sparbier'}})

    def page3(self,request, response, pathmatch):
        """The third page."""

        response.send_template('page3.tmpl', {
            'title': 'Page 3',
            'page3': True,
            'magic_numbers': [7,13,23,27,42],
            'current_user': {'id': 815, 'icon': '&#9752;', 'name': 'Tobias Findeisen'},
            'message': "<i>HTML-Content  &#x2603;</i>"
        })


        
if __name__ == '__main__':
    s = Webserver()
    s.set_templating("pystache")
    s.set_templating_path("templates.mustache/skel")
    s.add_app(SkelApp())
    s.add_app(StaticApp(prefix='static', path='static'))

    s.serve()

