from string import Template


class Templating:

    @classmethod
    def render(cls, path, filename, dictionary):
        with open(path+'/'+filename, "r", encoding="utf-8") as file:
            templ = file.read()
            return Template(templ).safe_substitute(**dictionary)