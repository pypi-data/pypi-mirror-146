from cms.plugin_base import CMSPluginBase
from cms.plugin_pool import plugin_pool

from .models import Education


class PositionObject(CMSPluginBase):
    name = "Education"
    render_template = "djangocms_education/list_template.html"
    model = Education
    allow_children = True

    def render(self, context, instance, placeholder):
        context['instance'] = instance
        return context


plugin_pool.register_plugin(PositionObject)
