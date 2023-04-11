from odoo import models, fields

class ImageGallery(models.Model):
    _name = 'openacademy.gallery'
    _description = 'Image Gallery'
    _rec_name = 'name'

    name = fields.Char(string='Name', required=True)
    image = fields.Binary(string='Image')