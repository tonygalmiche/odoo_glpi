# -*- coding: utf-8 -*-
import datetime
from openerp import models,fields,api
from openerp.tools.translate import _
from openerp.exceptions import Warning


class is_site(models.Model):
    _name = "is.site"
    _description = "Site"
    _order='name'

    name             = fields.Char('Site', required=True)
    code             = fields.Char('Code', required=True)
    dest_mozilla_ids = fields.Many2many('is.utilisateur', 'is_site_utilisateur_rel', 'ris_site_id','utilisateur_id', string="Destinataires des anomalies des sauvegardes de Mozilla")


class is_service(models.Model):
    _name = "is.service"
    _description = "Service"
    _order='name'

    name            = fields.Char('Service', required=True)
    commentaire     = fields.Text('Commentaire')


class is_utilisateur(models.Model):
    _name = "is.utilisateur"
    _description = "Utilisateurs"
    _order='site_id,name'

    site_id         = fields.Many2one('is.site', 'Site', required=True)
    name            = fields.Char('Prénom Nom', required=True)
    login           = fields.Char('Login'     , required=True)
    mail            = fields.Char('Mail')
    service_id      = fields.Many2one('is.service', 'Service')
    commentaire     = fields.Text('Commentaire')
    action_ids      = fields.One2many('is.action', 'utilisateur_id', u'Actions', readonly=True)
    active          = fields.Boolean('Actif', default=True)

