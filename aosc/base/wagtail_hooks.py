import wagtail.admin.rich_text.editors.draftail.features as draftail_features
from wagtail.admin.rich_text.converters.html_to_contentstate import InlineStyleElementHandler, BlockElementHandler

from wagtail.contrib.modeladmin.options import (
    ModelAdmin, ModelAdminGroup, modeladmin_register)

from aosc.projects.models import Segments
from aosc.base.models import People, FooterText

from wagtail.core import hooks

'''
N.B. To see what icons are available for use in Wagtail menus and StreamField block types,
enable the styleguide in settings:

INSTALLED_APPS = (
   ...
   'wagtail.contrib.styleguide',
   ...
)

or see http://kave.github.io/general/2015/12/06/wagtail-streamfield-icons.html

This demo project includes the full font-awesome set via CDN in base.html, so the entire
font-awesome icon set is available to you. Options are at http://fontawesome.io/icons/.
'''


class ProjectSegmentAdmin(ModelAdmin):
    # These stub classes allow us to put various models into the custom "Wagtail Bakery" menu item
    # rather than under the default Snippets section.
    model = Segments
    menu_icon = 'fa-suitcase'
    search_fields = ('name', )


class PeopleModelAdmin(ModelAdmin):
    model = People
    menu_label = 'People'  # ditch this to use verbose_name_plural from model
    menu_icon = 'fa-users'  # change as required
    list_display = ('first_name', 'last_name', 'job_title', 'thumb_image')
    list_filter = ('job_title', )
    search_fields = ('first_name', 'last_name', 'job_title')


class FooterTextAdmin(ModelAdmin):
    model = FooterText
    search_fields = ('body',)


class BakeryModelAdminGroup(ModelAdminGroup):
    menu_label = 'Bakery Misc'
    menu_icon = 'fa-cutlery'  # change as required
      # will put in 4th place (000 being 1st, 100 2nd)
    items = (PeopleModelAdmin, FooterTextAdmin)


# When using a ModelAdminGroup class to group several ModelAdmin classes together,
# you only need to register the ModelAdminGroup class with Wagtail:
modeladmin_register(ProjectSegmentAdmin)
#modeladmin_register(BreadModelAdminGroup)
#modeladmin_register(BakeryModelAdminGroup)


@hooks.register('register_rich_text_features')
def register_blockquote_feature(features):
    """
    Registering the `blockquote` feature, which uses the `blockquote` Draft.js block type,
    and is stored as HTML with a `<blockquote>` tag.
    """
    feature_name = 'blockquote'
    type_ = 'blockquote'
    tag = 'blockquote'

    control = {
        'type': type_,
        'label': '❝',
        'description': 'Quote',
        'element': 'blockquote',
    }

    features.register_editor_plugin(
        'draftail',
        feature_name,
        draftail_features.BlockFeature(control)
    )

    features.register_converter_rule(
        'contentstate',
        feature_name,
        {
            'from_database_format': {tag: BlockElementHandler(type_)},
            'to_database_format': {'block_map': {type_: tag}},
        }
    )
    features.default_features.append(feature_name)


@hooks.register('register_rich_text_features')
def register_codeline_feature(features):
    feature_name = 'Code Line'
    type_ = 'CODE'
    tag = 'code'

    control = {
        'type': type_,
        'label': '>_',
        'description': 'Code Line',
    }

    features.register_editor_plugin(
        'draftail', feature_name, draftail_features.InlineStyleFeature(control)
    )

    db_conversion = {
        'from_database_format': {tag: InlineStyleElementHandler(type_)},
        'to_database_format': {'style_map': {type_: tag}},
    }

    features.register_converter_rule('contentstate', feature_name, db_conversion)
    features.default_features.append(feature_name)