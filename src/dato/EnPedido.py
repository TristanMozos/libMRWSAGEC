# -*- coding: utf-8 -*-
'''
Created on 27 dic. 2016

@author:     Tristán Mozos Pérez

@copyright:  2017 Halltic eSolutions S.L. All rights reserved.

@license:    GPLv3 - http://www.gnu.org/copyleft/gpl.html

This file is part of libMRWSAGEC.

libMRWSAGEC is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

libMRWSAGEC is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with libMRWSAGEC.  If not, see <http://www.gnu.org/licenses/>.

@contact: tristan.mozos@halltic.com

'''
from src.dato.EnComun import Precio

class Pedido(object):
    
    def __init__(self, idExterno='', tipoEnvio=0, canalVenta='', importePedido='', monedaPedido='', numArticulos=0, listProduc=None,
                 NIF_DR=None, nombre_DR=None, email_DR = None, telefono_DR=None,
                 tipoVia_DR='', nombreVia_DR='', numVia_DR='', otrosDatos_DR='', codPostal_DR='', ciudad_DR='', region_DR='', codPais_DR='',
                 contacto_DR = None, aLaAtencionDe_DR = None, horario_DR= None, observaciones_DR = None,
                 NIF_DE=None, nombre_DE=None, email_DE = None, telefono_DE=None,
                 tipoVia_DE='', nombreVia_DE='', numVia_DE='', otrosDatos_DE='', codPostal_DE='', ciudad_DE='', region_DE='', codPais_DE='',
                 contacto_DE = None, aLaAtencionDe_DE = None, horario_DE= None, observaciones_DE = None,
                 fecha='', numAlbaran='', referencia = "", enFranquicia = '', codigoServicio='', numBultos = '', peso = "", entregaSabado = '', 
                 entregaPartirDe = '', horario = None, tramoHorario = '', notificaciones=None):
        '''
        Constructor
        '''
        'IdExterno del pedido'
        self.idExterno = idExterno
        'Tipo Envío (Estándar o Urgente)'
        self.tipoEnvio=tipoEnvio
        'Canal de venta del pedido (Amazon.es, Amazon.fr, eBay...)'
        self.canalVenta = canalVenta
        'Precio total del pedido'
        self.precio = Precio(importePedido, monedaPedido) 
        'Número de artículos del pedido'
        self.numArticulos=numArticulos
        'Lista con los productos del pedido'
        self.productos=listProduc
        'Datos de recogida, remitente y dirección'
        self.datosRecogida=DatosCliente(NIF=NIF_DR, nombre=nombre_DR, email=email_DR, telefono=telefono_DR, 
                                        tipoVia=tipoVia_DR, nombreVia=nombreVia_DR, numVia=numVia_DR, otrosDatos=otrosDatos_DR, codPostal=codPostal_DR, ciudad=ciudad_DR, region=region_DR, codPais=codPais_DR,
                                        contacto=contacto_DR, aLaAtencionDe=aLaAtencionDe_DR, horario=horario_DR, observaciones=observaciones_DR)
        'Datos de envío, destinatario y dirección'
        self.datosEnvio=DatosCliente(NIF=NIF_DE, nombre=nombre_DE, email=email_DE, telefono=telefono_DE,
                                     tipoVia=tipoVia_DE, nombreVia=nombreVia_DE, numVia=numVia_DE, otrosDatos=otrosDatos_DE, codPostal=codPostal_DE, ciudad=ciudad_DE, region=region_DE, codPais=codPais_DE,
                                     contacto=contacto_DE, aLaAtencionDe=aLaAtencionDe_DE, horario=horario_DE, observaciones=observaciones_DE)
        'Datos del servicio'
        self.datosServicio = DatosServicio(fecha=fecha, numAlbaran=numAlbaran, referencia=referencia, enFranquicia=enFranquicia, 
                                           codigoServicio=codigoServicio, numBultos=numBultos, peso=peso, entregaSabado=entregaSabado, 
                                           entregaPartirDe=entregaPartirDe, horario=horario, tramoHorario=tramoHorario, notificaciones=notificaciones)
    
