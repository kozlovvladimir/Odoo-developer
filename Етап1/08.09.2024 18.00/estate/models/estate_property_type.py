from odoo import models, fields, api
from odoo.exceptions import ValidationError


class EstatePropertyType(models.Model):
    _name = 'estate.property.type'
    _description = 'Property Type'

    name = fields.Char(string='Title', required=True)

    # Поле для вибору статусу
    status = fields.Selection([
        ('new', 'New'),
        ('active', 'Active'),
        ('archived', 'Archived')],
        string='Status', default='new')

    # Додаємо поле для очікуваної ціни
    expected_price = fields.Float(string='Expected Price', required=True)

    # Додаємо поле для стану
    state = fields.Selection(
        [('new', 'New'), ('offer_received', 'Offer Received'), ('offer_accepted', 'Offer Accepted'), ('sold', 'Sold')],
        string='State', default='new'
    )

    def set_status_new(self):
        self.status = 'new'

    def set_status_active(self):
        self.status = 'active'

    def set_status_archived(self):
        self.status = 'archived'

    @api.constrains('name')
    def _check_unique_name(self):
        for record in self:
            existing = self.search([('name', '=', record.name), ('id', '!=', record.id)])
            if existing:
                raise ValidationError("The name must be unique")
