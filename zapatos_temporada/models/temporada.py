from odoo import models, fields, api


class ZapatosDescuento(models.Model):
    _inherit = 'zapatos.zapato'
    
    subprecio = fields.Float(
        string="Precio de Oferta",
        compute="_compute_subprecio",
        readonly=True,
        store=True
    )
    
    @api.depends('precio', 'stock')
    def _compute_subprecio(self):
        """Calcula el precio de oferta con 15% de descuento si stock > 30"""
        for record in self:
            if record.stock > 30:
                record.subprecio = record.precio * 0.85
            else:
                record.subprecio = record.precio
