import sublime
import sublime_plugin
import re
import socket

try:
    # python2
    from xmlrpclib import ServerProxy
    import markdown2
except ImportError:
    # python3
    from xmlrpc.client import ServerProxy
    import os
    import sys
    abspath = os.path.abspath(os.path.dirname(__file__))
    sys.path.append(abspath)
    import markdown2


def markdown_to_html(content):
    return markdown2.markdown(content).encode('utf-8').decode()


def rst_to_html(content):
    try:
        from docutils.core import publish_string
        return publish_string(content, writer_name='html')
    except ImportError:
        error_msg = """RstPreview requires docutils to be installed for the python interpreter that Sublime uses.
    run: `sudo easy_install-2.6 docutils` and restart Sublime (if on Mac OS X or Linux). For Windows check the docs at
    https://github.com/d0ugal/RstPreview"""
        sublime.error_message(error_msg)
        raise


class MarkupJiraConfluenceCommand(sublime_plugin.TextCommand):

    def __init__(self, view):
        self.view = view
        self.markups = dict([
            ('Markdown', markdown_to_html),
            ('reStructuredText', rst_to_html),
            ('Markdown Extended', markdown_to_html)])
    def markup_to_html(self, content):
        syntax = self.view.settings().get('syntax')
        syntax = syntax.split('.')[0].split('/')[-1]
        if not syntax in self.markups:
            sublime.message_dialog('not support %s syntax yet' % syntax)
            return
        else:
            converter = self.markups[syntax]
        new_content = converter(content)
        return new_content

    def get_meta_and_content(self, contents):
        meta = dict()
        content = list()
        tmp = contents.splitlines()
        for x, entry in enumerate(tmp):
            if entry.strip():
                if re.match(r'[Ss]pace: *', entry):
                    meta['space'] = re.sub('[^:]*: *', '', entry)
                elif re.match(r'[Pp]arent Title: *', entry):
                    meta['parent_title'] = re.sub('[^:]*: *', '', entry)
                elif re.match(r'[Tt]itle: *', entry):
                    meta['title'] = re.sub('[^:]*: *', '', entry)
            else:
                content = tmp[x + 1:]
                break
        return meta, content

    def get_token(self, username, password):
        try:
            token = self.serv.confluence2.login(username, password)
            return token
        except Exception as error:
            sublime.message_dialog('Can not login Confluence')
            print(error)
            return

    def get_page_by_title(self, token, space, title):
        try:
            page = self.serv.confluence2.getPage(token, space, title)
            return page
        except:
            return

    def store_page(self, token, space, parent_title, title, content):
        parent_page = self.get_page_by_title(token, space, parent_title)
        try:
            parent_id = parent_page['id']
        except TypeError:
            sublime.message_dialog('space or parent doesn\'t exist')
            raise
        page = self.get_page_by_title(token, space, title)
        if page:
            page['parentId'] = parent_id
            page['content'] = content
        else:
            page = dict(
                content=content, parentId=parent_id, space=space, title=title)
        self.serv.confluence2.storePage(token, page)
        result = self.serv.confluence2.getPage(token, space, title)
        sublime.message_dialog(result['url'])
        return

    def run(self, edit):
        # self.get_syntax()
        region = sublime.Region(0, self.view.size())
        contents = self.view.substr(region)
        meta, content = self.get_meta_and_content(contents)
        # print('%r' % meta)
        new_content = self.markup_to_html('\n'.join(content))
        if not new_content:
            return

        settings = sublime.load_settings('MarkupJiraConfluence.sublime-settings')
        confluence_url = settings.get('confluence_url')
        username = settings.get('username')
        password = settings.get('password')
        socket.setdefaulttimeout(10)
        sublime.status_message('posting...')
        self.serv = ServerProxy(confluence_url)
        token = self.get_token(username, password)
        if not token:
            return
        space = meta.get('space')
        parent_title = meta.get('parent_title')
        title = meta.get('title')
        self.store_page(token, space, parent_title, title, new_content)
