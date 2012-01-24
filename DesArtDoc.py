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

   def onchange_articolo(self, cr, uid, ids, product_id, listino_id, qty, partner_id, data_doc, uom):
    v = {}
    if product_id:    
        #import pdb;pdb.set_trace()
        partner_obj = self.pool.get("res.partner")
        if partner_id:
            lang = partner_obj.browse(cr, uid, partner_id).lang
        context = {'lang': lang, 'partner_id': partner_id}
        v = {}
        if product_id:            
            product_obj = self.pool.get('product.product')
            riga_art = product_obj.browse(cr, uid, product_id)   
            if riga_art:
                # import pdb;pdb.set_trace()
                if riga_art.description_sale:
                    if riga_art.variants: 
                     v['descrizione_riga'] = riga_art.name + " - " + self.des_variants(cr, uid, product_id, context) + " - " + riga_art.description_sale
                     #+ " - " + riga_art.description_sale
                    else:
                      v['descrizione_riga'] = riga_art.name + " - " + riga_art.description_sale
                      #+ " - " + riga_art.description_sale
                else:
                   if riga_art.variants:
                      v['descrizione_riga'] = riga_art.name + " - " + self.des_variants(cr, uid, product_id, context) 
#+ riga_art.variants
                   else:
                      v['descrizione_riga'] = riga_art.name
                    
                v['product_uom'] = riga_art.uom_id.id
                #import pdb;pdb.set_trace()
                if riga_art.property_account_income:
                    v['contropartita'] = riga_art.property_account_income.id
                else:
                    v['contropartita'] = riga_art.categ_id.property_account_income_categ.id
                righe_tasse_articolo = self.pool.get('account.fiscal.position').map_tax(cr, uid, False, riga_art.taxes_id)
                if righe_tasse_articolo: 
                    v['codice_iva'] = righe_tasse_articolo[0]
                
                # determina il prezzo
                
                dati_prz = self.determina_prezzo_sconti(cr, uid, ids, product_id, listino_id, qty, partner_id, uom, data_doc)
                
                v['product_prezzo_unitario'] = dati_prz['prezzo']
                v['discount_riga'] = dati_prz['sconto']
                #import pdb;pdb.set_trace()                 
                v['sconti_riga'] = dati_prz['StringaSconto']
            else:
                v['discount_riga'] = 0.0
            v['prezzo_netto'] = self.calcola_netto(cr, uid, ids,v['product_prezzo_unitario'], v['discount_riga']) 
            v['totale_riga'] = self.totale_riga(qty, v['prezzo_netto'])   

            
    return {'value':v}
FiscalDocRighe()
