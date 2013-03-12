# -*- coding: utf-8 -*-

from Acquisition import aq_inner
from Acquisition import aq_parent
from jornada.contenttypes.article import IArticle
from five import grok
from Products.CMFPlone.interfaces import IPloneSiteRoot
from zope.lifecycleevent.interfaces import IObjectAddedEvent

import logging

logger = logging.getLogger('jornada.contenttypes')


@grok.subscribe(IArticle, IObjectAddedEvent)
def log_object_creation(obj, event):
    """Write a message on the log when an article is created.
    """
    title = aq_inner(obj).Title()
    container = aq_parent(obj)
    is_root = IPloneSiteRoot.providedBy(container)
    container = 'site root' if is_root else container.Title()
    logger.info("The object '%s' was created in '%s'" % (title, container))
