from odoo import models, fields

class DiseaseDirectory(models.Model):
    _name = 'hospital.disease.directory'
    _description = 'Disease Directory'
    _parent_name = 'parent_id'

    disease_name = fields.Char(string='Disease Name', required=True)
    parent_id = fields.Many2one('hospital.disease.directory', string='Parent Disease Type', ondelete='cascade')
    child_ids = fields.One2many('hospital.disease.directory', 'parent_id', string='Subtypes')
    is_category = fields.Boolean(string='Is Category?', default=False)

    def name_get(self):
        res = []
        for record in self:
            name = record.disease_name
            res.append((record.id, name))
        return res
