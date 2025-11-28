# See LICENSE file for full copyright and licensing details.
# Part of BrowseInfo. See LICENSE file for full copyright and licensing details.

import tempfile
import binascii
from odoo import models, fields, exceptions, api, _
from io import BytesIO
import re 
import xlsxwriter
import base64, os
from PIL import Image
import io
from zipfile import ZIP_DEFLATED, ZipFile

class ExportProductsImages(models.TransientModel):
    _name = 'export.products.with.images'
    _description = 'Export Products Images'

    is_product_with_image_imformation = fields.Boolean(string = "Product Image with Information")
    is_only_image_into_zip_file = fields.Boolean(string = "Only Image into Zip File")
    is_export_extra_product_images = fields.Boolean(string = "Export Extra Product Images")
    product_ids = fields.Many2many('product.template', string='Product')

    def sanitize_filename(self, filename):
        # Remove spaces and other characters that might cause issues
        return re.sub(r'[^\w\-_. ]', '_', filename)

    def resize_image_data(self, file_path, bound_width_height):
        im = Image.open(file_path)
        im = im.convert('RGB')  # Changed by falak
        im.thumbnail(bound_width_height, Image.ANTIALIAS)
        im_bytes = BytesIO()
        im.save(im_bytes, format='PNG')
        return im_bytes

    def action_export(self):
        self.ensure_one()
        if self.is_product_with_image_imformation == True:
            name_of_file = 'Export Product With Images.xlsx'
            file_path = 'Export Product with Images' + '.xlsx'
            workbook = xlsxwriter.Workbook('/tmp/'+file_path)
            worksheet = workbook.add_worksheet('Export Product with Images')
            header_format = workbook.add_format({'bold': True,'valign':'vcenter','font_size':16,'align': 'center','bg_color':'#D8D8D8'})
            title_format = workbook.add_format({'border': 1,'bold': True, 'valign': 'vcenter','align': 'center', 'font_size':14,'bg_color':'#D8D8D8'})
            cell_wrap_format_bold = workbook.add_format({'bold': True,'valign':'vjustify','valign':'vcenter','align': 'center','font_size':15,'bg_color':'#D8D8D8'})
            cell_wrap_format = workbook.add_format({'valign':'vjustify','valign':'vcenter','align': 'center','font_size':12,})
            cell_wrap_format_center = workbook.add_format({'valign':'vjustify','valign':'vcenter','align': 'center','font_size':12,}) 
            cell_text_wrap_format = workbook.add_format({'text_wrap': True,'valign':'vjustify','valign':'vcenter','align': 'center','font_size':12,})
            cell_text_wrap_format.set_text_wrap()

            header = 'Export Product With Images' 

            worksheet.set_column(0, 0, 20)
            worksheet.set_column(1, 2, 25)
            worksheet.set_column(3, 3, 25)
            worksheet.set_column(4, 4, 17)
            worksheet.set_column(5, 5, 15)
            worksheet.set_column(10, 10, 17)

            product_ids = self.env['product.template'].browse(self._context.get('active_ids', []))
            worksheet.merge_range(1, 0, 0, 5, header,header_format)
            rowscol = 1
            worksheet.set_row(rowscol,20)
            worksheet.write(rowscol + 2, 0, 'Internal Reference', cell_wrap_format_bold)
            worksheet.write(rowscol + 2, 1, 'Product Name', cell_wrap_format_bold)
            worksheet.write(rowscol + 2, 2, 'Category',cell_wrap_format_bold)
            worksheet.write(rowscol + 2, 3, 'Image', cell_wrap_format_bold)
            worksheet.write(rowscol + 2, 4, 'Sale Price', cell_wrap_format_bold)
            worksheet.write(rowscol + 2, 5, 'Cost', cell_wrap_format_bold)
            rows = (rowscol + 3)
            for data in product_ids:
                worksheet.set_row(rows,30)
                worksheet.write(rows, 0, data.default_code or '', cell_wrap_format)
                worksheet.write(rows, 1, data.name or '', cell_text_wrap_format)
                worksheet.write(rows, 2, data.categ_id.complete_name or '', cell_text_wrap_format)
                if data.image_1920:
                    
                    prod_img = BytesIO(base64.b64decode(data.image_1920))
                    image_path = 'product_image_png.png'
                    bound_width_height = (270, 90)
                    image_data = self.resize_image_data(prod_img, bound_width_height)
                    worksheet.insert_image(rows, 3, "product_image.png", {'image_data': image_data,})
                    worksheet.set_row(rows,85)
                worksheet.write(rows, 4, data.list_price or '', cell_text_wrap_format)
                worksheet.write(rows, 5, str('%.2f' % data.standard_price or ''), cell_wrap_format_center)

                worksheet.conditional_format(rows, 3, rows, 7, {'type': 'no_blanks', 'format': cell_wrap_format})

                rows = rows+1
                rowscol = rows

            workbook.close()
            export_id = base64.b64encode(open('/tmp/' + file_path, 'rb+').read())
            result_id = self.env['excel.report'].create({'file': export_id ,'file_name': name_of_file})
                            
            return {
                'name': 'Export Products with Images',
                'view_mode': 'form',
                'res_model': 'excel.report',
                'type': 'ir.actions.act_window',
                'view_type': 'form',
                'res_id': result_id.id,
                'target': 'new',
            }
        if self.is_only_image_into_zip_file == True:
            zip_file_name = '/tmp/Export Product Images.zip'
            if os.path.exists(zip_file_name):
                os.remove(zip_file_name)
            with ZipFile(zip_file_name, 'w', ZIP_DEFLATED) as file:
                product_ids = self.env['product.template'].browse(self._context.get('active_ids', []))
                for product in product_ids:
                    if product.image_1920:
                        image_data = base64.b64decode(product.image_1920)
                        image = Image.open(io.BytesIO(image_data))
                        image.thumbnail((400, 400), Image.ANTIALIAS)
                        image = image.convert('RGB')
                        image_buffer = io.BytesIO()
                        image.save(image_buffer, 'JPEG')
                        prod_name = product.name
                        sanitized_product_name = self.sanitize_filename(prod_name.replace(' ','_'))
                        if product.default_code :
                            file.writestr(f"{product.default_code+sanitized_product_name}.jpeg", image_buffer.getvalue())
                        else :

                            file.writestr(f"{sanitized_product_name}.jpeg", image_buffer.getvalue())

                            # ...
                        if self.is_export_extra_product_images == True:
                            if product.product_template_image_ids:
                                for extra in product.product_template_image_ids:
                                    if extra.image_1920:
                                        image_data = base64.b64decode(extra.image_1920)
                                        image = Image.open(io.BytesIO(image_data))
                                        image.thumbnail((400, 400), Image.ANTIALIAS)
                                        image = image.convert('RGB')

                                        image_buffer = io.BytesIO()
                                        image.save(image_buffer, 'JPEG')
                                        file.writestr(f"{product.name}_{extra.name}.jpeg", image_buffer.getvalue())
                file.close() 

                zip_wizard_record = self.env['excel.report'].create({
                      'file':base64.b64encode(open(zip_file_name, "rb").read()),
                      'file_name':'Export Products Images.zip'}
                        )
                return {
                    'name': 'Export Products with Images',
                    'view_mode': 'form',
                    'res_model': 'excel.report',
                    'type': 'ir.actions.act_window',
                    'view_type': 'form',
                    'res_id': zip_wizard_record.id,
                    'target': 'new',
                }

class ExcelReport(models.TransientModel):
    _name = "excel.report"
    _description = "Excel Report"

    file = fields.Binary("Download File")
    file_name = fields.Char(string="File Name")
