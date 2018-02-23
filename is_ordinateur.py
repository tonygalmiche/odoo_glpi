# -*- coding: utf-8 -*-
import datetime
from openerp import models,fields,api
from openerp.tools.translate import _
from openerp.exceptions import Warning


class is_partage(models.Model):
    _name = "is.partage"
    _description = "Partages Windows"
    _order='name'

    name = fields.Char('Partage', required=True)


class is_ordinateur(models.Model):
    _name = "is.ordinateur"
    _description = "Ordinateurs"
    _order='name'

    site_id        = fields.Many2one('is.site', 'Site', required=True)
    name           = fields.Char('Nom du poste', required=True)
    service_id     = fields.Many2one('is.service', 'Service')
    utilisateur_id = fields.Many2one('is.utilisateur', 'Utilisateur')
    date_debut     = fields.Date('Date de mise en service')
    partage_ids    = fields.Many2many('is.partage' , 'is_ordinateur_partage_rel' , 'ordinateur_id','partage_id' , string="Partages", help=u"Ce champ est utilisé par le programme de sauvegarde des messageries" )
    commentaire    = fields.Text('Commentaire')
    action_ids     = fields.One2many('is.action', 'ordinateur_id', u'Actions', readonly=True)
    active         = fields.Boolean('Actif', default=True)







