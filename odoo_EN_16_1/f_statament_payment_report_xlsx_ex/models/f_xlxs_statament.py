# -*- coding: utf-8 -*-

from odoo import models, tools, api, fields, _

from datetime import datetime, timedelta, date
from odoo.tools import DEFAULT_SERVER_DATE_FORMAT
from odoo.http import request
from collections import defaultdict
import logging

_logger = logging.getLogger(__name__)


class FxlsReportCustStatement(models.AbstractModel):
    _name = 'report.f_statament_payment_report_xlsx_ex.freport_detial_xls'
    _description = "Statement Payment Report xls"

    _inherit = ["report.report_xlsx.abstract"]
    
    
    def f_get_level2_path(self,categ):
        """
        Returns the category path up to 2 levels:
        root/child
        If deeper (like root/child/grandchild), it will be rolled up to root/child.
        """
        if not categ:
            return "غير مصنف"
    
        path_parts = []
        current = categ
    
        while current:
            path_parts.insert(0, current.name)
            current = current.parent_id
    
        # Example: ['all', 'a', 'd'] → keep only first 2: ['all','a']
        if len(path_parts) > 2:
            path_parts = path_parts[:2]
    
        return "/".join(path_parts)

    
    
    
    def get_product_name(self,rec_id,product_id):

                        return ''



    def get_categ_detaiks(self,sheet_new,row_number,column_number,format5,format9,summary_data):
        print('pass')
        
                        

                        
    
    
    
    

    def generate_xlsx_report(self, workbook, data, partners):
        wizard_record = request.env['f.detailed.customer'].search([])[-1]
        # self = self.with_context(lang=wizard_record.lang)

        total_stat_vals = self.env['report.f_customer_detailed_statement.freport_detial'].get_total_stat(
            wizard_record.from_date, wizard_record.to_date, wizard_record.partner_id.id, wizard_record.account_type)
        aging_details_vals = self.env['report.f_customer_detailed_statement.freport_detial'].get_aging_data(
            wizard_record.from_date, wizard_record.to_date, wizard_record.partner_id.id)
        checks_vlas = self.env['report.f_customer_detailed_statement.freport_detial'].get_check_endorsed_data(
            wizard_record.from_date, (wizard_record.to_date).strftime("%Y-%m-%d"), wizard_record.partner_id.id)

        partner = self.env['res.partner'].search([('id', '=', wizard_record.partner_id.id)])
        f_statment_ids = self.env['f.customer.detailed.report'].search(
            [('partner_id', '=', wizard_record.partner_id.id)])

        report_date = datetime.now().strftime("%Y-%m-%d"),

        company = self.env.company.name,

        format1 = workbook.add_format({'font_size': 22, 'bg_color': '#D3D3D3'})
        format4 = workbook.add_format({'font_size': 22})
        format2 = workbook.add_format({'font_size': 12, 'bold': True, 'bg_color': '#D3D3D3'})
        format3 = workbook.add_format({'align': 'right', 'font_size': 12, 'bg_color': '#D0D1FF', 'bold': True})
        format5 = workbook.add_format({'align': 'right', 'font_size': 10, 'bg_color': '#D3D3D3', 'bold': True})
        format7 = workbook.add_format({'font_size': 10, 'bg_color': '#FFFFFF'})
        format6 = workbook.add_format({'font_size': 22, 'bg_color': '#FFFFFF'})
        format9 = workbook.add_format({'font_size': 12})
        format10 = workbook.add_format({'font_size': 12, 'bg_color': 'green'})
        format11 = workbook.add_format({'font_size': 14, 'bg_color': 'yellow'})
        format18 = workbook.add_format({'font_size': 10, 'bg_color': 'yellow', 'align': 'center', 'bold': True})
        format12 = workbook.add_format({'font_size': 10})
        format14 = workbook.add_format({'font_size': 10})
        format12.set_align('center')
        format13 = workbook.add_format(
            {'font_size': 10, 'num_format': 'yyyy-mm-dd', 'bg_color': '#D0D1FF', 'bold': True})
        format30 = workbook.add_format({'font_size': 10, 'num_format': 'yyyy-mm-dd', 'align': 'center', 'bold': True})
        format19 = workbook.add_format({'font_size': 10, 'num_format': 'yyyy-mm-dd'})
        format22 = workbook.add_format({'font_size': 10, 'align': 'center', 'bg_color': '#D3D3D3', 'bold': True})
        format20 = workbook.add_format({'font_size': 10, 'align': 'center', 'bold': True})
        format28 = workbook.add_format({'font_size': 10, 'bold': True})

        row_number = 0
        column_number = 0

        sheet_new = workbook.add_worksheet(" تقرير كشف حساب العميل")
        sheet_new.right_to_left()
        sheet_new.write('B1', "كشف حساب", format28)

        sheet_new.write('A2', ": العميل", format5)
        sheet_new.write('B2', partner.name, format5)

        sheet_new.write('A3', ": المدينة", format5)
        sheet_new.write('B3', partner.city, format5)

        sheet_new.write('A4', ": مرجع العميل", format5)
        sheet_new.write('B4', partner.ref, format5)

        sheet_new.write('D2', ": التاريخ", format5)
        sheet_new.write('E2', report_date[0], format13)

        sheet_new.write('D3', ": الفترة", format5)
        sheet_new.write('E3', wizard_record.from_date, format13)
        sheet_new.write('D4', "الى", format5)
        sheet_new.write('E4', wizard_record.to_date, format13)

        sheet_new.write('A7', ": الرصيد الافتتاحي", format5)
        sheet_new.write('B7', total_stat_vals['opening_balance'], format5)

        sheet_new.write('D7', ": مدين", format5)
        sheet_new.write('E7', total_stat_vals['debt'], format5)

        sheet_new.write('D8', ": دائن", format5)
        sheet_new.write('E8', total_stat_vals['credit'], format5)

        sheet_new.write('A8', ": الرصيد", format5)
        sheet_new.write('B8', total_stat_vals['balance'], format5)

        

        row_number = 11
        column_number = 0

        sheet_new.write(row_number, column_number, "التاريخ", format11)
        sheet_new.write(row_number, column_number + 2, "المرجع", format11)
        sheet_new.write(row_number, column_number + 1, "نوع الحركة", format11)
        sheet_new.write(row_number, column_number + 3, "المبلغ/العملة", format11)
        sheet_new.write(row_number, column_number + 4, "مدين", format11)
        sheet_new.write(row_number, column_number + 5, "دائن", format11)
        sheet_new.write(row_number, column_number + 6, "الرصيد", format11)
        sheet_new.write(row_number, column_number + 7, "العملة", format11)
        sheet_new.write(row_number, column_number + 8, "ملاحظات", format11)

        row_number += 1

        summary_data = {}

        for z in f_statment_ids.with_context(lang=wizard_record.lang):
            sheet_new.write(row_number, column_number, z.f_report_date, format13)
            sheet_new.write(row_number, column_number+2, z.ref, format3)
            type = ''
            if z.sudo().type == 'out_invoice':
                type = 'فاتورة عميل'
            elif z.sudo().type == 'in_invoice':
                type = 'فاتورة مورد'
            elif z.sudo().type == 'out_refund':
                type = 'إشعار دائن للعميل '
            elif z.sudo().type == 'in_refund':
                type = 'إشعار المورد الدائن '
            elif z.sudo().type == 'entry':
                type = 'قيد اليومية'
            elif z.sudo().type == 'out_receipt':
                type = 'إيصال المبيعات '
            elif z.sudo().type == 'in_receipt':
                type = 'إيصال الشراء'
            elif z.sudo().type == 'beg_bal':
                type = 'الرصيد الافتتاحي'
            elif z.sudo().type == 'inbound':
                type = 'سندات القبض'
            elif z.sudo().type == 'outbound':
                type = 'دفعات الموردين'
            elif z.sudo().type == 'pos_order':
                type = 'POS Order'
            elif z.sudo().type == 'pos_paym':
                type = 'POS Payment'

            sheet_new.write(row_number, column_number + 1, type, format3)
            sheet_new.write(row_number, column_number + 3, z.sudo().amount_cuurency, format3)
            sheet_new.write(row_number, column_number + 4, z.sudo().debt, format3)
            sheet_new.write(row_number, column_number + 5, z.sudo().credit, format3)
            sheet_new.write(row_number, column_number + 6, z.sudo().acum_balance, format3)
            sheet_new.write(row_number, column_number + 7, z.sudo().currency_id.symbol, format3)
            note = z.sudo().f_note
            if z.sudo().f_note == False:
                note = z.sudo().invoice_id.ref
                if z.sudo().invoice_id.ref == False:
                    note = ''
            
            sheet_new.write(row_number, column_number + 8, note, format3)

            if wizard_record.include_payment_details and z.sudo().multi_pay_id:
                row_number += 1
                sheet_new.write(row_number, column_number, "دفتر اليومية", format5)
                sheet_new.write(row_number, column_number + 1, "رقم الشيك", format5)
                sheet_new.write(row_number, column_number + 2, "تاريخ الستحقاق", format5)
                sheet_new.write(row_number, column_number + 3, "المبلغ", format5)

                if wizard_record.include_payment_details and z.sudo().multi_pay_id and z.sudo().multi_pay_id.f_payment_type == 'inbound':
                    for rec in z.sudo().multi_pay_id.f_payment_lines:
                        if rec.currency_id.id == z.sudo().currency_id.id:
                            row_number += 1
                            sheet_new.write(row_number, column_number, rec.journal_id.name, format9)
                            sheet_new.write(row_number, column_number + 1, rec.check_number, format9)
                            sheet_new.write(row_number, column_number + 2, rec.due_date, format30)
                            sheet_new.write(row_number, column_number + 3, rec.amount, format9)

                if wizard_record.include_payment_details and z.sudo().multi_pay_id and z.sudo().multi_pay_id.f_payment_type == 'outbound':
                    for rec in z.sudo().multi_pay_id.f_payment_lines_v:
                        if rec.currency_id.id == z.sudo().currency_id.id:
                            row_number += 1
                            sheet_new.write(row_number, column_number, rec.journal_id.name, format9)
                            sheet_new.write(row_number, column_number + 1, rec.check_number, format9)
                            sheet_new.write(row_number, column_number + 2, rec.due_date, format30)
                            sheet_new.write(row_number, column_number + 3, rec.amount, format9)

            if wizard_record.include_details and z.sudo().journal_id.type in (
            'sale', 'purchase') and z.sudo().invoice_id.invoice_line_ids and not z.sudo().invoice_id.returned_check_id:
                row_number += 1
                sheet_new.write(row_number, column_number, "المرجع", format5)
                sheet_new.write(row_number, column_number + 1, "المنتج", format5)
                sheet_new.write(row_number, column_number + 2, "الكمية", format5)
                sheet_new.write(row_number, column_number + 3, "السعر", format5)
                sheet_new.write(row_number, column_number + 4, "خصم%", format5)
                sheet_new.write(row_number, column_number + 5, "المبلغ", format5)

                for rec in z.sudo().invoice_id.invoice_line_ids:

                    invoice_date = z.sudo().invoice_id.invoice_date or z.sudo().invoice_id.date
                    if not invoice_date:
                            continue
                    month_key = invoice_date.strftime("%Y-%m")
                    categ_path = self.f_get_level2_path(rec.product_id.categ_id)
                
                    if not summary_data.get(month_key):
                        summary_data[month_key] = {}
                
                    if not summary_data[month_key].get(categ_path):
                        summary_data[month_key][categ_path] = {
                            'categ': categ_path,
                            'qty': rec.quantity,
                        }
                    else:
                        summary_data[month_key][categ_path]['qty'] += rec.quantity

                
                    row_number += 1
                    ref_code = ''
                    if rec.product_id.default_code:
                        ref_code = rec.product_id.default_code

                    sheet_new.write(row_number, column_number, ref_code, format9)
                    #prod_list = list()
                    prod_name = ''
                    if rec.name:
                        prod_name = rec.name
                    else:
                        prod_name = rec.product_id.name

                    if rec.product_id:

                        prod_name  =  prod_name + self.get_product_name(rec.id,rec.product_id.id)

                    sheet_new.write(row_number, column_number + 1, prod_name, format9)
                    sheet_new.write(row_number, column_number + 2, rec.quantity, format9)
                    sheet_new.write(row_number, column_number + 3, rec.price_unit, format9)
                    sheet_new.write(row_number, column_number + 4, rec.discount, format9)
                    sheet_new.write(row_number, column_number + 5, rec.price_total, format9)

            row_number += 1

        row_number += 2
        sheet_new.write(row_number, column_number + 1, "محصلة المدين والدائن في الفترة ", format11)
        sheet_new.write(row_number, column_number + 3, total_stat_vals['debt'], format11)
        sheet_new.write(row_number, column_number + 4, total_stat_vals['credit'], format11)
        sheet_new.write(row_number, column_number + 5, total_stat_vals['balance'], format11)
        row_number += 2

        sheet_new.write(row_number, column_number + 1, 'الرصيد الحالي', format11)
        sheet_new.write(row_number, column_number + 5, total_stat_vals['total_balance'], format11)
        row_number += 1
        sheet_new.write(row_number, column_number + 1, 'الشيكات الغير محصلة الحالية', format11)
        sheet_new.write(row_number, column_number + 5, checks_vlas['sum_endorsed_checks'], format11)

        row_number += 2
        if wizard_record.include_details_aging:
            if aging_details_vals['aging_values']:
                sheet_new.write(row_number, column_number, 'تفاصيل التعمير الحالية ', format11)
                row_number += 2

                sheet_new.write(row_number, column_number, '30-0 ', format3)
                sheet_new.write(row_number, column_number + 1, '60-31 ', format3)
                sheet_new.write(row_number, column_number + 2, '90-61 ', format3)
                sheet_new.write(row_number, column_number + 3, '120-91 ', format3)
                sheet_new.write(row_number, column_number + 4, '150-121 ', format3)
                sheet_new.write(row_number, column_number + 5, '180-150 ', format3)
                sheet_new.write(row_number, column_number + 6, 'اقدم من  180 ', format3)

                row_number += 1
                sheet_new.write(row_number, column_number, aging_details_vals['aging_values'][3], format9)
                sheet_new.write(row_number, column_number + 1, aging_details_vals['aging_values'][4], format9)
                sheet_new.write(row_number, column_number + 2, aging_details_vals['aging_values'][5], format9)
                sheet_new.write(row_number, column_number + 3, aging_details_vals['aging_values'][6], format9)
                sheet_new.write(row_number, column_number + 4, aging_details_vals['aging_values'][7], format9)
                sheet_new.write(row_number, column_number + 5, aging_details_vals['aging_values'][8], format9)
                sheet_new.write(row_number, column_number + 6, aging_details_vals['aging_values'][9], format9)

        row_number += 2
        if wizard_record.include_check_endorsed_details:
            if checks_vlas['checks_end_values']:
                sheet_new.write(row_number, column_number, 'تفاصيل الشيكات', format11)
                row_number += 1
                sheet_new.write(row_number, column_number, 'تاريخ الاستحقاق ', format5)
                sheet_new.write(row_number, column_number + 1, 'رقم الدفعة ', format5)
                sheet_new.write(row_number, column_number + 2, 'البنك ', format5)
                sheet_new.write(row_number, column_number + 3, 'الشيك #', format5)
                sheet_new.write(row_number, column_number + 4, 'حالة الشيك ', format5)
                sheet_new.write(row_number, column_number + 5, 'تاريخ الدفعة ', format5)
                sheet_new.write(row_number, column_number + 6, 'المبلغ /العملة ', format5)
                sheet_new.write(row_number, column_number + 7, ' العملة ', format5)
                sheet_new.write(row_number, column_number + 8, 'رقم الحساب ', format5)

                for rec_check in checks_vlas['checks_end_values']:
                    row_number += 1
                    sheet_new.write(row_number, column_number, checks_vlas['checks_end_values'][rec_check]['date'],
                                    format30)
                    sheet_new.write(row_number, column_number + 1, checks_vlas['checks_end_values'][rec_check]['name'],
                                    format9)
                    sheet_new.write(row_number, column_number + 2, checks_vlas['checks_end_values'][rec_check]['bank'],
                                    format9)
                    sheet_new.write(row_number, column_number + 3,
                                    checks_vlas['checks_end_values'][rec_check]['check_no'], format9)
                    sheet_new.write(row_number, column_number + 4,
                                    checks_vlas['checks_end_values'][rec_check]['check_state'], format9)
                    sheet_new.write(row_number, column_number + 5,
                                    checks_vlas['checks_end_values'][rec_check]['pay_date'], format30)
                    sheet_new.write(row_number, column_number + 6,
                                    checks_vlas['checks_end_values'][rec_check]['amount'], format9)
                    sheet_new.write(row_number, column_number + 7,
                                    checks_vlas['checks_end_values'][rec_check]['currency_name'], format9)
                    sheet_new.write(row_number, column_number + 8,
                                    checks_vlas['checks_end_values'][rec_check]['account_number'], format9)







        
        # Header
        
        row_number += 2
        self.get_categ_detaiks(sheet_new,row_number,column_number,format5,format9,summary_data)






















