# -*- coding: utf-8 -*-

from collections import defaultdict
from odoo import models, fields, api, _
from odoo.exceptions import ValidationError


class Product(models.Model):
    _inherit = 'product.product'

    @api.constrains('default_code')
    def _check_default_code_uniqueness(self):
        for rec in self:
            if not rec.default_code:
                raise ValidationError(_("Internal Referance can't be empty"))

        all_default_code = [b for b in self.mapped('default_code') if b]
        domain = [('default_code', 'in', all_default_code)]
        matched_products = self.sudo().search(domain, order='id')
        if len(matched_products) > len(
                all_default_code):
            products_by_ref = defaultdict(list)
            for product in matched_products:
                products_by_ref[product.default_code].append(product)

            duplicates_as_str = "\n".join(
                _("- default_code \"%s\" already assigned to product(s): %s", default_code,
                  ", ".join(p.display_name for p in products))
                for default_code, products in products_by_ref.items() if len(products) > 1
            )
            raise ValidationError(_("default_code(s) already assigned:\n\n%s", duplicates_as_str))

    @api.constrains('barcode')
    def _check_barcode_uniqueness(self):
        for rec in self:
            if not rec.barcode:
                raise ValidationError(_("Barcode can't be empty"))

        """ With GS1 nomenclature, products and packagings use the same pattern. Therefore, we need
        to ensure the uniqueness between products' barcodes and packagings' ones"""
        all_barcode = [b for b in self.mapped('barcode') if b]
        domain = [('barcode', 'in', all_barcode)]
        matched_products = self.sudo().search(domain, order='id')
        if len(matched_products) > len(all_barcode):  # It means that you find more than `self` -> there are duplicates
            products_by_barcode = defaultdict(list)
            for product in matched_products:
                products_by_barcode[product.barcode].append(product)

            duplicates_as_str = "\n".join(
                _("- Barcode \"%s\" already assigned to product(s): %s", barcode,
                  ", ".join(p.display_name for p in products))
                for barcode, products in products_by_barcode.items() if len(products) > 1
            )
            raise ValidationError(_("Barcode(s) already assigned:\n\n%s", duplicates_as_str))

        if self.env['product.packaging'].search(domain, order="id", limit=1):
            raise ValidationError(_("A packaging already uses the barcode"))

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            seq_date = None
            if 'create_date' in vals:
                seq_date = fields.Datetime.context_timestamp(self, fields.Datetime.to_datetime(vals['create_date']))

            seq = self.env['ir.sequence'].next_by_code('product.template.barcode', sequence_date=seq_date)

            vals['barcode'] = seq

            vals['default_code'] = seq

        return super().create(vals_list)

    def generate_barcode_default_code(self):

        domain = [('barcode', '=', False)]

        products = self.env['product.product'].search(domain)

        for product in products:
            seq_date = fields.Datetime.context_timestamp(self, fields.datetime.now())
            seq = self.env['ir.sequence'].next_by_code('product.template.barcode', sequence_date=seq_date)

            product.barcode = seq
            product.default_code = seq

        return True


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    def generate_barcode_default_code(self):
        return self.env['product.product'].generate_barcode_default_code()

