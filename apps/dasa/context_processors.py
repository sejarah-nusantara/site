#
# copyright Gerbrandy SRL
# www.gerbrandy.com
# 2013
#

# TODO: refactor: move this logic to the view class (where also the menu etc is defined)

from dasa import models
from dasa import config


def dasa_context(request):
    context = {}

    footerlink_slugs = [
        config.SLUG_COPYRIGHT,
        config.SLUG_DISCLAIMER,
        config.SLUG_PRIVACY,
        config.SLUG_SITE_POLICY,
       ]
    footerlinks = []
    for slug in footerlink_slugs:
        try:
            footerlinks.append(models.BasicPage.objects.get(slug=slug))
        except:
            # TODO: do something with this error!
            pass

    context['footerlinks'] = footerlinks

    context.update(config.__dict__)
    return context
