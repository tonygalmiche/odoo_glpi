# -*- coding: utf-8 -*-
import datetime
from openerp import models,fields,api
from openerp.tools.translate import _
from openerp.exceptions import Warning


class is_save_mozilla(models.Model):
    _name = "is.save.mozilla"
    _description = "Sauvegarde Mozilla"
    _order='heure_debut desc'

    date            = fields.Date('Date sauvegarde')
    site_id         = fields.Many2one('is.site', 'Site')
    service_id      = fields.Many2one('is.service', 'Service')
    utilisateur_id  = fields.Many2one('is.utilisateur', 'Utilisateur')
    ordinateur_id   = fields.Many2one('is.ordinateur', 'Ordinateur')
    partage         = fields.Char('Partage')
    mail            = fields.Char('Mail')
    taille          = fields.Integer('Taille (Mo)')
    nb_modifs       = fields.Integer('Nb modifs')
    heure_debut     = fields.Datetime('Heure début')
    heure_fin       = fields.Datetime('Heure fin')
    temps           = fields.Integer('Temps (s)')
    resultat        = fields.Text('Résultat')


    def name_get(self, cr, uid, ids, context=None):
        res = []
        for obj in self.browse(cr, uid, ids, context=context):
            name=str(obj.heure_debut)+" "+obj.ordinateur_id.name
            res.append((obj.id,name))
        return res


