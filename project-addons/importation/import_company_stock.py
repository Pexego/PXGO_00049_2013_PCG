#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import xmlrpclib
import socket
import traceback
import xlrd

class import_products(object):
    def __init__(self, dbname, user, passwd, products_file, company_id):
        """método incial"""

        try:
            self.url_template = "http://%s:%s/xmlrpc/%s"
            self.server = "localhost"
            self.port = 9069
            self.dbname = dbname
            self.user_name = user
            self.user_passwd = passwd
            self.products_file = products_file
            self.company_id = int(company_id)

            #
            # Conectamos con OpenERP
            #
            login_facade = xmlrpclib.ServerProxy(self.url_template % (self.server, self.port, 'common'))
            self.user_id = login_facade.login(self.dbname, self.user_name, self.user_passwd)
            self.object_facade = xmlrpclib.ServerProxy(self.url_template % (self.server, self.port, 'object'))

            res = self.import_product()
            #con exito
            if res:
                print ("All imported")
        except Exception, e:
            print ("ERROR: ", (e))
            sys.exit(1)

        #Métodos Xml-rpc

    def exception_handler(self, exception):
        """Manejador de Excepciones"""
        print "HANDLER: ", (exception)
        return True

    def create(self, model, data, context={}):
        """
        Wrapper del metodo create.
        """
        try:
            res = self.object_facade.execute(self.dbname, self.user_id, self.user_passwd,
                                                            model, 'create', data, context)
            return res
        except socket.error, err:
            raise Exception(u'Conexion rechazada: %s!' % err)
        except xmlrpclib.Fault, err:
            raise Exception(u'Error %s en create: %s' % (err.faultCode, err.faultString))


    def search(self, model, query, offset=0, limit=False, order=False, context={}, count=False, obj=1):
        """
        Wrapper del metodo search.
        """
        try:
            ids = self.object_facade.execute(self.dbname, self.user_id, self.user_passwd,
                                    model, 'search', query, offset, limit, order, context, count)
            return ids
        except socket.error, err:
                raise Exception(u'Conexion rechazada: %s!' % err)
        except xmlrpclib.Fault, err:
                raise Exception(u'Error %s en search: %s' % (err.faultCode, err.faultString))


    def read(self, model, ids, fields, context={}):
        """
        Wrapper del metodo read.
        """
        try:
            data = self.object_facade.execute(self.dbname, self.user_id, self.user_passwd,
                                            model, 'read', ids, fields, context)
            return data
        except socket.error, err:
                raise Exception(u'Conexion rechazada: %s!' % err)
        except xmlrpclib.Fault, err:
                raise Exception(u'Error %s en read: %s' % (err.faultCode, err.faultString))


    def write(self, model, ids, field_values,context={}):
        """
        Wrapper del metodo write.
        """
        try:
            res = self.object_facade.execute(self.dbname, self.user_id, self.user_passwd,
                                                    model, 'write', ids, field_values, context)
            return res
        except socket.error, err:
                raise Exception(u'Conexion rechazada: %s!' % err)
        except xmlrpclib.Fault, err:
                raise Exception(u'Error %s en write: %s' % (err.faultCode, err.faultString))


    def unlink(self, model, ids, context={}):
        """
        Wrapper del metodo unlink.
        """
        try:
            res = self.object_facade.execute(self.dbname, self.user_id, self.user_passwd,
                                                    model, 'unlink', ids, context)
            return res
        except socket.error, err:
                raise Exception(u'Conexion rechazada: %s!' % err)
        except xmlrpclib.Fault, err:
                    raise Exception(u'Error %s en unlink: %s' % (err.faultCode, err.faultString))

    def default_get(self, model, fields_list=[], context={}):
        """
        Wrapper del metodo default_get.
        """
        try:
            res = self.object_facade.execute(self.dbname, self.user_id, self.user_passwd,
                                        model, 'default_get', fields_list, context)
            return res
        except socket.error, err:
                raise Exception('Conexion rechazada: %s!' % err)
        except xmlrpclib.Fault, err:
                raise Exception('Error %s en default_get: %s' % (err.faultCode, err.faultString))

    def execute(self, model, method, *args, **kw):
        """
        Wrapper del método execute.
        """
        try:
            res = self.object_facade.execute(self.dbname, self.user_id, self.user_passwd,
                                                                model, method, *args, **kw)
            return res
        except socket.error, err:
                raise Exception('Conexión rechazada: %s!' % err)
        except xmlrpclib.Fault, err:
                raise Exception('Error %s en execute: %s' % (err.faultCode, err.faultString))

    def exec_workflow(self, model, signal, ids):
        """ejecuta un workflow por xml rpc"""
        try:
            res = self.object_facade.exec_workflow(self.dbname, self.user_id, self.user_passwd, model, signal, ids)
            return res
        except socket.error, err:
            raise Exception(u'Conexión rechazada: %s!' % err)
        except xmlrpclib.Fault, err:
            raise Exception(u'Error %s en exec_workflow: %s' % (err.faultCode, err.faultString))

    def _get_location_id(self, location_code):
        area = ""
        rest = ""
        for character in location_code:
            if character.isdigit():
                rest += character
            else:
                area += character
        if not rest:
            location_id = self.search("stock.location", [('name', '=', area)])
        elif location_code == 'NAV2':
            location_id = self.search("stock.location", [('name', '=', location_code)])
        else:
            stage = rest[-1]
            location_id = self.search("stock.location", [('name', '=', stage),('location_id.name', '=', rest[:-1]),('location_id.location_id.name','=',area)])
        if not location_id:
            raise Exception("Any location with code %s" % location_code)
        return location_id[0]

    def _get_supplier_by_name(self, supplier_name):
        supplier_ids = self.search("res.partner", [("name",'=',supplier_name)])
        return supplier_ids and supplier_ids[0] or False

    def import_product(self):
        pwb = xlrd.open_workbook(self.products_file, encoding_override="utf-8")
        sh = pwb.sheet_by_index(0)
        inventory = False

        def_supplier_tax = self.search("account.tax", [("name", '=', "P_IVA21_BC")])
        company_data = self.read("res.company", self.company_id, ["name"])
        cont = 1
        all_lines = sh.nrows - 1
        print "products no: ", all_lines
        for rownum in range(1, all_lines):
            record = sh.row_values(rownum)
            try:
                product_ids = self.search('product.product', [('default_code', '=', str(int(record[0])))])
                if not product_ids:
                    raise Exception("No product with code %s" % record[0])
                else:
                    product_id = product_ids[0]
                product_data = self.read('product.product', product_id, ['description', "uom_id"])
                new_note = product_data['description'] or ""
                if record[4]:
                    if new_note:
                        new_note += u"\nEquipo: " + record[4]
                    else:
                        new_note = u"Equipo: " + record[4]
                vals = {
                    'description': new_note,
                    'standard_price': (record[9] or 1.0),
                    "cost_method": "average",
                    "supplier_taxes_id": [(6, 0, def_supplier_tax)],
                }
                self.write('product.product', [product_id], vals)
                if record[11] and record[5]:
                    if not inventory:
                        inventory = self.create("stock.inventory", {
                            'name': u"Stock Inicial " + company_data["name"],
                            "company_id": self.company_id
                        })
                    location_code = record[5].split(";")[0]
                    inventory_line_vals = {
                        "inventory_id": inventory,
                        "product_id": product_id,
                        "product_qty": record[11],
                        "product_uom_id": product_data["uom_id"][0],
                        "location_id": self._get_location_id(location_code)
                    }
                    self.create("stock.inventory.line", inventory_line_vals)


                if record[7]:
                    suppliers = record[7].split(";")
                    refs = record[6].split(";")
                    if not refs:
                        for supp in suppliers:
                            refs.append("")
                    product_data = self.read("product.product", product_id, ["product_tmpl_id"])
                    for elem in zip(suppliers,refs):
                        supplier_id = self._get_supplier_by_name(elem[0])
                        if supplier_id:
                            supplier_vals = {
                                "name": supplier_id,
                                "product_code": elem[1],
                                "product_tmpl_id": product_data["product_tmpl_id"][0],
                                "company_id": False,
                                "principal_supplier": True
                            }
                            self.create("product.supplierinfo", supplier_vals)
                if record[13]:
                    warehouse_ids = self.search("stock.warehouse", [('company_id','=',self.company_id)])
                    warehouse_data = self.read("stock.warehouse", warehouse_ids[0], ["lot_stock_id"])
                    self.create("stock.warehouse.orderpoint",
                                {'product_id': product_id,
                                 'company_id': self.company_id,
                                 'product_max_qty': record[13],
                                 'product_min_qty': 0.0,
                                 'warehouse_id': warehouse_ids[0],
                                 'location_id': warehouse_data['lot_stock_id'][0]})


                print "%s de %s" % (cont, all_lines)
                cont += 1
            except Exception, e:
                print "EXCEPTION: REC: ",(record, e)
                import ipdb; ipdb.set_trace()

        if inventory:
            self.execute("stock.inventory", "prepare_inventory", [inventory])
            self.execute("stock.inventory", "action_done", [inventory])

        return True


if __name__ == "__main__":
    if len(sys.argv) < 5:
        print u"Uso: %s <dbname> <user> <password> <products.xls> <company_id>" % sys.argv[0]
    else:
        import_products(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4], sys.argv[5])
