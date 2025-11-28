from odoo import models, fields, api, _


class FConfigSettingsInherit(models.TransientModel):
    _inherit = 'res.config.settings'

    f_po_access_based_class = fields.Boolean(string="Classification Access")

    def set_values(self):
        super(FConfigSettingsInherit, self).set_values()
        config_parameters = self.env["ir.config_parameter"].sudo()

        f_po_access_based_class = self.f_po_access_based_class

        config_parameters.sudo().set_param('falak_purchase_logistics.f_po_access_based_class', f_po_access_based_class)
        rule = self.env.ref('falak_purchase_logistics.f_classifications_access_purchase_order')
        rule_shipping = self.env.ref('falak_purchase_logistics.f_classifications_access_purchase_order_shipping')
        rule_planning = self.env.ref('falak_purchase_logistics.f_classifications_access_purchase_order_planning')
        rule.write({'active': f_po_access_based_class})
        rule_shipping.write({'active': f_po_access_based_class})
        rule_planning.write({'active': f_po_access_based_class})

    def get_values(self):
        res = super(FConfigSettingsInherit, self).get_values()

        res.update(
            f_po_access_based_class=self.env["ir.config_parameter"].sudo().get_param(
                'falak_purchase_logistics.f_po_access_based_class')
        )
        print('res', res)
        return res
