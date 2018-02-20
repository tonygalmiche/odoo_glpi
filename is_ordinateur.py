# -*- coding: utf-8 -*-
import datetime
from openerp import models,fields,api
from openerp.tools.translate import _
from openerp.exceptions import Warning


class is_ordinateur(models.Model):
    _name = "is.ordinateur"
    _description = "Ordinateurs"
    _order='name'

    name           = fields.Char('Nom du poste', required=True)
    utilisateur_id = fields.Many2one('is.utilisateur', 'Utilisateur')
    date_debut     = fields.Date('Date de mise en service')
    commentaire    = fields.Text('Commentaire')
    action_ids     = fields.One2many('is.action', 'ordinateur_id', u'Actions', readonly=True)





