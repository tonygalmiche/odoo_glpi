# -*- coding: utf-8 -*-
from openerp import models,fields,api

class is_logiciel(models.Model):
    _name = "is.logiciel"
    _description = "Logiciel"
    _order='logiciel,version'
    _sql_constraints = [('logiciel_version_uniq','UNIQUE(logiciel_id,version_id)', 'Ce logiciel existe deja !')] 

    logiciel     = fields.Char('Logiciel'      , select=1)
    logiciel_id  = fields.Integer('Logiciel id', select=1)
    version      = fields.Char('Version'       , select=1)
    version_id   = fields.Integer('Version id' , select=1)
    nb           = fields.Integer('Nb installations')
    ordinateurs  = fields.Text('Ordinateurs')
    commentaire  = fields.Text('Commentaire')
