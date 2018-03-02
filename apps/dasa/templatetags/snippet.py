
import re
from django import template

register = template.Library()


def snippet(value, length):
    value = re.sub('<.*?>', '', value)
    orig_len = len(value)
    if orig_len > 200:
        value = value[:200]
        postfix = '...'
    else:
        postfix = ''
    value = ' '.join(value.split()[:-1]) + postfix

    return value

register.filter('snippet', snippet)


def tooltip_footnotes(value, footnote_texts):
    """Given two strings, adds tooltips-anchors to footnote markers in the first string, based on footnotes in the second string

    for example:
        'text[1] about this[2]', '[1] ladida [2] some other footnote'
    becaomes
        'text<a title='ladida'>[1]</a> ...'

    """
    if not value:
        return value
    if not footnote_texts:
        return value
    for footnote_number in re.findall('[[0-9]+?]', value):
        # try to find the footnote in our tool_tip
        m_footnote_text = re.search(re.escape(footnote_number), footnote_texts)
        if m_footnote_text:
            footnote_text = footnote_texts[m_footnote_text.end():]
            footnote_text = footnote_text[:footnote_text.find('[')]
        else:
            footnote_text = footnote_texts

        value = value.replace(footnote_number, u'<a title="{footnote_text}">{footnote_number}</a>'.format(**locals()))
    return value


register.filter('tooltip_footnotes', tooltip_footnotes)
