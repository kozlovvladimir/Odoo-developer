from odoo import models, fields, api, Command
from odoo.exceptions import ValidationError, UserError
from datetime import timedelta

class EstateProperty(models.Model):
    _name = 'estate.property'
    _description = 'Real Estate Property'
    _inherit = ['mail.thread']  # Підтримка стрічки повідомлень

    name = fields.Char(string='Назва', required=True)
    description = fields.Text(string='Опис')
    postcode = fields.Char(string='Поштовий індекс')
    date_availability = fields.Date(
        string='Дата доступності',
        default=lambda self: fields.Date.context_today(self) + timedelta(days=90)
    )
    expected_price = fields.Float(string='Очікувана ціна', required=True)
    selling_price = fields.Float(string='Ціна продажу', readonly=True, copy=False)
    bedrooms = fields.Integer(string='Кількість спалень', default=2)
    living_area = fields.Integer(string='Житлова площа')
    facades = fields.Integer(string='Кількість фасадів')
    garage = fields.Boolean(string='Наявність гаража')
    garden = fields.Boolean(string='Наявність саду')
    garden_area = fields.Integer(string='Площа саду')
    garden_orientation = fields.Selection([
        ('north', 'Північ'),
        ('south', 'Південь'),
        ('east', 'Схід'),
        ('west', 'Захід')],
        string='Орієнтація саду'
    )
    total_area = fields.Integer(string='Загальна площа (кв.м)', compute='_compute_total_area', store=True)
    best_price = fields.Float(string='Найкраща пропозиція', compute='_compute_best_price', store=True)
    active = fields.Boolean(string='Активний', default=True)

    state = fields.Selection([
        ('new', 'Новий'),
        ('offer_received', 'Отримано пропозицію'),
        ('offer_accepted', 'Пропозицію прийнято'),
        ('sold', 'Продано'),
        ('canceled', 'Скасовано')],
        string='Статус',
        required=True,
        copy=False,
        default='new'
    )

    property_type_id = fields.Many2one('estate.property.type', string='Тип нерухомості')
    buyer_id = fields.Many2one('res.partner', string='Покупець', copy=False)
    salesman_id = fields.Many2one('res.users', string='Продавець', default=lambda self: self.env.user)
    offer_ids = fields.One2many('estate.property.offer', 'property_id', string='Пропозиції')
    tag_ids = fields.Many2many('estate.property.tag', string='Теги')

    _sql_constraints = [
        ('check_expected_price_positive', 'CHECK(expected_price > 0)', 'Очікувана ціна повинна бути строго позитивною.'),
        ('check_selling_price_positive', 'CHECK(selling_price >= 0)', 'Ціна продажу повинна бути позитивною.')
    ]

    @api.constrains('expected_price', 'selling_price')
    def _check_price_positive(self):
        for record in self:
            if record.expected_price <= 0:
                raise ValidationError('Очікувана ціна повинна бути строго позитивною.')
            if record.selling_price < 0:
                raise ValidationError('Ціна продажу повинна бути позитивною.')

    @api.constrains('expected_price', 'selling_price')
    def _check_selling_price_minimum(self):
        for record in self:
            if record.selling_price:
                min_acceptable_price = 0.9 * record.expected_price
                if record.selling_price < min_acceptable_price:
                    raise ValidationError("Ціна продажу не може бути нижчою за 90% від очікуваної ціни.")

    @api.depends('offer_ids.price')
    def _compute_best_price(self):
        for record in self:
            record.best_price = max(record.offer_ids.mapped('price'), default=0.0)

    @api.depends('living_area', 'garden_area')
    def _compute_total_area(self):
        for record in self:
            record.total_area = (record.living_area or 0) + (record.garden_area or 0)

    @api.onchange('garden')
    def _onchange_garden(self):
        if self.garden:
            self.garden_area = 10
            self.garden_orientation = 'north'
        else:
            self.garden_area = 0
            self.garden_orientation = False

    @api.onchange('offer_ids')
    def _onchange_offer_ids(self):
        if self.offer_ids:
            self.state = 'offer_received'

    def action_cancel(self):
        for record in self:
            if record.state == 'sold':
                raise ValidationError("Проданий об'єкт не можна скасувати.")
            record.state = 'canceled'

    def action_set_sold(self):
        """
        Оновлення статусу та створення рахунку для проданого об'єкта нерухомості.
        """
        for record in self:
            if record.state == 'canceled':
                raise ValidationError("Скасований об'єкт не можна продати.")
            record.state = 'sold'
            if record.best_price:
                record.selling_price = record.best_price
                accepted_offer = record.offer_ids.filtered(
                    lambda o: o.price == record.best_price and o.status == 'accepted')
                if accepted_offer:
                    record.buyer_id = accepted_offer.partner_id

            # Перевіряємо наявність покупця
            if not record.buyer_id:
                raise UserError("Необхідно вказати покупця перед продажем об'єкта.")

            # Створюємо рахунок
            journal = self.env['account.journal'].search([('type', '=', 'sale')], limit=1)
            if not journal:
                raise UserError("Не знайдено журнал продаж. Перевірте налаштування рахунків.")

            # Используем любой доступный счет для учетных записей
            account = self.env['account.account'].search([], limit=1)
            if not account:
                raise UserError("Не знайдено жодного облікового рахунку. Будь ласка, налаштуйте хоча б один рахунок.")

            invoice_vals = {
                'move_type': 'out_invoice',  # Рахунок клієнта
                'partner_id': record.buyer_id.id,  # Покупець
                'journal_id': journal.id,  # Журнал рахунків
                'invoice_date': fields.Date.context_today(self),  # Дата рахунку
                'invoice_line_ids': [
                    (0, 0, {
                        'name': f'Продаж нерухомості: {record.name} (Комісія 6%)',  # Опис товару/послуги
                        'quantity': 1,  # Кількість одиниць
                        'price_unit': record.selling_price * 0.06,  # 6% від ціни продажу
                        'account_id': account.id,  # Основний обліковий рахунок
                    }),
                    (0, 0, {
                        'name': 'Адміністративний збір',  # Опис послуги
                        'quantity': 1,  # Кількість
                        'price_unit': 100.00,  # Фіксований адміністративний збір
                        'account_id': account.id,  # Основний обліковий рахунок
                    }),
                ],
            }

            invoice = self.env['account.move'].create(invoice_vals)

            # Додаємо повідомлення на об'єкт нерухомості
            record.message_post(
                body=f"Створено рахунок на продаж: <a href=# data-oe-model='account.move' data-oe-id='{invoice.id}'>Натисніть для перегляду рахунку</a>"
            )

    @api.ondelete(at_uninstall=False)
    def _prevent_deletion_if_not_new_or_canceled(self):
        for record in self:
            if record.state not in ['new', 'canceled']:
                raise ValidationError(
                    "Видаляти можна тільки об'єкти, що перебувають у стані 'Новий' або 'Скасовано'."
                )
