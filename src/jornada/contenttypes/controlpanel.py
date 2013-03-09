# -*- coding: utf-8 -*-

from jornada.contenttypes import _
from plone.app.registry.browser import controlpanel
from plone.directives import form
from zope import schema


class IJornadaSettings(form.Schema):
    """Interface for the control panel form.
    """
    available_sections = schema.Set(
        title=_(u"Available Sections"),
        default=set(),
        value_type=schema.TextLine(title=_(u"Section")),
    )

    default_section = schema.Choice(
        title=_(u"Default Section"),
        vocabulary=u'jornada.contenttypes.AvailableSections',
        required=False,
    )


class JornadaSettingsEditForm(controlpanel.RegistryEditForm):
    schema = IJornadaSettings
    label = _(u"Jornada Settings")
    description = _(u"Here you can modify the settings for jornada.contenttypes.")

    def updateFields(self):
        super(JornadaSettingsEditForm, self).updateFields()

    def updateWidgets(self):
        super(JornadaSettingsEditForm, self).updateWidgets()


class JornadaSettingsControlPanel(controlpanel.ControlPanelFormWrapper):
    form = JornadaSettingsEditForm
