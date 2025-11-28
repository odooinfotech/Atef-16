import json

def migrate(cr, version):
    cr.execute( """ALTER TABLE f_man_plan ADD COLUMN IF NOT EXISTS f_first_employee INTEGER default 2531;""")
    cr.execute("""DELETE FROM f_man_plan_products WHERE f_product_id IS NULL;""")
    cr.execute("""
    INSERT INTO product_template (name,detailed_type,categ_id,uom_id,uom_po_id,tracking,purchase_line_warn)
    VALUES (%s,'product',191,28,28,'none','no-message')
""", [json.dumps({"en_US": "test-manuf"})])

    
    cr.execute( """update f_man_plan_products l 
                set f_product_id = p.id 
                from product_template p ,product_product pp 
                
                where pp.product_tmpl_id = p.id and l.f_product_id is null  and p.name->>'en_US' = 'test-manuf'; """)
    cr.execute( """ALTER TABLE f_man_plan ADD COLUMN IF NOT EXISTS f_sec_employee INTEGER default 2531;""")
    cr.execute( """ALTER TABLE f_man_plan ADD COLUMN IF NOT EXISTS f_third_employee INTEGER default 2531;""")

