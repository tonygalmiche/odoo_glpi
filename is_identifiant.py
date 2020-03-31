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


    @api.multi
    def envoyer_identifiant_bluemind_action(self):
        for obj in self:
            if obj.bluemind == True:
                subject=u'['+obj.utilisateur_id.name+u'] Identifiant Bluemind'
                email_to   = obj.utilisateur_id.mail
                user       = self.env['res.users'].browse(self._uid)
                email_from = user.email
                nom        = user.name
                if email_to :
                    body_html=u"""
                        <p>Bonjour,</p>
                        <p>Nous avons mis en place la nouvelle version de l'agenda Bluemind et migré tous les comptes ainsi que votre agenda tel qu'il était à la date de la migration.</p>
                        <p>L'adresse pour y accéder est : <b><a href="https://bluemind4.plastigray.com">https://bluemind4.plastigray.com</a></b></p>
                        <p>
                            Vos identifiants sont désormais :<br>
                            - Identifiant : <b>"""+obj.name+u"""</b><br>
                            - Mot de passe : <b>"""+obj.mot_de_passe+u"""</b><br>
                        </p>
                        <p>Vous pouvez supprimer tous les raccourcis et mots de passe pour l'ancien Bluemind dans votre navigateur.</p>
                        <p>Suite à des contraintes techniques indépendantes de notre volonté, il sera nécessaire de supprimer puis recréer toutes les réservations de ressource.</p>
                        <p>Nous sommes conscient des désagréments engendrés, mais nous n'avons pas d'autre solution à proposer.</p>
                        <p>Cordialement</p>
                        <p>"""+nom+u"""</p>
                    """
                    vals={
                        'email_from'    : email_from, 
                        'email_to'      : email_to, 
                        'email_cc'      : email_from,
                        'subject'       : subject,
                        'body_html'     : body_html,
                    }
                    email=self.env['mail.mail'].create(vals)
                    if email:
                        self.env['mail.mail'].send(email)

