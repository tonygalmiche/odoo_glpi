# -*- coding: utf-8 -*-
import datetime
import pytz
from openerp import models,fields,api
from openerp.tools.translate import _
from openerp.exceptions import Warning
import logging
_logger = logging.getLogger(__name__)


class is_equipement_reseau(models.Model):
    _name = "is.equipement.reseau"
    _description = "Equipement reseau"
    _order='ordinateur_id'

    adresse_ip           = fields.Char('Adresse IP')
    adresse_mac          = fields.Char('Adresse MAC')
    site_id              = fields.Many2one('is.site', 'Site')
    ordinateur_id        = fields.Many2one('is.ordinateur', 'Ordinateur')
    date_creation        = fields.Datetime('Date de création')
    date_modification    = fields.Datetime('Date de modification')
    origine_modification = fields.Char('Origine de la modification')
    commentaire          = fields.Text('Commentaire')
    active               = fields.Boolean('Actif', default=True)


    def name_get(self, cr, uid, ids, context=None):
        res = []
        for obj in self.browse(cr, uid, ids, context=context):
            name=str(obj.adresse_ip)
            res.append((obj.id,name))
        return res




