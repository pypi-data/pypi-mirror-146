from django import template

register = template.Library()


@register.simple_tag(takes_context=True)
def render_block(context, block, **kwargs):
    request = context["request"]
    ctx = {"request": request}
    return block.render(request=request, context=ctx)
