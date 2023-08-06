from typing import Dict
from django.conf import settings
from django.template import Library, Node, NodeList, TemplateSyntaxError

register = Library()


class IfAppNode(Node):
    child_nodelists = ("nodelist_true", "nodelist_false")

    def __init__(
        self, app_name: str, nodelist_true: NodeList, nodelist_false: NodeList
    ):
        self.app_name = app_name  # type: str
        self.nodes = {
            True: nodelist_true,
            False: nodelist_false,
        }  # type: Dict[bool, NodeList]

    def __repr__(self):
        return "<IfAppNode>"

    def render(self, context):
        app_present = self.app_name in settings.INSTALLED_APPS
        return self.nodes[app_present].render(context)


def do_hasapp(parser, token, reverse: bool = False):
    """
    Parse the contents between {% ifapp %} and {% endifapp %} tags
    to a Node for rendering

    Use case: to set site-specific code based on the identification of a specific
    app in settings

    /* {% ifapp dird_templates %} */
    {name:'review', title:'Comments'}
    /* {% else %} */
    {name:'review', title:'{{ review_title|escapejs }}'}
    /* {% endifapp %} */

    """

    bits = list(token.split_contents())
    if len(bits) != 2:
        raise TemplateSyntaxError("%r takes one argument" % bits[0])
    end_tag = "end" + bits[0]
    nodelist_true = parser.parse(("else", end_tag))
    token = parser.next_token()
    if token.contents == "else":
        nodelist_false = parser.parse((end_tag,))
        parser.delete_first_token()
    else:
        nodelist_false = NodeList()
    app_name = parser.compile_filter(bits[1])
    if reverse:
        nodelist_true, nodelist_false = nodelist_false, nodelist_true
    return IfAppNode(app_name.token, nodelist_true, nodelist_false)


class IfSettingNode(Node):
    child_nodelists = ("nodelist_true", "nodelist_false")

    def __init__(self, thesetting, nodelist_true, nodelist_false, negate):
        self.thesetting = thesetting.token
        self.nodelist_true, self.nodelist_false = nodelist_true, nodelist_false
        self.negate = negate

    def __repr__(self):
        return "<IfSettingNode>"

    def render(self, context):
        thesetting_bool = bool(getattr(settings, self.thesetting, False))
        if (self.negate and not thesetting_bool) or (
            not self.negate and thesetting_bool
        ):
            return self.nodelist_true.render(context)
        return self.nodelist_false.render(context)


def do_ifsetting(parser, token, negate):
    bits = list(token.split_contents())
    if len(bits) != 2:
        raise TemplateSyntaxError("%r takes one argument" % bits[0])
    end_tag = "end" + bits[0]
    nodelist_true = parser.parse(("else", end_tag))
    token = parser.next_token()
    if token.contents == "else":
        nodelist_false = parser.parse((end_tag,))
        parser.delete_first_token()
    else:
        nodelist_false = NodeList()
    thesetting = parser.compile_filter(bits[1])
    return IfSettingNode(thesetting, nodelist_true, nodelist_false, negate)


@register.tag
def ifsetting(parser, token):
    """
    Outputs the contents of the block if settings.TOKEN.
    """
    return do_ifsetting(parser, token, False)


@register.tag
def ifnotsetting(parser, token):
    """
    Outputs the contents of the block if not settings.TOKEN.
    """
    return do_ifsetting(parser, token, True)


@register.tag
def ifapp(parser, token):
    """
    Render the nodes within the block when a given app is installed
    """
    return do_hasapp(parser, token)


@register.tag
def ifnotapp(parser, token):
    """
    Render the nodes within the block when a given app is not installed
    """
    return do_hasapp(parser, token, True)
