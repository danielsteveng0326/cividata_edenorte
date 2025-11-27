# Plantilla PAA

## Instrucciones para crear la plantilla

Debe crear un archivo Word llamado `plantilla_paa.docx` en esta carpeta con el formato oficial del Certificado PAA.

### Campos a incluir (placeholders):

Los siguientes campos deben estar en el documento Word exactamente como se muestran:

- `{{w_gen}}` - Género (EL o LA)
- `{{w_cargo}}` - Cargo del usuario
- `{{w_anno}}` - Año actual
- `{{w_codigos}}` - Códigos UNSPSC
- `{{w_objeto}}` - Objeto del contrato
- `{{w_valor}}` - Valor del contrato
- `{{w_plazo}}` - Plazo del contrato
- `{{w_fecha}}` - Fecha en letras

### Ejemplo de texto en la plantilla:

```
CERTIFICADO DEL PLAN ANUAL DE ADQUISICIONES

{{w_gen}} suscrito {{w_cargo}} de la Empresa de Distribución Eléctrica del Norte S.A. (EDENORTE), 
certifica que en el Plan Anual de Adquisiciones del año {{w_anno}}, se encuentra incluido el siguiente proceso:

CÓDIGOS UNSPSC: {{w_codigos}}

OBJETO: {{w_objeto}}

VALOR ESTIMADO: {{w_valor}}

PLAZO: {{w_plazo}}

Se expide la presente certificación a los {{w_fecha}}.
```

### Importante:

- Mantenga el formato original (tipografías, espaciados, alineaciones)
- Incluya encabezados y pies de página si es necesario
- Incluya firmas y sellos según el formato oficial
- NO modifique nada más que los placeholders indicados
