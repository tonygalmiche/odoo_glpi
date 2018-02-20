# -*- coding: utf-8 -*-
import datetime
from openerp import models,fields,api
from openerp.tools.translate import _
from openerp.exceptions import Warning


class is_utilisateur(models.Model):
    _name = "is.utilisateur"
    _description = "Utilisateurs"
    _order='name'

    name            = fields.Char('Prénom Nom', required=True)
    login           = fields.Char('Login'     , required=True)
    mail            = fields.Char('Mail')
    service         = fields.Char('Service')
    commentaire     = fields.Text('Commentaire')
    action_ids      = fields.One2many('is.action', 'utilisateur_id', u'Actions', readonly=True)

