# -*- coding: utf-8 -*-
from odoo import models, fields, api, _,tools
from datetime import date,datetime

class F_Sale_Order_Line_Inherit_ex(models.Model):
    _inherit = 'sale.order.line'

    def _f_where_pos_query(self):
        login_user_allowed_branches = tuple(self.env.user.f_allowed_branches.ids)
        if len(login_user_allowed_branches) == 1:
            allowed_branches_str = f"({login_user_allowed_branches[0]})"
        else:
            allowed_branches_str = login_user_allowed_branches
        return super(F_Sale_Order_Line_Inherit_ex, self)._f_where_pos_query() + f' AND  pos.f_related_branch in {allowed_branches_str}'
        
        
        
