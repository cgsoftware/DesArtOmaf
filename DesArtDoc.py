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


class FiscalDocRighe(osv.osv):
   _inherit = "fiscaldoc.righe"

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

   def onchange_articolo(self, cr, uid, ids, product_id, listino_id, qty, partner_id, data_doc, uom,context):
    v = {}
    res = super(FiscalDocRighe, self).onchange_articolo(cr, uid, ids, product_id, listino_id, qty, partner_id, data_doc, uom,context)
    v = res.get('value', False)
    warning = res.get('warning', False)
    domain = res.get('domain', False)
       
    if product_id:             
            product_obj = self.pool.get('product.product')
            riga_art = product_obj.browse(cr, uid, product_id)   
            if riga_art:
                #import pdb;pdb.set_trace()
                if riga_art.description_sale:
                    if riga_art.variants: 
                     v['descrizione_riga'] = riga_art.name + " - " + self.des_variants(cr, uid, product_id, context=False) + " - " + riga_art.description_sale
                     #+ " - " + riga_art.description_sale
                    else:
                      v['descrizione_riga'] = riga_art.name + " - " + riga_art.description_sale
                      #+ " - " + riga_art.description_sale
                else:
                   if riga_art.variants:
                      v['descrizione_riga'] = riga_art.name + " - " + self.des_variants(cr, uid, product_id, context=False) 
#+ riga_art.variants
                   else:
                      v['descrizione_riga'] = riga_art.name

    return {'value': v, 'domain': domain, 'warning': warning}            
    #return {'value':v}
FiscalDocRighe()
