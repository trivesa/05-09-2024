# -*- coding: utf-8 -*-
# Part of BrowseInfo. See LICENSE file for full copyright and licensing details.

from odoo import http
from odoo.http import request
from odoo.addons.web.controllers.main import content_disposition
import base64
import os, os.path
import csv
from os import listdir
import sys

class Download_xls(http.Controller):
    
    @http.route('/web/binary/download_document', type='http', auth="public")
    def download_document(self,model,id, **kw):

        Model = request.env[model]
        res = Model.browse(int(id)).sudo()

        if res.with_variant == True:

            invoice_xls = request.env['ir.attachment'].sudo().search([('name','=','product_with_variant.xls')])
            filecontent = invoice_xls.datas
            filename = 'product_with_variant.xls'
            filecontent = base64.b64decode(filecontent)

        elif res.with_variant == False:

            invoice_xls = request.env['ir.attachment'].sudo().search([('name','=','product.xls')])
            filecontent = invoice_xls.datas
            filename = 'product.xls'
            filecontent = base64.b64decode(filecontent)
            

        return request.make_response(filecontent,
            [('Content-Type', 'application/octet-stream'),
            ('Content-Disposition', content_disposition(filename))])
        
        
        