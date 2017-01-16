#Prompt: create a set of classes to render html pages 

#Step 1
class Element(object):
    tag = ''
    indent = '    '

    def __init__(self, content=None, **kwargs):
        '''constructor'''
        if content is None:
            self.content = []
        else:
            self.content = [content]
        self.args_dict = kwargs

    def append(self, new_content):
        '''add another string to the content'''
        return self.content.append(new_content)

    def render(self, file_out, indent=''):
        '''render tag and strings in the content'''
        file_out.write("\n{}<{}".format(indent, self.tag))
        if len(self.args_dict) > 0:
            for name, value in self.args_dict.items():
                file_out.write(' {}="{}"'.format(name, value))
            file_out.write(">")
        else:
            file_out.write(">")
        for item in self.content:
            try:
                item.render(file_out, self.indent + indent)
            except:
                file_out.write("\n{}{}".format(self.indent + indent, item))
        file_out.write("\n{}</{}>".format(indent, self.tag))

#Step 2 & 8
class Html(Element):
    tag = 'html'
    def render(self, file_out, indent=''):
        file_out.write("<{} {}>".format("!DOCTYPE", self.tag))
        super().render(file_out, indent='')

class Body(Element):
    tag = 'body'

class P(Element):
    tag = 'p'

#Step 3 & 8
class Head(Element):
    tag = 'head'

class OneLineTag(Element):
    def render(self, file_out, indent=''):
        file_out.write("\n{}<{}".format(indent, self.tag))
        if len(self.args_dict) > 0:
            for name, value in self.args_dict.items():
                file_out.write(' {}="{}"'.format(name, value))
            file_out.write(">")
        else:
            file_out.write(">")
        for item in self.content:
            try:
                item.render(file_out, self.indent + indent)
            except:
                file_out.write("{}".format(item))
        file_out.write("</{}>".format(self.tag))

class Title(OneLineTag):
    tag = 'title'

#Step 5 & 8
class SelfClosingTag(Element):
    def render(self, file_out, indent=''):
        file_out.write("\n{}<{}".format(indent, self.tag))
        if len(self.args_dict) > 0:
            for name, value in self.args_dict.items():
                file_out.write(' {}="{}"'.format(name, value))
        file_out.write(" />")

class Hr(SelfClosingTag):
    tag = 'hr'

class Br(SelfClosingTag):
    tag = 'br'

class Meta(SelfClosingTag):
    tag = 'meta'

#Step 6
class A(OneLineTag):
    tag = 'a'
    def __init__(self, link, content=None):
        self.link = link
        super().__init__(content, href=link)

#Step 7
class Ul(Element):
    tag = 'ul'

class Li(Element):
    tag = 'li'

class H(OneLineTag):
    def __init__(self, level, content=None):
        self.tag = 'h' + str(level)
        super().__init__(content)