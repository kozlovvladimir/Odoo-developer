from odoo import models, fields, api
from odoo.exceptions import ValidationError
from odoo.tools.float_utils import float_compare
from datetime import timedelta

class EstatePropertyOffer(models.Model):
    _name = 'estate.property.offer'
    _description = 'Property Offer'

    price = fields.Float(string='Price', required=True)
    status = fields.Selection([
        ('accepted', 'Accepted'),
        ('refused', 'Refused')],
        string='Status', copy=False, default='refused')
    partner_id = fields.Many2one('res.partner', string='Partner', required=True)
    property_id = fields.Many2one('estate.property', string='Property', required=True)
    validity = fields.Integer(string='Validity (days)', default=7)
    date_deadline = fields.Date(string='Deadline', compute='_compute_date_deadline', inverse='_inverse_date_deadline')

    _sql_constraints = [
        ('check_price_positive', 'CHECK(price > 0)', 'The offer price must be strictly positive.')
    ]

    @api.constrains('price')
    def _check_price_positive(self):
        for record in self:
            if record.price <= 0:
                raise ValidationError('The offer price must be strictly positive.')

    @api.depends('validity', 'create_date')
    def _compute_date_deadline(self):
        for record in self:
            if record.create_date:
                create_date = fields.Date.from_string(record.create_date)
                record.date_deadline = create_date + timedelta(days=record.validity)
            else:
                record.date_deadline = fields.Date.today() + timedelta(days=record.validity)

    def _inverse_date_deadline(self):
        for record in self:
            if record.date_deadline:
                create_date = fields.Date.from_string(record.create_date) if record.create_date else fields.Date.today()
                record.validity = (record.date_deadline - create_date).days

    @api.model
    def create(self, vals):
        """
        Overrides the create method to set property state to 'Offer Received'
        and check if the offer amount is lower than an existing offer.
        """
        property_id = vals.get('property_id')  # Получаем ID недвижимости
        if property_id:
            # Используем browse для получения объекта недвижимости по ID
            property_record = self.env['estate.property'].browse(property_id)

            if property_record:
                # Проверяем, есть ли существующие предложения с более высокой или равной ценой
                existing_offer = property_record.offer_ids.filtered(lambda o: o.price >= vals.get('price'))
                if existing_offer:
                    raise ValidationError("An existing offer has a higher or equal price. Please adjust your offer amount.")

                # Устанавливаем состояние недвижимости в 'Offer Received'
                property_record.write({'state': 'offer_received'})

        # Создаем запись предложения
        return super(EstatePropertyOffer, self).create(vals)

    def action_accept(self):
        for offer in self:
            if offer.status != 'accepted':
                # Check if the offer price is not lower than 90% of the property's expected price
                if float_compare(offer.price, offer.property_id.expected_price * 0.9, precision_rounding=0.01) < 0:
                    raise ValidationError("The offer price cannot be lower than 90% of the property's expected price.")
                offer.status = 'accepted'
                offer.property_id.write({
                    'selling_price': offer.price,
                    'buyer_id': offer.partner_id.id
                })
                other_offers = offer.property_id.offer_ids.filtered(lambda o: o.id != offer.id)
                other_offers.write({'status': 'refused'})

    def action_refuse(self):
        for offer in self:
            if offer.status != 'refused':
                offer.status = 'refused'
