from odoo import models, fields, _

class ImageGallery(models.Model):
    _name = 'openacademy.gallery'
    _description = 'Image Gallery'
    _rec_name = 'name'

    name = fields.Char(string=_('Name'), required=True)
    image = fields.Binary(string=_('Image'))