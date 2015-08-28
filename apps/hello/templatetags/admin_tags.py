import logging
from django.core import urlresolvers
from django.contrib.contenttypes.models import ContentType
from django import template

logger = logging.getLogger(__name__)
register = template.Library()


@register.simple_tag
def admin_url(instance):
    try:
        content_type = ContentType.objects.get_for_model(instance.__class__)
        return '<div class="col-sm-1 col-lg-pull-1"><a href="'\
               + urlresolvers.reverse("admin:%s_%s_change" %
                                      (content_type.app_label,
                                       content_type.model),
                                      args=(instance.id,)) \
               + '">(Admin)</a></div>'
    except ContentType.DoesNotExist as e:
        logger.info('Attempt to get does not exist object in template tag')
        logger.error(e)
        return 'ContentType.DoesNotExist'
    except Exception as e:
        info_message = 'Something wrong when trying to get admin_url'
        logger.info(info_message)
        logger.error(e)
        return info_message
