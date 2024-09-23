from odoo import models, fields, api
from odoo.exceptions import UserError

class EstateProperty(models.Model):
    _inherit = 'estate.property'

    def action_set_sold(self):
        """
        Перевизначення методу для створення рахунку при продажі об'єкта нерухомості.
        """
        super(EstateProperty, self).action_set_sold()  # Викликаємо оригінальний метод

        for record in self:
            if not record.buyer_id:
                raise UserError("Необхідно вказати покупця перед продажем об'єкта.")

            # Убираем проверку счета
            # account = self.env['account.account'].search([('code', '=', '1010')], limit=1)
            # if not account:
            #     account = self.env['account.account'].search([], limit=1)
            #     if not account:
            #         raise UserError("Не знайдено жодного облікового рахунку. Будь ласка, налаштуйте хоча б один рахунок.")

            # Створюємо дані для рахунку без привязки к конкретному счету
            invoice_vals = {
                'move_type': 'out_invoice',
                'partner_id': record.buyer_id.id,
                'invoice_date': fields.Date.context_today(self),
                'invoice_line_ids': [
                    (0, 0, {
                        'name': f'Продаж нерухомості: {record.name}',
                        'quantity': 1,
                        'price_unit': record.selling_price,
                        # Убираем привязку к account_id
                        # 'account_id': account.id,
                    }),
                    (0, 0, {
                        'name': 'Адміністративний збір',
                        'quantity': 1,
                        'price_unit': 100.00,
                        # 'account_id': account.id,
                    })
                ],
            }

            # Створюємо рахунок
            invoice = self.env['account.move'].create(invoice_vals)

            # Додаємо повідомлення на об'єкт нерухомості
            record.message_post(
                body=f"Рахунок на продаж створено: <a href=# data-oe-model='account.move' data-oe-id='{invoice.id}'>Натисніть для перегляду рахунку</a>"
            )
