#
#
# install pystache: pip install pystache2
#
#
import pystache


class Templating:

    @classmethod
    def render(cls, path, filename, dictionary):
        with open(path+'/'+filename, "r", encoding='utf-8') as file:
            templ = file.read()
            renderer = pystache.Renderer(search_dirs=[path])
            return renderer.render(templ, dictionary)
