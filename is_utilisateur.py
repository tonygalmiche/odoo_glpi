# -*- coding: utf-8 -*-
import datetime
from openerp import models,fields,api
from openerp.tools.translate import _
from openerp.exceptions import Warning


class is_site(models.Model):
    _name = "is.site"
    _description = "Site"
    _order='name'

    name             = fields.Char(u'Site', required=True)
    code             = fields.Char(u'Code', required=True)
    signature_mail   = fields.Html(u'Modèle signature mail',sanitize=False)
    dest_mozilla_ids = fields.Many2many('is.utilisateur', 'is_site_utilisateur_rel', 'ris_site_id','utilisateur_id', string="Destinataires des anomalies des sauvegardes de Mozilla")


class is_service(models.Model):
    _name = "is.service"
    _description = "Service"
    _order='name'
    _sql_constraints = [('name_uniq','UNIQUE(name)', 'Ce code existe déjà')] 

    name            = fields.Char('Service', required=True)
    commentaire     = fields.Text('Commentaire')


class is_utilisateur(models.Model):
    _name = "is.utilisateur"
    _description = "Utilisateurs"
    _order='site_id,name'
    _sql_constraints = [
        ('name_uniq','UNIQUE(name)'  , 'Ce nom existe déjà'),
        ('login_uniq','UNIQUE(login)', 'Ce login existe déjà'),
    ] 

    site_id         = fields.Many2one('is.site', 'Site', required=True)
    name            = fields.Char('Prénom Nom', required=True)
    login           = fields.Char('Login'     , required=True)
    mail            = fields.Char('Mail')
    service_id      = fields.Many2one('is.service', 'Service')
    fonction        = fields.Char('Fonction')
    telephone       = fields.Char('Téléphone')
    portable        = fields.Char('Portable')
    fax             = fields.Char('Fax')
    autre           = fields.Char('Autre')
    commentaire     = fields.Text('Commentaire')
    action_ids      = fields.One2many('is.action', 'utilisateur_id', u'Actions', readonly=True)
    signature_mail  = fields.Html(u'Signature mail',sanitize=False)
    active          = fields.Boolean('Actif', default=True)


    @api.multi
    def get_tr(self,val):
        if val and val!='':
            val=u"""
                <tr>
                    <td>
                        <font size="3" color="#939393">"""+val+u"""</font>
                    </td>
                </tr>
            """
        else:
            val=''
        return val


    @api.multi
    def generer_signature_mail(self):
        for obj in self:
            html=obj.site_id.signature_mail
            telephone = obj.telephone or ''
            portable  = obj.portable or ''
            fax       = obj.fax or ''
            if telephone != '':
                telephone = u'Tél : '+telephone
            if portable != '':
                portable = u'Mobile : '+portable
            if fax != '':
                fax = u'Fax : '+fax

            fonction  = self.get_tr(obj.fonction)
            telephone = self.get_tr(telephone)
            portable  = self.get_tr(portable)
            fax       = self.get_tr(fax)
            autre     = self.get_tr(obj.autre)

            html = html.replace('${name}'     , (obj.name or ''))
            html = html.replace('${mail}'    , (obj.mail or ''))
            html = html.replace('<tr><td>${fonction}</td></tr>' , fonction)
            html = html.replace('<tr><td>${telephone}</td></tr>', telephone)
            html = html.replace('<tr><td>${portable}</td></tr>' , portable)
            html = html.replace('<tr><td>${fax}</td></tr>'      , fax)
            html = html.replace('<tr><td>${autre}</td></tr>'    , autre)
            if html:
                obj.signature_mail = html


    @api.multi
    def envoyer_signature_mail(self):
        for obj in self:
            name = 'signature-mail.html'
            path = '/tmp/' + name
            f = open(path,'wb')
            f.write(obj.signature_mail.encode('utf-8'))
            f.close()
            datas = open(path,'rb').read().encode('base64')

            # ** Recherche si une pièce jointe est déja associèe ***************
            attachment_obj = self.env['ir.attachment']
            model=self._name
            #name='commandes.pdf'
            attachments = attachment_obj.search([('res_model','=',model),('res_id','=',obj.id),('name','=',name)])
            # ******************************************************************

            # ** Creation ou modification de la pièce jointe *******************
            vals = {
                'name':        name,
                'datas_fname': name,
                'type':        'binary',
                'res_model':   model,
                'res_id':      obj.id,
                'datas':       datas,
            }
            if attachments:
                for attachment in attachments:
                    attachment.write(vals)
            else:
                attachment = attachment_obj.create(vals)
            subject=u'['+obj.name+u'] Nouvelle signature de mail'
            email_to=obj.mail
            user  = self.env['res.users'].browse(self._uid)
            email_from = user.email

            email_to = email_from

            nom   = user.name
            body_html=u"""
                <p>Bonjour,</p>
                <p>Veuillez trouver ci-joint une nouvelle signature pour votre mail.</p>
                <p>Merci de mettre en place celle-ci dans Thunderbird.</p>
                <p>"""+nom+u"""</p>
            """
            vals={
                'email_from'    : email_from, 
                'email_to'      : email_to, 
                'email_cc'      : email_from,
                'subject'       : subject,
                'body_html'     : body_html,
                'attachment_ids': [(6, 0, [attachment.id])] 
            }
            email=self.env['mail.mail'].create(vals)
            if email:
                self.env['mail.mail'].send(email)


