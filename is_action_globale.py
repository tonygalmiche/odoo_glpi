# -*- coding: utf-8 -*-
import datetime
from openerp import models,fields,api
from openerp.tools.translate import _
from openerp.exceptions import Warning


def _date_creation():
    now  = datetime.date.today()
    return now.strftime('%Y-%m-%d')


class is_action_globale(models.Model):
    _name = "is.action.globale"
    _description = "Action Globale"
    _order='name desc'


    @api.depends('action_ids')
    def _compute_avancement(self):
        for obj in self:
            nb1=len(self.env['is.action'].search([('action_globale_id','=',obj.id),('date_realisee','!=',False)]))
            nb2=len(obj.action_ids)

            avancement=0
            if nb2!=0:
                avancement=100.0*nb1/nb2
            print nb1,nb2,avancement
            obj.avancement=avancement


    name            = fields.Char('N°action', readonly=True)
    action          = fields.Char('Action', required=True)
    date_creation   = fields.Date('Date création', required=True)
    date_prevue     = fields.Date('Date prévue'  , required=True)
    date_realisee   = fields.Date('Date réalisée')
    avancement      = fields.Float("% avancement", readonly=True, compute='_compute_avancement', store=True)
    commentaire     = fields.Text('Commentaire')
    filtre_sur      = fields.Selection([('utilisateur', u'Utilisateur'),('ordinateur', u'Ordinateur')], u"Filtre sur", required=True)
    site_id         = fields.Many2one('is.site', 'Site')
    service_id      = fields.Many2one('is.service', 'Service')
    utilisateur_ids = fields.Many2many('is.utilisateur', 'is_action_globale_utilisateur_rel', 'action_globale_id','utilisateur_id', string="Utilisateurs")
    ordinateur_ids  = fields.Many2many('is.ordinateur' , 'is_action_globale_ordinateur_rel' , 'action_globale_id','ordinateur_id' , string="Ordinateurs" )
    action_ids      = fields.One2many('is.action', 'action_globale_id', u'Actions', readonly=True)


    _defaults = {
        'date_creation': lambda *a: _date_creation(),
    }


    @api.model
    def create(self, vals):
        sequence_ids = self.env['ir.model.data'].search([('name','=','is_action_globale_seq')])
        if len(sequence_ids)>0:
            sequence_id = sequence_ids[0].res_id
            vals['name'] = self.env['ir.sequence'].get_id(sequence_id, 'id')
        res = super(is_action_globale, self).create(vals)
        return res



    @api.multi
    def creer_action_par_ordinateur(self):
        for obj in self:
            filtre=[]
            if obj.site_id.id:
                filtre.append(('site_id'       ,'=' , obj.site_id.id))
            if obj.service_id.id:
                filtre.append(('service_id'       ,'=' , obj.service_id.id))
            if len(obj.utilisateur_ids)>0:
                ids=[]
                for utilisateur in obj.utilisateur_ids:
                    ids.append(utilisateur.id)
                filtre.append(('utilisateur_id','in', ids))
            if len(obj.ordinateur_ids)>0:
                ids=[]
                for ordinateur in obj.ordinateur_ids:
                    ids.append(ordinateur.id)
                filtre.append(('id','in', ids))
            ordinateurs = self.env['is.ordinateur'].search(filtre)
            for ordinateur in ordinateurs:
                actions = self.env['is.action'].search([('action_globale_id','=',obj.id),('ordinateur_id','=',ordinateur.id)])
                if len(actions)==0:
                    vals={
                        'action_globale_id': obj.id,
                        'name'             : obj.action,
                        'ordinateur_id'    : ordinateur.id,
                        'utilisateur_id'   : ordinateur.utilisateur_id.id,
                        'date_prevue'      : obj.date_prevue,
                    }
                    res=self.env['is.action'].create(vals)
                else:
                    for action in actions:
                        vals={
                            'name'             : obj.action,
                            'date_prevue'      : obj.date_prevue,
                        }
                        action.write(vals)


    @api.multi
    def creer_action_par_utilisateur(self):
        for obj in self:
            filtre=[]
            if obj.site_id.id:
                filtre.append(('site_id'       ,'=' , obj.site_id.id))
            if obj.service_id.id:
                filtre.append(('service_id'       ,'=' , obj.service_id.id))
            if len(obj.utilisateur_ids)>0:
                ids=[]
                for utilisateur in obj.utilisateur_ids:
                    ids.append(utilisateur.id)
                filtre.append(('id','in', ids))
            if len(obj.ordinateur_ids)>0:
                ids=[]
                for ordinateur in obj.ordinateur_ids:
                    ids.append(ordinateur.id)
                filtre.append(('ordinateur_id','in', ids))

            print 'filtre=',filtre

            utilisateurs = self.env['is.utilisateur'].search(filtre)
            for utilisateur in utilisateurs:
                actions = self.env['is.action'].search([('action_globale_id','=',obj.id),('utilisateur_id','=',utilisateur.id)])
                if len(actions)==0:
                    vals={
                        'action_globale_id': obj.id,
                        'name'             : obj.action,
                        'utilisateur_id'   : utilisateur.id,
                        'date_prevue'      : obj.date_prevue,
                    }
                    res=self.env['is.action'].create(vals)
                else:
                    for action in actions:
                        vals={
                            'name'             : obj.action,
                            'date_prevue'      : obj.date_prevue,
                        }
                        action.write(vals)


    @api.multi
    def liste_actions(self):
        for obj in self:
            return {
                'name': u'Lignes',
                'view_mode': 'tree,form',
                'view_type': 'form',
                'res_model': 'is.action',
                'domain': [
                    ('action_globale_id','=',obj.id),
                ],
                'type': 'ir.actions.act_window',
                'limit': 1000,
            }





