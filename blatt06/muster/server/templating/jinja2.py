#
#
# install jinja2: pip install jinja2
#
#

from jinja2 import Environment, FileSystemLoader


class Templating:

    @classmethod
    def render(cls, path, filename, dictionary):
        templateLoader = FileSystemLoader(searchpath=path)
        templateEnv = Environment(loader=templateLoader, autoescape=True)
        template = templateEnv.get_template(filename)
        return template.render(dictionary)