# -*- coding: utf-8 -*-

from collections import defaultdict
from odoo import models, fields, api, _
from odoo.exceptions import ValidationError


class ResPartner(models.Model):
    _inherit = 'res.partner'

    @api.constrains('ref')
    def _check_ref_uniqueness(self):
        if not self.ref:
            raise ValidationError(_("Referance can't be empty"))
        all_ref = [b for b in self.mapped('ref') if b]
        domain = [('ref', 'in', all_ref)]
        matched_contacts = self.sudo().search(domain, order='id')
        if len(matched_contacts) > len(
                all_ref):
            contacts_by_ref = defaultdict(list)
            for contact in matched_contacts:
                contacts_by_ref[contact.ref].append(contact)

            duplicates_as_str = "\n".join(
                _("- ref \"%s\" already assigned to contact(s): %s", ref,
                  ", ".join(c.name for c in contacts))
                for ref, contacts in contacts_by_ref.items() if len(contacts) > 1
            )
            raise ValidationError(_("ref(s) already assigned:\n\n%s", duplicates_as_str))

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            seq_date = None
            if 'create_date' in vals:
                seq_date = fields.Datetime.context_timestamp(self, fields.Datetime.to_datetime(vals['create_date']))
            vals['ref'] = self.env['ir.sequence'].next_by_code('res.partner.ref', sequence_date=seq_date) or _('New')

        return super().create(vals_list)
