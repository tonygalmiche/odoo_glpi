# -*- coding: utf-8 -*-
from openerp import models,fields,api

class is_logiciel(models.Model):
    _name = "is.logiciel"
    _description = "Logiciel"
    _order='logiciel,version'

    logiciel     = fields.Char('Logiciel'      , select=1)
    logiciel_id  = fields.Integer('Logiciel id', select=1)
    version      = fields.Char('Version'       , select=1)
    version_id   = fields.Integer('Version id' , select=1)
    nb           = fields.Integer('Nb installations')
    ordinateurs  = fields.Text('Ordinateurs')
    commentaire  = fields.Text('Commentaire')
