from odoo import models, fields, api
from odoo.exceptions import ValidationError


class ZapatosDevolucion(models.Model):
    _name = 'zapatos.devolucion'
    _description = 'Devolución / Cambio de Zapato'
    _order = 'fecha desc, id desc'

    name = fields.Char(string='Referencia',required=True,copy=False,readonly=True,default='Nuevo')
    tipo = fields.Selection([
        ('devolucion', 'Devolución'),
        ('cambio', 'Cambio'),
    ], string='Tipo', required=True, default='devolucion')
    estado = fields.Selection([
        ('borrador', 'Borrador'),
        ('confirmado', 'Confirmado'),
        ('completado', 'Completado'),
        ('cancelado', 'Cancelado'),
    ], string='Estado', default='borrador', tracking=True)
    fecha = fields.Date(string='Fecha',required=True,default=fields.Date.today)
    zapato_id = fields.Many2one(comodel_name='zapatos.zapato',string='Zapato Original',required=True,domain=[('activo', '=', True)],)
    zapato_cambio_id = fields.Many2one(comodel_name='zapatos.zapato',string='Zapato de Cambio',domain=[('activo', '=', True)],help='Completar solo si el tipo es Cambio.',)
    cantidad = fields.Integer(string='Cantidad', required=True, default=1)
    motivo = fields.Selection([
        ('talla_incorrecta', 'Talla incorrecta'),
        ('defecto_fabricacion', 'Defecto de fabricación'),
        ('no_le_gusto', 'No le gustó'),
        ('otro', 'Otro'),
    ], string='Motivo', required=True)
    notas = fields.Text(string='Notas adicionales')
    precio_devuelto = fields.Float(string='Monto a devolver',compute='_compute_precio_devuelto',store=True,)
    diferencia_precio = fields.Float(string='Diferencia de precio',compute='_compute_diferencia_precio',store=True,help='Diferencia entre el zapato de cambio y el original (solo aplica en Cambio).',)

    @api.depends('zapato_id', 'cantidad')
    def _compute_precio_devuelto(self):
        for rec in self:
            if rec.zapato_id:
                rec.precio_devuelto = rec.zapato_id.precio * rec.cantidad
            else:
                rec.precio_devuelto = 0.0

    @api.depends('zapato_id', 'zapato_cambio_id', 'cantidad')
    def _compute_diferencia_precio(self):
        for rec in self:
            if rec.tipo == 'cambio' and rec.zapato_id and rec.zapato_cambio_id:
                rec.diferencia_precio = (
                    rec.zapato_cambio_id.precio - rec.zapato_id.precio
                ) * rec.cantidad
            else:
                rec.diferencia_precio = 0.0

    @api.constrains('tipo', 'zapato_cambio_id')
    def _check_zapato_cambio(self):
        for rec in self:
            if rec.tipo == 'cambio' and not rec.zapato_cambio_id:
                raise ValidationError(
                    'Debe seleccionar el Zapato de Cambio cuando el tipo es "Cambio".'
                )

    @api.constrains('cantidad')
    def _check_cantidad(self):
        for rec in self:
            if rec.cantidad <= 0:
                raise ValidationError('La cantidad debe ser mayor a cero.')



    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('name', 'Nuevo') == 'Nuevo':
                prefijo = 'DEV' if vals.get('tipo') == 'devolucion' else 'CAM'
                vals['name'] = self.env['ir.sequence'].next_by_code(
                    'zapatos.devolucion'
                ) or prefijo + '/0001'
        return super().create(vals_list)


    def action_confirmar(self):
        for rec in self:
            rec.estado = 'confirmado'

    def action_completar(self):
        """Completa la devolución/cambio y ajusta el stock."""
        for rec in self:
            if rec.estado != 'confirmado':
                raise ValidationError('Solo se pueden completar registros confirmados.')

            # Devolver stock del zapato original
            rec.zapato_id.stock += rec.cantidad

            # Si es cambio, descontar stock del zapato de reemplazo
            if rec.tipo == 'cambio' and rec.zapato_cambio_id:
                if rec.zapato_cambio_id.stock < rec.cantidad:
                    raise ValidationError(
                        f'Stock insuficiente para "{rec.zapato_cambio_id.name}". '
                        f'Disponible: {rec.zapato_cambio_id.stock}, requerido: {rec.cantidad}.'
                    )
                rec.zapato_cambio_id.stock -= rec.cantidad

            rec.estado = 'completado'

    def action_cancelar(self):
        for rec in self:
            rec.estado = 'cancelado'

    def action_borrador(self):
        for rec in self:
            rec.estado = 'borrador'
