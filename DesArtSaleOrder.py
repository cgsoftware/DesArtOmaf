# -*- encoding: utf-8 -*-

from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
import decimal_precision as dp
import time
import netsvc
import pooler, tools
import math
from tools.translate import _

from osv import fields, osv


class sale_order_line(osv.osv):
   _inherit = "sale.order.line"

   def des_variants(self,cr,uid,product_id,context):
       desvar = ""
       if product_id:            
            product_obj = self.pool.get('product.product')
            riga_art = product_obj.browse(cr, uid, product_id)  
            if riga_art.dimension_value_ids:
                for variante in riga_art.dimension_value_ids:
                    #import pdb;pdb.set_trace()
                    desvar += variante.dimension_id.desc_type+':'+variante.desc_value+' - '
            if riga_art.marchio_ids:
                desvar +=  "Marchio:" + riga_art.marchio_ids.name
       
       return desvar



   def product_id_change(self, cr, uid, ids, pricelist, product, qty=0,
            uom=False, qty_uos=0, uos=False, name='', partner_id=False,
            lang=False, update_tax=True, date_order=False, packaging=False, fiscal_position=False, flag=False):
        res = super(sale_order_line, self).product_id_change( cr, uid, ids, pricelist, product, qty,uom, qty_uos, uos, name, partner_id,lang, update_tax, date_order, packaging, fiscal_position, flag)
        v = res.get('value', False)
        domain = res.get('domain', False)       
        warning = res.get('warning', False)    
        product_id = product
        if product_id:             
            product_obj = self.pool.get('product.product')
            riga_art = product_obj.browse(cr, uid, product_id)   
            if riga_art:
                #import pdb;pdb.set_trace()
                if riga_art.description_sale:
                    if riga_art.variants: 
                     v['name'] = riga_art.name + " - " + self.des_variants(cr, uid, product_id, context=False) + " - " + riga_art.description_sale
                     #+ " - " + riga_art.description_sale
                    else:
                      v['name'] = riga_art.name + " - " + riga_art.description_sale
                      #+ " - " + riga_art.description_sale
                else:
                   if riga_art.variants:
                      v['name'] = riga_art.name + " - " + self.des_variants(cr, uid, product_id, context=False) 
                   else:
                      v['name'] = riga_art.name
        
        return {'value': v, 'domain': domain, 'warning': warning}

sale_order_line()
