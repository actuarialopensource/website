from django import template

register = template.Library()

@register.inclusion_tag('tags/disqus.html', takes_context=True)
def show_comments(context):
    page = context['page']

    return {'disqus_url': page.full_url,
            'disqus_identifier': page.url,
            'request': context['request']}