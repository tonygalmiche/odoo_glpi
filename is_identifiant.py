# -*- coding: utf-8 -*-
import datetime
from openerp import models,fields,api
from openerp.tools.translate import _
from openerp.exceptions import Warning


class is_identifiant(models.Model):
    _name = "is.identifiant"
    _description = "Identifiants"
    _order='name,ordinateur_id'

    name             = fields.Char('Login'       , required=True)
    mot_de_passe     = fields.Char('Mot de passe', required=True)
    site_id          = fields.Many2one('is.site', 'Site', required=True)
    service_id       = fields.Many2one('is.service', 'Service')
    utilisateur_id   = fields.Many2one('is.utilisateur', 'Utilisateur')
    ordinateur_id    = fields.Many2one('is.ordinateur', 'Ordinateur')
    admin_ordinateur = fields.Boolean("Compte admin de l'ordinateur"      , default=False)
    cpt_utilisateur  = fields.Boolean("Compte utilisateur de l'ordinateur", default=False)
    lam_gray         = fields.Boolean('LAM Gray'                          , default=False)
    lam_st_brice     = fields.Boolean('LAM ST-Brice'                      , default=False)
    lam_pk           = fields.Boolean('LAM PK'                            , default=False)
    bluemind         = fields.Boolean('Bluemind'                          , default=False)
    mail             = fields.Boolean('Mail FC-NET'                       , default=False)
    tightvnc         = fields.Boolean('TightVNC'                          , default=False)
    commentaire      = fields.Text('Commentaire')
    active           = fields.Boolean('Actif', default=True)

