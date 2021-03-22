# -*- coding: utf-8 -*-
"""
Created on Sat Jan 23 17:31:40 2021

@author: RROJASQ
"""
import pandas as pd
import numpy as np

#%%
repeat = 5
archivo_movimientos = pd.read_csv("files/Movimiento - copia.csv", header=0)

archivo_ventas = pd.read_excel("files/Libro_ventas.xlsx", header=0)
archivo_ventas["Fecha elaboración"] = pd.to_datetime(archivo_ventas["Fecha elaboración"])
archivo_ventas_proceso = pd.DataFrame(np.repeat(archivo_ventas.values,repeat,axis=0),
                                      columns=archivo_ventas.columns)

#%%
archivo_ventas_proceso["CMDAnoMovimiento"] = archivo_ventas_proceso["Fecha elaboración"].dt.year.astype('Int64')
archivo_ventas_proceso["CMDPeriodoMovimiento"] = archivo_ventas_proceso["Fecha elaboración"].dt.month.astype('Int64')
archivo_ventas_proceso["CMDComprobanteMovimiento"] = 2
archivo_ventas_proceso["CMDPrefijoMovimiento"] = archivo_ventas_proceso["Comprobante"].str[:4]
archivo_ventas_proceso["CMDDocumentoMovimiento"] = archivo_ventas_proceso["Comprobante"].str[5:]
archivo_ventas_proceso["CMDFechaMovimiento"] = archivo_ventas_proceso["Fecha elaboración"].dt.strftime("%m/%d/%Y")
archivo_ventas_proceso["CMDItemMovimiento"] = archivo_ventas_proceso.index+1
archivo_ventas_proceso["CMDCodCentroCostosMovimiento"] = 0
archivo_ventas_proceso["CMDCodigoMonedaMovimiento"] = 0
archivo_ventas_proceso["CMDCodigoActivoMovimiento"] = None
archivo_ventas_proceso["CMDCodigoDiferidoMovimiento"] = None
archivo_ventas_proceso["CMDIdentificadorUnoMovimiento"] = archivo_ventas_proceso["Identificación"]
archivo_ventas_proceso["CMDSucursalMovimiento"] = 0
archivo_ventas_proceso["CMDIdentificadorDosMovimiento"] = archivo_ventas_proceso["Identificación"]
archivo_ventas_proceso["CMDPrefijoRefmovimiento"] = 0
archivo_ventas_proceso["CMDDocumentoRefMovimiento"] = archivo_ventas_proceso["Comprobante"]
archivo_ventas_proceso["CMDComentariosMovimiento"] = "Venta accesorios varios"
archivo_ventas_proceso["CMDValorMovimiento"] = archivo_ventas_proceso["Base gravada"]
archivo_ventas_proceso["CMDValorBaseMovimiento"] = archivo_ventas_proceso["Base gravada"]
archivo_ventas_proceso["CMDValorMonedaMovimiento"] = 0
archivo_ventas_proceso["CMDOrigenMovimiento"] = "DIG"
archivo_ventas_proceso["CMDConsecutivoCruceExtractoMovimiento"] = 0
archivo_ventas_proceso["CMDAnoCruceExtractoMovimiento"] = None
archivo_ventas_proceso["CMDPeriodoCruceExtractoMovimiento"] = None
archivo_ventas_proceso["CMDTipoAsientoMovimiento"] = "F"
archivo_ventas_proceso["CMDValorOtraMonedaMovimiento"] = 0

archivo_ventas_proceso["tipo"] = archivo_ventas_proceso["CMDItemMovimiento"] % 6
 #Total, base gravable (5, 19), iva (5, 19), base exenta
archivo_ventas_proceso.loc[(archivo_ventas_proceso["tipo"]==0), "tipo"] = "TOTAL"
archivo_ventas_proceso.loc[(archivo_ventas_proceso["tipo"]==1), "tipo"] = "BASE_GRAVADA_5"
archivo_ventas_proceso.loc[(archivo_ventas_proceso["tipo"]==2), "tipo"] = "BASE_GRAVADA_19"
archivo_ventas_proceso.loc[(archivo_ventas_proceso["tipo"]==3), "tipo"] = "IVA_5"
archivo_ventas_proceso.loc[(archivo_ventas_proceso["tipo"]==4), "tipo"] = "IVA_19"
archivo_ventas_proceso.loc[(archivo_ventas_proceso["tipo"]==5), "tipo"] = "BASE_EXENTA"

archivo_ventas_proceso["procesado"] = None

# SUCURSAL
archivo_ventas_proceso.loc[(archivo_ventas_proceso["CMDPrefijoMovimiento"]=="FV-2"),
                           "sucursal"] = "PRINCIPAL"
archivo_ventas_proceso.loc[(archivo_ventas_proceso["CMDPrefijoMovimiento"]=="FV-3"),
                           "sucursal"] = "OVIEDO"

# NATURALEZA DE LA CUENTA
archivo_ventas_proceso.loc[(archivo_ventas_proceso["tipo"]!="TOTAL"),
                           "CMDNaturalezaMovimiento"] = "CNO"
archivo_ventas_proceso.loc[(archivo_ventas_proceso["tipo"]=="TOTAL"),
                           "CMDNaturalezaMovimiento"] = "DNO"

