# -*- coding: utf-8 -*-
from openerp import models,fields,api
from openerp.tools.translate import _
from openerp.exceptions import Warning
from datetime import datetime, timedelta
import time
from math import *


def _date_creation():
    #now  = datetime.date.today()
    now=datetime.now()
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
            obj.avancement=avancement
            obj.nb_actions=nb2
            obj.nb_actions_restant=nb2-nb1
            obj.avancement_txt=str(nb1)+'/'+str(nb2)


    name               = fields.Char('N°action', readonly=True)
    action             = fields.Char('Action', required=True)
    date_creation      = fields.Date('Date création', required=True)
    date_prevue_debut  = fields.Date('Date prévue de début', required=True)
    tps_prevu          = fields.Float("Temps prévu par action (H)")
    nb_actions_semaine = fields.Integer("Nombre d'actions par semaine",help="Si 0, la date de fin sera égale à la date de début")
    nb_actions         = fields.Integer("Nombre d'actions", readonly=True)
    nb_actions_restant = fields.Integer("Nombre d'actions restant", readonly=True)
    date_prevue        = fields.Date('Date prévue de fin', readonly=True)
    date_realisee      = fields.Date('Date réalisée')
    avancement_txt     = fields.Char("Avancement"  , readonly=True, compute='_compute_avancement', store=True)
    avancement         = fields.Float("% avancement", readonly=True, compute='_compute_avancement', store=True)
    commentaire        = fields.Text('Commentaire')
    filtre_sur         = fields.Selection([('utilisateur', u'Utilisateur'),('ordinateur', u'Ordinateur')], u"Filtre sur", required=True)
    site_id            = fields.Many2one('is.site', 'Site')
    type_ordinateur_id = fields.Many2one('is.type.ordinateur', "Type d'ordinateur")
    service_id         = fields.Many2one('is.service', 'Service')
    utilisateur_ids    = fields.Many2many('is.utilisateur', 'is_action_globale_utilisateur_rel', 'action_globale_id','utilisateur_id', string="Utilisateurs")
    ordinateur_ids     = fields.Many2many('is.ordinateur' , 'is_action_globale_ordinateur_rel' , 'action_globale_id','ordinateur_id' , string="Ordinateurs" )
    action_ids         = fields.One2many('is.action', 'action_globale_id', u'Actions', readonly=True)


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



#                end_date = datetime.strptime(end_date, '%Y-%m-%d')
#                #days=int(quantity*product.temps_realisation/(3600*24))
#                #days=product.produce_delay+int(quantity*product.temps_realisation/(3600*24))
#                tps_fab=quantity*product.temps_realisation/(3600*24)
#                days=int(ceil(tps_fab))
#                start_date= end_date - timedelta(days=days)
#                start_date = start_date.strftime('%Y-%m-%d')



    @api.multi
    def creer_actions(self):
        for obj in self:
            filtre=[]
            if obj.site_id.id:
                filtre.append(('site_id'           ,'=', obj.site_id.id))
            if obj.service_id.id:
                filtre.append(('service_id'        ,'=', obj.service_id.id))
            if obj.type_ordinateur_id.id:
                filtre.append(('type_ordinateur_id','=', obj.type_ordinateur_id.id))
            if len(obj.utilisateur_ids)>0:
                ids=[]
                for utilisateur in obj.utilisateur_ids:
                    ids.append(utilisateur.id)
                if obj.filtre_sur=='ordinateur':
                    filtre.append(('utilisateur_id','in', ids))
                else:
                    filtre.append(('id','in', ids))
            if len(obj.ordinateur_ids)>0:
                ids=[]
                for ordinateur in obj.ordinateur_ids:
                    ids.append(ordinateur.id)
                if obj.filtre_sur=='ordinateur':
                    filtre.append(('id','in', ids))
                else:
                    filtre.append(('ordinateur_id','in', ids))
            if obj.filtre_sur=='ordinateur':
                rows = self.env['is.ordinateur'].search(filtre)
            else:
                rows = self.env['is.utilisateur'].search(filtre)
            date=obj.date_prevue_debut
            mk_debut = datetime.strptime(date, '%Y-%m-%d')
            date_prevue=obj.date_prevue_debut
            days=0.0
            for row in rows:
                if obj.filtre_sur=='ordinateur':
                    actions = self.env['is.action'].search([('action_globale_id','=',obj.id),('ordinateur_id','=',row.id)])
                else:
                    actions = self.env['is.action'].search([('action_globale_id','=',obj.id),('utilisateur_id','=',row.id)])
                if len(actions)==0 or actions[0].date_realisee==False:
                    if obj.nb_actions_semaine!=0:
                        days=days+7.0/obj.nb_actions_semaine
                        mk = mk_debut + timedelta(days=int(ceil(days)))
                        date_prevue=mk.strftime('%Y-%m-%d')
                    else:
                        date_prevue=obj.date_prevue_debut
                if len(actions)==0:
                    if obj.filtre_sur=='ordinateur':
                        vals={
                            'action_globale_id': obj.id,
                            'name'             : obj.action,
                            'ordinateur_id'    : row.id,
                            'utilisateur_id'   : row.utilisateur_id.id,
                            'date_prevue'      : date_prevue,
                            'tps_prevu'        : obj.tps_prevu,
                        }
                    else:
                        vals={
                            'action_globale_id': obj.id,
                            'name'             : obj.action,
                            'utilisateur_id'   : row.id,
                            'date_prevue'      : date_prevue,
                            'tps_prevu'        : obj.tps_prevu,
                        }
                    res=self.env['is.action'].create(vals)
                else:
                    for action in actions:
                        action.name      = obj.action
                        action.tps_prevu = obj.tps_prevu
                        if action.date_realisee==False:
                            action.date_prevue=date_prevue
            obj.date_prevue=date_prevue


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





