from odoo import api, fields, models

class ZapatosZapato(models.Model):
    _inherit = 'zapatos.zapato'

    alerta_stock = fields.Boolean(
        string="Requiere Reabastecimiento",
        compute="_compute_alerta_stock",
        store=True,
    )

    @api.depends('stock')
    def _compute_alerta_stock(self):
        for zapato in self:
            zapato.alerta_stock = zapato.stock < 5
