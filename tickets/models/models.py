from odoo import models, fields, api, exceptions
from datetime import datetime


class Tickets(models.Model):
    _name = 'tickets.print'
    _description = 'Tickets print'

    start_date = fields.Datetime(string="date de debut", default=fields.Datetime.today)
    end_date = fields.Datetime(string="date de fin", store=True)
    lieu_ids = fields.Many2one('tickets.lieu', ondelete='cascade', string="lieu", required=True)
    operateur_ids = fields.Many2one('tickets.operateur', ondelete='cascade', string="operateur", required=True)
    client_ids = fields.Many2one('tickets.client', ondelete='cascade', string="client", required=True)
    recieve_date = fields.Datetime(string="date de reception", default=fields.Datetime.today)
    out_date = fields.Datetime(string="date de sortie", store=True)
    tel = fields.Char()
    info = fields.Text()
    material_ids = fields.Many2many('tickets.material', string="Material")
    commentaire = fields.Text()
    rep = fields.Selection(string='Type', selection=[('reparable', 'reparable'), ('non reparable', 'non reparable')], default='non reparable')
    recup = fields.Selection(string='recuperation', selection=[('sortie', 'sortie'), ('non sortie', 'non sortie')], default='non sortie')
    color = fields.Integer(string="color", compute='change_color')

    name = fields.Char(string='ID', help="Lab Result ID", readonly="1", copy=False, index=True)

    @api.onchange
    def change_color(self):
        if datetime.today() < self.end_date:
            color = 0
        elif (self.rep == "reparable" and self.recup == "sortie") or (self.rep == "non reparable" and self.recup == "sortie"):
            color = 1
        elif self.rep == "reparable" and self.recup == "non sortie":
            color = 2
        elif self.rep == "non reparable" and self.recup == "non sortie":
            color = 3
        
        return color

    @api.model
    def create(self, vals):
        vals['name'] = self.env['ir.sequence'].next_by_code('patient.scanning.test')

        return super(Tickets, self).create(vals)

    @api.onchange('client_ids')
    def onchange_product_id(self):
        self.tel = self.client_ids.tel


class Operateur(models.Model):
    _name = 'tickets.operateur'
    _description = 'Tickets Operateur'

    name = fields.Char(required=True)
    description = fields.Text()


class Lieu(models.Model):
    _name = 'tickets.lieu'
    _description = 'Tickets lieu'

    name = fields.Char(required=True)
    description = fields.Text()


class Client(models.Model):
    _name = 'tickets.client'
    _description = 'Tickets Client'

    name = fields.Char(required=True)
    tel = fields.Char(required=True)
    adress = fields.Text()
    description = fields.Text()


class Material(models.Model):
    _name = 'tickets.material'
    _description = 'Tickets material'

    name = fields.Char(required=True)
    description = fields.Text()
