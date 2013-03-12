# -*- coding: utf-8 -*-

from Acquisition import aq_inner
from jornada.contenttypes import _
from plone.app.layout.navigation.root import getNavigationRootObject
from plone.app.portlets.cache import render_cachekey
from plone.app.portlets.portlets import base
from plone.memoize import ram
from plone.memoize.compress import xhtml_compress
from plone.memoize.instance import memoize
from plone.portlets.interfaces import IPortletDataProvider
from Products.CMFCore.utils import getToolByName
from zope import schema
from zope.browserpage.viewpagetemplatefile import ViewPageTemplateFile
from zope.component import getMultiAdapter
from zope.formlib import form
from zope.interface import implements


class IArticlesPortlet(IPortletDataProvider):
    """This portlet displays recent Articles.
    """

    count = schema.Int(
        title=_(u"Number of items to display"),
        description=_(u'How many items to list.'),
        default=5,
        required=False)


class Assignment(base.Assignment):

    implements(IArticlesPortlet)

    def __init__(
        self, count=5):

        self.count = count

    @property
    def title(self):
        return _(u"Latest Articles")


class Renderer(base.Renderer):

    _template = ViewPageTemplateFile('articles.pt')

    def __init__(self, *args):
        base.Renderer.__init__(self, *args)

    @ram.cache(render_cachekey)
    def render(self):
        return xhtml_compress(self._template())

    @property
    def available(self):
        return self.data.count > 0 and len(self._data())

    def published_articles(self):
        return self._data()

    def all_news_link(self):
        context = aq_inner(self.context)
        portal_state = getMultiAdapter(
            (context, self.request), name=u'plone_portal_state')
        portal = portal_state.portal()
        if 'news' in getNavigationRootObject(context, portal).objectIds():
            return '%s/news' % portal_state.navigation_root_url()
        return None

    @memoize
    def _data(self):
        context = aq_inner(self.context)
        catalog = getToolByName(context, 'portal_catalog')
        portal_state = getMultiAdapter(
            (context, self.request), name=u'plone_portal_state')

        # get recent articles and sort them by date in reverse order
        query = {}
        query['portal_type'] = 'Article'
        query['path'] = portal_state.navigation_root_path()
        query['review_state'] = 'published'
        query['sort_on'] = 'Date'
        query['sort_order'] = 'reverse'
        query['sort_limit'] = self.data.count

        return catalog(**query)[:self.data.count]

    @property
    def title(self):
        return _(u"Latest Articles")


class AddForm(base.AddForm):

    form_fields = form.Fields(IArticlesPortlet)

    label = _(u"Add Articles Portlet")
    description = _(u"This portlet displays recent Articles.")

    def create(self, data):
        return Assignment(**data)


class EditForm(base.EditForm):

    form_fields = form.Fields(IArticlesPortlet)

    label = _(u"Edit Articles Portlet")
    description = _(u"This portlet displays recent Articles.")
