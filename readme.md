# Usage

Procesar distrito descargar los json de las mesas. 

- Primer parametro es la provincia. 
- Segundo es la categoria, 10 es la de intendente. 
- "Nacional" es para recorrer solo mesas nacionales, se puede hacer lo mismo de extranjeros.
- Hay un parametro opcional que es recorrer solo un distrito especificando el id.
```
procesar_distrito("02", "10", "nacional")
```

Despues se puede transformar los json a un df de pandas. 
- Si no se le aclara municipio procesa todos los json encontrados en las carpetas de cada distrito.
```
json_to_df(municipio_target="063")
```
