from odoo import models, fields, api

class ZapatosZapato(models.Model):
    _inherit = 'zapatos.zapato'
    porcentaje_descuento = fields.Float(string='Descuento (%)', default=0.0)
    precio_oferta = fields.Float(
        string='Precio de Oferta',
        compute='_compute_precio_oferta',
        store=True
    )
    @api.depends('precio', 'porcentaje_descuento') 
    def _compute_precio_oferta(self):
        for record in self:
            if record.porcentaje_descuento > 0:
                rebaja = record.precio * (record.porcentaje_descuento / 100.0)
                record.precio_oferta = record.precio - rebaja
            else:
                record.precio_oferta = record.precio