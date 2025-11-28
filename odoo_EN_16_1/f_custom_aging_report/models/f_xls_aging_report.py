
# -*- coding: utf-8 -*-

from odoo import models, tools, api, fields,_

from datetime import datetime,timedelta,date
from odoo.tools import DEFAULT_SERVER_DATE_FORMAT
from odoo.http import request



class FxlsReportAging(models.AbstractModel):

    _name = 'report.f_custom_aging_report.freport_detial_xls'
    _inherit = ["report.report_xlsx.abstract"]
    _description = "Aging Details xls"

    def generate_xlsx_report(self, workbook, data, partners):
        wizard_record = request.env['f.product.aging'].search([])[-1]

        f_aging_ids = self.env['f.aging.details'].search([('id','!=',False)])

        report_date= datetime.now().strftime("%Y-%m-%d"),

        company =self.env.company.name,


        format1 = workbook.add_format({'font_size': 22, 'bg_color': '#D3D3D3'})
        format4 = workbook.add_format({'font_size': 22})
        format2 = workbook.add_format({'font_size': 12, 'bold': True, 'bg_color': '#D3D3D3'})
        format3 = workbook.add_format({'font_size': 12, 'bg_color': '#D0D1FF', 'bold': True})
        format5 = workbook.add_format({'font_size': 10, 'bg_color': '#D3D3D3', 'bold': True})
        format7 = workbook.add_format({'font_size': 10, 'bg_color': '#FFFFFF'})
        format6 = workbook.add_format({'font_size': 22, 'bg_color': '#FFFFFF'})
        format9 = workbook.add_format({'font_size': 12})
        format10 = workbook.add_format({'font_size': 12, 'bg_color': 'green'})
        format11 = workbook.add_format({'font_size': 14, 'bg_color': 'yellow'})
        format18 = workbook.add_format({'font_size': 10, 'bg_color': 'yellow', 'align': 'center', 'bold': True})
        format12 = workbook.add_format({'font_size': 10})
        format14 = workbook.add_format({'font_size': 10})
        format12.set_align('center')
        format13 = workbook.add_format({'font_size': 10, 'num_format': 'yyyy-mm-dd', 'align': 'center','bg_color': '#D0D1FF', 'bold': True})
        format30 = workbook.add_format({'font_size': 10, 'num_format': 'yyyy-mm-dd', 'align': 'center', 'bold': True})
        format19 = workbook.add_format({'font_size': 10, 'num_format': 'yyyy-mm-dd'})
        format22 = workbook.add_format({'font_size': 10, 'align': 'center', 'bg_color': '#D3D3D3', 'bold': True})
        format20 = workbook.add_format({'font_size': 10, 'align': 'center', 'bold': True})

        row_number = 7
        column_number = 0

        sheet_new = workbook.add_worksheet("Aging Report")

        row_number = 0
        column_number = 0

        days = wizard_record.breakdown_days
        day1 = '0' + ' - ' + str(days)
        day2 = str(days+1) + ' - ' + str(days*2)
        day3 = str(days *2+1) + ' - ' + str(days * 3)
        day4 = str(days * 3 + 1) + ' - ' + str(days * 6)
        day5 = str(days * 6 + 1) + ' - ' + str(days * 8)
        day6 = str(days * 8+ 1) + ' - ' + str(days * 12)
        day7 = '> '+  str(days * 12)

        sheet_new.write(row_number, column_number , "Product", format11)
        sheet_new.write(row_number, column_number + 1, "Barcode", format11)
        sheet_new.write(row_number, column_number + 2, "Ref", format11)
        sheet_new.write(row_number, column_number + 3, "Total Cost", format11)
        sheet_new.write(row_number, column_number + 4, "Total Qty", format11)
        sheet_new.write(row_number, column_number + 5, "Unit Cost", format11)
        sheet_new.write(row_number, column_number + 6, day1, format11)
        sheet_new.write(row_number, column_number + 7, "Interval Cost", format11)

        sheet_new.write(row_number, column_number + 8, day2, format11)
        sheet_new.write(row_number, column_number + 9, "Interval Cost", format11)

        sheet_new.write(row_number, column_number + 10, day3, format11)
        sheet_new.write(row_number, column_number + 11, "Interval Cost", format11)
        sheet_new.write(row_number, column_number + 12, day4, format11)
        sheet_new.write(row_number, column_number + 13, "Interval Cost", format11)
        sheet_new.write(row_number, column_number + 14, day5, format11)
        sheet_new.write(row_number, column_number + 15, "Interval Cost", format11)
        sheet_new.write(row_number, column_number + 16, day6, format11)
        sheet_new.write(row_number, column_number + 17, "Interval Cost", format11)
        sheet_new.write(row_number, column_number + 18, day7, format11)
        sheet_new.write(row_number, column_number + 19, "Interval Cost", format11)

        row_number += 1

        for z in f_aging_ids:
            sheet_new.write(row_number, column_number, z.product_id.name,format9)
            sheet_new.write(row_number, column_number+1, z.barcode, format9)
            sheet_new.write(row_number, column_number + 2, z.default_code, format9)
            sheet_new.write(row_number, column_number + 3, z.total_cost, format9)
            sheet_new.write(row_number, column_number + 4, z.on_hand_quantity, format9)
            sheet_new.write(row_number, column_number + 5, z.product_id.standard_price, format9)
            sheet_new.write(row_number, column_number + 6, z.days, format9)
            sheet_new.write(row_number, column_number + 7, z.cost0, format9)
            sheet_new.write(row_number, column_number + 8, z.days1, format9)
            sheet_new.write(row_number, column_number + 9, z.cost1, format9)
            sheet_new.write(row_number, column_number + 10, z.days2, format9)
            sheet_new.write(row_number, column_number + 11, z.cost2, format9)
            sheet_new.write(row_number, column_number + 12, z.days3, format9)
            sheet_new.write(row_number, column_number + 13, z.cost3, format9)
            sheet_new.write(row_number, column_number + 14, z.days4, format9)
            sheet_new.write(row_number, column_number + 15, z.cost4, format9)
            sheet_new.write(row_number, column_number + 16, z.days5, format9)
            sheet_new.write(row_number, column_number + 17, z.cost5, format9)
            sheet_new.write(row_number, column_number + 18, z.days6, format9)
            sheet_new.write(row_number, column_number + 19, z.cost6, format9)
            row_number += 1

