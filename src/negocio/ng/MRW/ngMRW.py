#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
Created on 10 abr. 2017

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

For use these library we need install zeep. We can install with pip typing the next instruction:
pip install zeep

'''

from src.negocio.util.utFiles import utConfig
from src.dato.EnPedido import DatosServicio, DatosCliente, NotificacionEnvio
from datetime import date
from zeep import xsd


class ngMRWSagec(object):
    '''
    classdocs
    '''

    def __init__(self, rutaFicheroCfg='config/mrwSagec.cfg'):
        '''
        Constructor que también carga las credenciales con las que llamaremos al SAGEC
        :rutaFicheroCfg ruta del fichero de donde se recogerán las credenciales      
        '''
        self.rutaCfg=rutaFicheroCfg
        utcon = utConfig(rutaFicheroCfg)
        
        datosSAGEC=utcon.configMapOptions(section='SAGEC')
        
        self.url = datosSAGEC['URL_MRW_SOAP_PROD'.lower()]
        self.codFranquicia = datosSAGEC['FRANQUICIA_SAGEC'.lower()]
        self.codAbonado = datosSAGEC['ABONADO_SAGEC'.lower()]
        self.codDepartamento = datosSAGEC['DEPARTAMENTO_SAGEC'.lower()]
        self.userName = datosSAGEC['USER_SAGEC'.lower()]
        self.passw = datosSAGEC['PASS_SAGEC'.lower()]
        
        self.datosRecogida = None
    
    def direccionRecogidaPorDefectoConfig(self, datosRecogida=DatosCliente()):
        '''
        Método que carga los datos de recogida por defecto que hay en el fichero de configuración
        :datosRecogida Entidad con los datos de recogida, si está inicializada se machacan los datos
        '''
        utcon = utConfig(self.rutaCfg)
        
        confRecogida=utcon.configMapOptions(section='DIRECCION_RECOGIDA')
        
        datosRecogida.direccion.codigoPostal = confRecogida['COD_POSTAL'.lower()]
        datosRecogida.direccion.ciudad = confRecogida['LOCALIDAD'.lower()]
        datosRecogida.direccion.tipoVia = confRecogida['TIPO_VIA'.lower()]
        datosRecogida.direccion.nombreVia = confRecogida['CALLE'.lower()]
        datosRecogida.direccion.numVia = confRecogida['NUM'.lower()]
        datosRecogida.datosPersServicio.contacto = confRecogida['CONTACTO'.lower()]
        datosRecogida.datosPersonales.nombre = confRecogida['NOMBRE'.lower()]
        datosRecogida.datosPersonales.telefono = confRecogida['TELEFONO'.lower()]
        datosRecogida.datosPersonales.NIF = confRecogida['NIF'.lower()]
        
        return datosRecogida
    
    def datosServicioPorDefectoConfig(self, datoServicio=DatosServicio()):
        '''
        Método que carga los datos del servicio por defecto que hay en el fichero de configuración
        :datosServicio Entidad con los datos de servicio, si está inicializada se machacan los datos
        '''
        utcon = utConfig(self.rutaCfg)
        
        confServicio=utcon.configMapOptions(section='DATOS_SERVICIO')
        
        # Si la fecha está vacía asignamos la fecha actual
        if datoServicio.fecha==None or datoServicio.fecha=='':
            datoServicio.fecha=date.today()  # Asigna fecha actual
            
        datoServicio.enFranquicia = confServicio['ENFRANQUICIA'.lower()]
        datoServicio.codigoServicio = confServicio['COD_SERVICIO'.lower()]
        datoServicio.numBultos = confServicio['NUM_BULTOS'.lower()]
        datoServicio.peso = confServicio['PESO'.lower()]
        datoServicio.entregaSabado = confServicio['ENTREGA_SABADO'.lower()]
        datoServicio.tramoHorario = confServicio['TRAMO_HORARIO'.lower()]
        
        if not(datoServicio.notificaciones):
            datoServicio.notificaciones = [NotificacionEnvio(), None]
        
        return datoServicio
        
       
    def llamadaSAGEC(self, pedido):
        '''
        :pedido objeto con los datos necesarios para la llamada al SAGEC
        Método encargado de la llamada al SAGEC
        '''
        from zeep import Client
        
        client = Client(self.url)
               
        authInfo = self.loadCabecerasEnvio(client)
        
        request = self.loadEnvio(client, pedido)
        
        response = client.service.TransmEnvio(request=request, _soapheaders={'AuthInfo': authInfo})
        
        return response
        
        

    def loadCabecerasEnvio(self, client):
        '''
        Método que carga el tipo AuthInfo
        ns0:AuthInfo(CodigoFranquicia: xsd:string, CodigoAbonado: xsd:string, CodigoDepartamento: xsd:string, UserName: xsd:string, Password: xsd:string, _attr_1: {})
        :client cliente para recuperar la factoría que formará las credenciales en la llamada soap
        '''
        
        factory = client.type_factory("ns0")
    
        return factory.AuthInfo(CodigoFranquicia=self.codFranquicia,
                         CodigoAbonado=self.codAbonado,
                         CodigoDepartamento=self.codDepartamento,
                         UserName=self.userName,
                         Password=self.passw)
        
    def loadEnvio(self, client, pedido):
        '''
        ns0:TransmEnvioRequest(DatosRecogida: ns0:DatosRemitenteRequest, DatosEntrega: ns0:DatosDestinatarioRequest, DatosServicio: ns0:DatosServicioRequest)
        :client
        :pedido pedido con los datos que vamos a necesitar para formar el envío
        '''
        factory = client.type_factory("ns0")
    
        return factory.TransmEnvioRequest(DatosRecogida=self.loadDatosRecogida(factory, pedido.datosRecogida),
                                          DatosEntrega=self.loadDatosEnvio(factory, pedido.datosEnvio),
                                          DatosServicio=self.loadDatosServicioEnvio(factory, pedido))
    
    def loadDireccion(self, factory, direccion):
        '''
        Dirección de envío
        ns0:DireccionRequest(CodigoDireccion: xsd:string, 
                             CodigoTipoVia: xsd:string, 
                             Via: xsd:string, 
                             Numero: xsd:string, 
                             Resto: xsd:string, 
                             CodigoPostal: xsd:string, 
                             Poblacion: xsd:string, 
                             Provincia: xsd:string, 
                             Estado: xsd:string, CodigoPais: xsd:string, 
                             TipoPuntoEntrega: xsd:string, 
                             CodigoPuntoEntrega: xsd:string, 
                             CodigoFranquiciaAsociadaPuntoEntrega: xsd:string, 
                             TipoPuntoRecogida: xsd:string, 
                             CodigoPuntoRecogida: xsd:string, 
                             CodigoFranquiciaAsociadaPuntoRecogida: xsd:string, 
                             Agencia: xsd:string)
        :factory factoría para formar la dirección
        :direccion objeto con los datos de la dirección
        '''
        
        
        # Son los datos del destinatario
        return factory.DireccionRequest(CodigoDireccion=xsd.SkipValue,  # Opcional - Se puede omitir. Si se indica sustituira al resto de parametros
                                        CodigoTipoVia=direccion.tipoVia,  # Opcional - Se puede omitir aunque es recomendable usarlo
                                        Via=direccion.nombreVia,  # Obligatorio
                                        Numero=direccion.numVia,  # Obligatorio - Recomendable que sea el dato real. Si no se puede extraer el dato real se pondra 0 (cero)
                                        Resto=direccion.otrosDatos,  # Opcional - Se puede omitir.
                                        CodigoPostal=direccion.codigoPostal ,  # Obligatorio
                                        Poblacion=direccion.ciudad,  # Obligatorio
                                        Estado=xsd.SkipValue,  # Opcional - Se debe omitir para envios nacionales.
                                        CodigoPais=direccion.codPais  # Opcional - Se puede omitir para envios nacionales.
                                        )        
    
    def loadDatosRecogida(self, factory, datosRecogida):
        '''
        Datos del destinatario del envío
        ns0:DatosRemitenteRequest(Direccion: ns0:DireccionRequest, 
                                  Nif: xsd:string, 
                                  Nombre: xsd:string, 
                                  Telefono: xsd:string, 
                                  Contacto: xsd:string,
                                  Horario: ns0:HorarioRequest, 
                                  Observaciones: xsd:string)
        :factory
        :datosRecogida
        '''
     
        
        return factory.DatosRemitenteRequest(Direccion=self.loadDireccion(factory, datosRecogida.direccion),
                Nif=datosRecogida.datosPersonales.NIF,  # Opcional - Se puede omitir.
                Nombre=datosRecogida.datosPersonales.nombre,  # Obligatorio
                Telefono=datosRecogida.datosPersonales.telefono,  # Opcional - Muy recomendable
                Contacto=datosRecogida.datosPersServicio.contacto,  # Opcional - Muy recomendable
                Horario=datosRecogida.datosPersServicio.horario,  # Opcional - Se puede omitir este campo y los sub-arrays
                Observaciones=datosRecogida.datosPersServicio.observaciones  # Opcional - Se puede omitir.
                )
    
    def loadDatosEnvio(self, factory, datosEntrega):
        '''
        Datos del destinatario del envío
        ns0:DatosDestinatarioRequest(Direccion: ns0:DireccionRequest, 
                                     Nif: xsd:string, 
                                     Nombre: xsd:string, 
                                     Telefono: xsd:string, 
                                     Contacto: xsd:string, 
                                     ALaAtencionDe: xsd:string, 
                                     Horario: ns0:HorarioRequest, 
                                     Observaciones: xsd:string)
        :factory
        :datosEntrega
        '''
        
        return factory.DatosDestinatarioRequest(Direccion=self.loadDireccion(factory, datosEntrega.direccion),
                                                Nif=datosEntrega.datosPersonales.NIF,  # Opcional - Se puede omitir.
                                                Nombre=datosEntrega.datosPersonales.nombre,  # Obligatorio
                                                Telefono=datosEntrega.datosPersonales.telefono,  # Opcional - Muy recomendable
                                                Contacto=datosEntrega.datosPersServicio.contacto,  # Opcional - Muy recomendable
                                                ALaAtencionDe=datosEntrega.datosPersServicio.aLaAtencionDe,  # Opcional - Se puede omitir.
                                                Horario=datosEntrega.datosPersServicio.horario,  # Opcional - Se puede omitir este campo y los sub-arrays
                                                Observaciones=datosEntrega.datosPersServicio.observaciones  # Opcional - Se puede omitir.
                                                )
        
    
    def loadDatosServicioEnvio(self, factory, pedido):
        '''
        Datos del servicio de envío
        ns0:DatosServicioRequest(Fecha: xsd:string, 
                                 NumeroAlbaran: xsd:string, 
                                 Referencia: xsd:string, 
                                 EnFranquicia: xsd:string, 
                                 CodigoServicio: xsd:string, 
                                 DescripcionServicio: xsd:string, 
                                 Frecuencia: xsd:string, 
                                 CodigoPromocion: xsd:string, 
                                 NumeroSobre: xsd:string, 
                                 Bultos: ns0:ArrayOfBultoRequest, 
                                 NumeroBultos: xsd:string, 
                                 Peso: xsd:string, 
                                 NumeroPuentes: xsd:string, 
                                 EntregaSabado: xsd:string, 
                                 Entrega830: xsd:string, 
                                 EntregaPartirDe: xsd:string, 
                                 Gestion: xsd:string, 
                                 Retorno: xsd:string, 
                                 CodigoServicioRetorno: xsd:string, 
                                 ConfirmacionInmediata: xsd:string, 
                                 Reembolso: xsd:string, 
                                 ImporteReembolso: xsd:string, 
                                 TipoMercancia: xsd:string, 
                                 ValorDeclarado: xsd:string, 
                                 ServicioEspecial: xsd:string, 
                                 CodigoMoneda: xsd:string, 
                                 ValorEstadistico: xsd:string, 
                                 ValorEstadisticoEuros: xsd:string, 
                                 Notificaciones: ns0:ArrayOfNotificacionRequest, 
                                 SeguroOpcional: ns0:SeguroOpcionalRequest, 
                                 TramoHorario: xsd:string, 
                                 PortesDebidos: xsd:string, 
                                 Mascara_Tipos: xsd:string, 
                                 Mascara_Campos: xsd:string, 
                                 Asistente: xsd:string)
        :factory
        :pedido
        '''
        return factory.DatosServicioRequest(Fecha=pedido.datosServicio.fecha,  # Obligatorio. Fecha >= Hoy()
                                            Referencia=pedido.datosServicio.referencia,  # Obligatorio. ¿numero de pedido/albaran/factura?
                                            EnFranquicia=pedido.datosServicio.enFranquicia,  # Opcional (N = Entrega en domicilio - E = Entrega en franquicia)
                                            CodigoServicio=pedido.datosServicio.codigoServicio,  # Obligatorio - 0800 = Ecommerce
                                            NumeroBultos=pedido.datosServicio.numBultos,  # Obligatorio. Solo puede haber un bulto por envio en eCommerce
                                            Peso=pedido.datosServicio.peso,  # Obligatorio. Debe ser igual al valor Peso en BultoRequest si se ha usado
                                            EntregaSabado=pedido.datosServicio.horario,  # Opcional - Se puede omitir. (coste adicional)
                                            EntregaPartirDe=pedido.datosServicio.entregaPartirDe,  # Opcional (coste adicional)
                                            Notificaciones=self.loadNotificacionesEnvio(factory, pedido),  # Opcional - Se puede omitir todo el nodo y subnodos
                                            TramoHorario=pedido.datosServicio.tramoHorario  # Opcional - Horario de entrega (coste adicional)
                                            )        
    
    def loadNotificacionesEnvio(self, factory, pedido):
        '''
        Método para cargar las notificaciones de los datos del servicio desde el fichero de configuración
        ns0:ArrayOfNotificacionRequest(NotificacionRequest: ns0:NotificacionRequest[])
        :factory
        :pedido
        '''
        if pedido.datosServicio.notificaciones == None:
            '''
            elements = factory.ArrayOfNotificacionRequest(            
            elements[0](CanalNotificacion=pedido.datosServicio.notificaciones[0].canal,
                        TipoNotificacion=pedido.datosServicio.notificaciones[0].tipoEnvio,
                        MailSMS=pedido.datosServicio.notificaciones[0].telEmail),
            elements[1](CanalNotificacion=pedido.datosServicio.notificaciones[1].canal,
                        TipoNotificacion=pedido.datosServicio.notificaciones[1].tipoEnvio,
                        MailSMS=pedido.datosServicio.notificaciones[1].telEmail))
            '''
            rutaCfg = self.rutaConfigPorDefecto()
            utcon = utConfig(rutaCfg)
        
            confRecogida=utcon.configMapOptions(section='NOTIFICACION_REMITENTE')            
            
            notRemitente=factory.NotificacionRequest(CanalNotificacion=confRecogida['CANAL'.lower()],
                                                     TipoNotificacion=confRecogida['TIPO'.lower()],
                                                     MailSMS=confRecogida['EMAIL_NOTIF_POR_DEFECTO'.lower()])
            
            confRecogida=utcon.configMapOptions(section='NOTIFICACION_DESTINATARIO')
            
            notDestinatario=factory.NotificacionRequest(CanalNotificacion=confRecogida['CANAL'.lower()],
                                                        TipoNotificacion=confRecogida['TIPO'.lower()],
                                                        MailSMS=pedido.datosEnvio.datosPersonales.email)
            
            return factory.ArrayOfNotificacionRequest([notRemitente, notDestinatario])
        
        
        
        