class DatosCliente():
    '''
    Clase que va a tener los datos personales de la persona, así como la dirección
    '''
    def __init__(self, 
                 NIF=None, nombre=None, email = None, telefono=None,
                 tipoVia='', nombreVia='', numVia='', otrosDatos='', codPostal='', ciudad='', region='', codPais='',
                 contacto = None, aLaAtencionDe = None, horario= None, observaciones = None):
        
        self.datosPersonales = DatosPersonales()
        self.direccion = Direccion()
        self.datosPersServicio = DatosPersonalesServicio()
        
class DatosPersonales(object):
    
    def __init__(self, NIF=None, nombre=None, email = None, telefono=None):
        'Nombre completo'
        self.nombre=nombre
        'NIF'
        self.NIF=NIF
        'Email'
        self.email = email        
        'Teléfono'
        self.telefono=telefono
        
class Direccion(object):
    
    def __init__(self, tipoVia='', nombreVia='', numVia='', otrosDatos='', codPostal='', ciudad='', region='', codPais=''):
        '''
        Constructor
        '''
        'Tipo vía'  
        self.tipoVia = tipoVia
        'Nombre vía'  
        self.nombreVia = nombreVia
        'Número de la vía'
        self.numVia=numVia
        'Piso, puerta, escalera, etc'
        self.otrosDatos = otrosDatos
        'Código postal'
        self.codigoPostal = codPostal
        'Ciudad'
        self.ciudad = ciudad
        'Provincia, comunidad o región'
        self.region = region
        'Código país'
        self.codPais = codPais
        
class DatosPersonalesServicio(object):
    '''
        Datos de la persona asociados al servicio, tales como contacto, horario, observaciones, etc
    '''
    def __init__(self, contacto = None, aLaAtencionDe = None, horario= None, observaciones = None):
        'Contacto'
        self.contacto = contacto
        'A la atención de'
        self.aLaAtencionDe = aLaAtencionDe
        'Horario'
        self.horario= horario
        'Observaciones'
        self.observaciones = observaciones
        
class DatosServicio(object):
    '''
    Clase con los datos del servicio de envío,
    están cargados casi todos los datos que necesitamos por defecto
    Los datos de esta clase son los que hay para el envío nacional 
    '''
    
    def __init__(self, fecha='', numAlbaran='', referencia = "", enFranquicia = '', 
                 codigoServicio='', numBultos = '', peso = "", entregaSabado = '', 
                 entregaPartirDe = '', horario = None, tramoHorario = '', notificaciones=None):
        '''
        Constructor
        '''
        'Fecha. Obligatorio'
        self.fecha=fecha
        'NumeroAlbaran'
        self.numAlbaran=numAlbaran
        'Referencia'
        self.referencia = referencia
        'EnFranquicia'  
        self.enFranquicia = enFranquicia
        'Obligatorio'
        self.codigoServicio=codigoServicio
        'Número Bultos. Obligatorio'
        self.numBultos = numBultos
        'Peso, en kilogramos. Obligatorio'
        self.peso = peso
        'Entrega en Sabado'
        self.entregaSabado = entregaSabado
        'Entrega a partir de'
        self.entregaPartirDe = entregaPartirDe
        'Entrega en tramo horario. '
        self.horario = horario
        'Entrega en tramo horario. '
        self.tramoHorario = tramoHorario
        'Notificaciones'
        self.notificaciones=notificaciones
        
class NotificacionEnvio(object):
    
    def __init__(self, canal='', tipo='', telEmail=''):
        
        'Canal de notificacion 1=SMS(coste adicional) 2=EMAIL(gratuito)'
        self.canal=canal
        
        'Tipo Notificacion'
        '1 = Confirmación de entrega'
        '2 = Seguimiento de envío (informa los diferentes estados de tránsito del envío)'
        '3 = Aviso de entrega en franquicia (informa al destinatario del envío que la mercancía está disponible en la franquicia de destino. Solo tendrá sentido para entrega en franquicia, y será obligatorio)'
        '4 = Preaviso de entrega (informa al destinatario del envío de la fecha de entrega de la mercancía. Solo tendrá sentido cuando NO sea entrega en franquicia)'
        '5 = Confirmación de recogida (informa al destinatario que el envío ha sido recogido en origen. Solo tendrá sentido cuando NO sea entrega en franquicia)'
        self.tipo = tipo
        
        'Teléfono móvil o dirección email, según CanalNotificacion'
        self.telEmail=telEmail
        

        
