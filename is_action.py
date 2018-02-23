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

    action_globale_id = fields.Many2one('is.action.globale', 'Action globale')
    name              = fields.Char('Action', required=True)
    ordinateur_id     = fields.Many2one('is.ordinateur', 'Ordinateur')
    utilisateur_id    = fields.Many2one('is.utilisateur', 'Utilisateur')
    mail              = fields.Char('Mail', related='utilisateur_id.mail', readonly=True)
    date_creation     = fields.Date('Date création', required=True)
    date_prevue       = fields.Date('Date prévue'  , required=True)
    date_realisee     = fields.Date('Date réalisée')
    commentaire       = fields.Text('Commentaire')


    _defaults = {
        'date_creation': lambda *a: _date_creation(),
    }


    @api.multi
    def acceder_action(self):
        for obj in self:
            return {
                'name': u'Action '+obj.name or '',
                'view_mode': 'form,tree',
                'view_type': 'form',
                'res_model': 'is.action',
                'res_id': obj.id,
                'type': 'ir.actions.act_window',
            }


    @api.multi
    def write(self, vals):
        res=super(is_action, self).write(vals)
        for obj in self:
            if obj.action_globale_id:
                obj.action_globale_id._compute_avancement()
        return res