#%% CUENTAS

archivo_ventas_proceso.loc[
    (archivo_ventas_proceso["tipo"] == "TOTAL") &
    (archivo_ventas_proceso["sucursal"] == "PRINCIPAL"), 
                       "CMDCodigoCuentaMovimiento"] = "130505"
archivo_ventas_proceso.loc[
    (archivo_ventas_proceso["tipo"] == "TOTAL") &
    (archivo_ventas_proceso["sucursal"] == "OVIEDO"), 
                       "CMDCodigoCuentaMovimiento"] = "11100503"

archivo_ventas_proceso.loc[
    (archivo_ventas_proceso["tipo"] == "BASE_GRAVADA_19") &
    (archivo_ventas_proceso["sucursal"] == "PRINCIPAL"), 
                       "CMDCodigoCuentaMovimiento"] = "41359501"
archivo_ventas_proceso.loc[
    (archivo_ventas_proceso["tipo"] == "BASE_GRAVADA_19") &
    (archivo_ventas_proceso["sucursal"] == "OVIEDO"), 
                       "CMDCodigoCuentaMovimiento"] = "41359510"

archivo_ventas_proceso.loc[
    (archivo_ventas_proceso["tipo"] == "BASE_GRAVADA_5") &
    (archivo_ventas_proceso["sucursal"] == "PRINCIPAL"), 
                       "CMDCodigoCuentaMovimiento"] = "41359503"
archivo_ventas_proceso.loc[
    (archivo_ventas_proceso["tipo"] == "BASE_GRAVADA_5") &
    (archivo_ventas_proceso["sucursal"] == "OVIEDO"), 
                       "CMDCodigoCuentaMovimiento"] = "41359511"

archivo_ventas_proceso.loc[
    (archivo_ventas_proceso["tipo"] == "IVA_19") &
    (archivo_ventas_proceso["sucursal"] == "PRINCIPAL"), 
                       "CMDCodigoCuentaMovimiento"] = "24080101"
archivo_ventas_proceso.loc[
    (archivo_ventas_proceso["tipo"] == "IVA_19") &
    (archivo_ventas_proceso["sucursal"] == "OVIEDO"), 
                       "CMDCodigoCuentaMovimiento"] = "24080101"

archivo_ventas_proceso.loc[
    (archivo_ventas_proceso["tipo"] == "IVA_5") &
    (archivo_ventas_proceso["sucursal"] == "PRINCIPAL"), 
                       "CMDCodigoCuentaMovimiento"] = "24080103"
archivo_ventas_proceso.loc[
    (archivo_ventas_proceso["tipo"] == "IVA_5") &
    (archivo_ventas_proceso["sucursal"] == "OVIEDO"), 
                       "CMDCodigoCuentaMovimiento"] = "24080103"

archivo_ventas_proceso.loc[
    (archivo_ventas_proceso["tipo"] == "BASE_EXENTA") &
    (archivo_ventas_proceso["sucursal"] == "PRINCIPAL"), 
                       "CMDCodigoCuentaMovimiento"] = "41359502"
archivo_ventas_proceso.loc[
    (archivo_ventas_proceso["tipo"] == "BASE_EXENTA") &
    (archivo_ventas_proceso["sucursal"] == "OVIEDO"), 
                       "CMDCodigoCuentaMovimiento"] = "41359512"

columnas_movimiento = ["CMDAnoMovimiento","CMDPeriodoMovimiento","CMDComprobanteMovimiento","CMDPrefijoMovimiento","CMDDocumentoMovimiento","CMDFechaMovimiento","CMDItemMovimiento","CMDCodigoCuentaMovimiento","CMDCodCentroCostosMovimiento","CMDCodigoMonedaMovimiento","CMDCodigoActivoMovimiento","CMDCodigoDiferidoMovimiento","CMDIdentificadorUnoMovimiento","CMDSucursalMovimiento","CMDIdentificadorDosMovimiento","CMDPrefijoRefmovimiento","CMDDocumentoRefMovimiento","CMDComentariosMovimiento","CMDValorMovimiento","CMDValorBaseMovimiento","CMDValorMonedaMovimiento","CMDNaturalezaMovimiento","CMDOrigenMovimiento","CMDConsecutivoCruceExtractoMovimiento","CMDAnoCruceExtractoMovimiento","CMDPeriodoCruceExtractoMovimiento","CMDTipoAsientoMovimiento","CMDValorOtraMonedaMovimiento"]
columnas_archivo_movimiento = archivo_movimientos.columns
archivo_ventas_final = archivo_ventas_proceso[columnas_movimiento]
archivo_ventas_final.to_csv("files/archivo_ventas_final.csv", index=False)

# Base gravable, iva: CNO --> OK
# TOTAL: DNO --> OK
#FV-2: PRINCIPAL --> OK
#FV-3: OVIEDO --> OK
#Cuentas: 19%: 
        # Base gravable:Principal: 41359501 --> OK, 
        #   Oviedo: 41359510  --> OK
        # iva: 24080101 --> OK
        #5%
        #Oviedo: 41359511 --> OK
        #24080103 --> OK

# Base no gravada (exenta): . No tiene IVA
    #Principal:41359502 --> OK
       #OViedo 41359512 --> OK


# Total de la principal: 130505 --> OK
