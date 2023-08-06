""" EEAContentTypes actions for plone.app.contentrules
"""

import logging
from time import time

from DateTime import DateTime
from OFS.SimpleItem import SimpleItem
from plone import api
from plone.app.contentrules.browser.formhelper import NullAddForm
from plone.contentrules.rule.interfaces import IExecutable, IRuleElementData
from zope.component import adapter
from zope.interface import Interface, implementer

logger = logging.getLogger("eea.dexterity.indicators")


class IRetractAndRenameOldVersionAction(Interface):
    """ Retract and rename old version
    """


@implementer(IRetractAndRenameOldVersionAction, IRuleElementData)
class RetractAndRenameOldVersionAction(SimpleItem):
    """ Retract and rename old version action
    """

    element = 'eea.dexterity.indicators.retract_and_rename_old_version'
    summary = (
        "Will retract and rename older version of this Indicator. "
        "Then rename current Indicator (remove copy_of_ from id)"
    )


@implementer(IExecutable)
@adapter(Interface, IRetractAndRenameOldVersionAction, Interface)
class RetractAndRenameOldVersionExecutor(object):
    """ Retract and rename old version executor
    """
    def __init__(self, context, element, event):
        self.context = context
        self.element = element
        self.event = event

    def __call__(self):
        obj = self.event.object
        oid = obj.getId()
        if not oid.startswith('copy_of_'):
            return True

        parent = obj.getParentNode()
        old_id = oid.replace('copy_of_', '', 1)
        new_id = old_id + '-%d' % time()

        try:
            old_version = parent[old_id]
            api.content.transition(
                obj=old_version, transition='markForDeletion')
            api.content.rename(obj=old_version, new_id=new_id)
            api.content.rename(obj=obj, new_id=old_id)
            obj.setEffectiveDate(DateTime())
        except Exception as err:
            logger.exception(err)
            return True
        return True


class RetractAndRenameOldVersionAddForm(NullAddForm):
    """ Retract and rename old version addform
    """
    def create(self):
        """ Create content-rule
        """
        return RetractAndRenameOldVersionAction()
