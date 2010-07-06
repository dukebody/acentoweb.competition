# CMF and Zope imports
from zope.interface import implements

# Archetypes imports
from Products.Archetypes import atapi

# Product imports
from acentoweb.competition.config import PROJECTNAME
from acentoweb.competition.interfaces import ICompetition

CompetitionSchema = atapi.BaseFolderSchema.copy()

class Competition(atapi.BaseFolder):
    """An Archetype for an LibreOrganizacion application
    """
    implements(ICompetition)

    schema = CompetitionSchema
    
    _at_rename_after_creation = True  # ??? isn't this the default?
    
    def tag(self, **kwargs):
        return self.getField('image').tag(self, **kwargs)

atapi.registerType(Competition, PROJECTNAME)
