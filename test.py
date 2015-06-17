#!/usr/bin/env python
# encoding: utf-8
username = ''
password = ''
code = 'XXX1'
debug = True

from correos.picking import *
from correos.utils import services
import base64
from base64 import decodestring

print "Correos services"
services = services()
print services

with API(username, password, code, debug) as correos_api:
    print "Test connection"
    print correos_api.test_connection()

with Picking(username, password, code, debug) as picking_api:
    print "Send a new picking to Correos - Label PDF"

    data = {}

    data['RemitenteNombre'] = 'Zikzakmedia SL'
    data['RemitenteNif'] = '123456'
    data['RemitenteDireccion'] = 'Sant Jaume 9, Baix Segona'
    data['RemitenteLocalidad'] = u'Vilafranca del Penedes'
    data['RemitenteProvincia'] = 'Barcelona'
    data['RemitenteCP'] = '08720'
    data['RemitenteTelefonocontacto'] = '938902108'
    data['RemitenteEmail'] = 'zikzak@zikzakmedia.com'
    data['DestinatarioNombre'] = u'Raimon Esteve Cusine'
    data['DestinatarioDireccion'] = 'Durruti 1937, 4art 2ona'
    data['DestinatarioLocalidad'] = 'Barcelona'
    data['DestinatarioProvincia'] = 'Barcelona'
    data['DestinatarioCP'] = '08021'
    data['DestinatarioPais'] = 'ES'
    data['DestinatarioTelefonocontacto'] = '612121212'
    data['DestinatarioEmail'] = 'zikzak@zikzakmedia.com'
    data['CodProducto'] = 'S0235'
    data['ReferenciaCliente'] = 'ZZS0001'
    # 'TipoFranqueo': 'FP'
    # 'Valor':
    # 'TipoReembolso':
    # 'Importe':
    # 'NumeroCuenta':
    # 'EntregaExclusivaDestinatario':
    data['Observaciones1'] =  'Testing Correos API - Create picking'

    reference, label, error = picking_api.create(data)
    print "Picking send %s" % reference
    with open("/tmp/correos-label.pdf","wb") as f:
        f.write(decodestring(label))
    print "Generated PDF label in /tmp/correos-label.pdf"

    # Test a shipment with "reembolso"
    data['Reembolso'] = True
    data['TipoReembolso'] = 'RC'
    data['Importe'] = 125.45
    data['NumeroCuenta'] = '00720101930000122351'
    reference, label, error = picking_api.create(data)

    print "Picking Reembolso send %s" % reference
    with open("/tmp/correos-label-reembolso.pdf","wb") as f:
        f.write(decodestring(label))
    print "Generated PDF label in /tmp/correos-label-reembolso.pdf"

    print "Get Label PDF"
    data = {}
    data['CodEnvio'] = reference

    label = picking_api.label(data)
    with open("/tmp/correos-label-2.pdf","wb") as f:
        f.write(decodestring(label))
    print "Generated PDF label in /tmp/correos-label-2.pdf"
