# -*- coding: utf-8 -*-
{
    "name" : "InfoSaône - Module Odoo GLPI",
    "version" : "0.2",
    "author" : "InfoSaône",
    "category" : "InfoSaône",
    "description": """
InfoSaône - Module Odoo GLPI
===================================================
InfoSaône - Module Odoo GLPI
    """,
    "maintainer": 'InfoSaône',
    "website": 'http://www.infosaone.com',
    "depends" : [
        "base",
        "document",
    ], 
    "data" : [
        "security/ir.model.access.csv",
        "is_utilisateur_view.xml",
        "is_ordinateur_view.xml",
        "is_action_view.xml",
        "is_action_globale_view.xml",
        "is_identifiant_view.xml",
        "is_save_mozilla_view.xml",
        "is_save_serveur_view.xml",
        "is_suivi_sauvegarde_view.xml",
        "is_equipement_reseau_view.xml",
        "res_company_view.xml",
        "assets.xml",
        "menu.xml",
    ], 
    "installable": True,
    "active": False,
    "application": True
}

