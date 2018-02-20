# -*- coding: utf-8 -*-
import datetime
from openerp import models,fields,api
from openerp.tools.translate import _
from openerp.exceptions import Warning


def _date_creation():
    now  = datetime.date.today()
    return now.strftime('%Y-%m-%d')


class is_action(models.Model):
    _name = "is.action"
    _description = "Actions"
    _order='date_creation desc, name'

    name           = fields.Char('Action', required=True)
    ordinateur_id  = fields.Many2one('is.ordinateur', 'Ordinateur')
    utilisateur_id = fields.Many2one('is.utilisateur', 'Utilisateur')
    mail           = fields.Char('Mail', related='utilisateur_id.mail', readonly=True)
    date_creation  = fields.Date('Date création', required=True)
    date_prevue    = fields.Date('Date prévue'  , required=True)
    date_realisee  = fields.Date('Date réalisée')
    commentaire    = fields.Text('Commentaire')


    _defaults = {
        'date_creation': lambda *a: _date_creation(),
    }



