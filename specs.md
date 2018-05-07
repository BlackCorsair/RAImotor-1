
# Modelo Vectorial - Especificaciones

## Resumen

Se pide desarrollar un script en Python que implemente un Modelo Vectorial de recuperación para el cálculo de similitud entre documentos y consultas. Se trabajará en el ámbito de la minería de textos y el procesamiento del lenguaje natural (PLN).

## Consultas

**Q1** - What video game won Spike's best driving game award in 2006?

**Q2** - What is the default combination of Kensington cables?

**Q3** - Who won the first ACM Gerard Salton prize?

## Documentos

Se trabajará con [5 documentos HTML](https://github.com/FCLatorre/RAIvectorial/tree/develop/docrepository) en idioma inglés.

## Acrónimos

**TF (term frequency)** - frecuencia de un término i en un documento j

tfi,j = fi,j

**IDF (inverse document frequency)** - frecuencia de un término i en el resto de la colección

idfi = log(N/ni)

ni = número de documentos de la colección en los que aparece el término i

N = número total de documentos de la colección

## Funciones de similitud

**Producto Escalar TF:** Función de similitud del producto escalar con pesos según TF

sim(dj,q) = dj * q =  Σ Wij * Wiq

donde Wij = tfi,j = fi,j

**Producto Escalar TF IDF:** Función de similitud del producto escalar con TFxIDF

sim(dj,q) = dj * q =  Σ Wij * Wiq

donde Wij = tfi,j * idfi = fi,j * log(N/ni)

**Coseno TF:** Función de similitud del coseno con pesos TF

CosSim (dj, q) = (Σ Wij * Wiq) / [sqrt(Σ W^2ij) * sqrt(Σ W^2iq)]

donde Wij = tfi,j = fi,j

**Coseno TF IDF:** Función de similitud del coseno con pesos TFxIDF

CosSim (dj, q) = (Σ Wij * Wiq) / [sqrt(Σ W^2ij) * sqrt(Σ W^2iq)]

donde Wij = tfi,j * idfi = fi,j * log(N/ni)

## Output

El output que se muestre por consola tendrá el siguiente formato (X,XX hace referencia a un número con dos cifras decimales):

**RELEVANCIA: ProductoEscalarTF**

| Nombre del doc | Q1   | Q2   | Q3   |
|----------------|------|------|------|
| 2010-22-100    | X,XX | X,XX | X,XX |
| 2010-42-103    | X,XX | X,XX | X,XX |
| 2010-58-044    | X,XX | X,XX | X,XX |
| 2010-76-088    | X,XX | X,XX | X,XX |
| 2010-99-086    | X,XX | X,XX | X,XX |

**RELEVANCIA: ProductoEscalarTFIDF**

| Nombre del doc | Q1   | Q2   | Q3   |
|----------------|------|------|------|
| 2010-22-100    | X,XX | X,XX | X,XX |
| 2010-42-103    | X,XX | X,XX | X,XX |
| 2010-58-044    | X,XX | X,XX | X,XX |
| 2010-76-088    | X,XX | X,XX | X,XX |
| 2010-99-086    | X,XX | X,XX | X,XX |

**RELEVANCIA: CosenoTF**

| Nombre del doc | Q1   | Q2   | Q3   |
|----------------|------|------|------|
| 2010-22-100    | X,XX | X,XX | X,XX |
| 2010-42-103    | X,XX | X,XX | X,XX |
| 2010-58-044    | X,XX | X,XX | X,XX |
| 2010-76-088    | X,XX | X,XX | X,XX |
| 2010-99-086    | X,XX | X,XX | X,XX |

**RELEVANCIA: CosenoTFIDF**

| Nombre del doc | Q1   | Q2   | Q3   |
|----------------|------|------|------|
| 2010-22-100    | X,XX | X,XX | X,XX |
| 2010-42-103    | X,XX | X,XX | X,XX |
| 2010-58-044    | X,XX | X,XX | X,XX |
| 2010-76-088    | X,XX | X,XX | X,XX |
| 2010-99-086    | X,XX | X,XX | X,XX |

Para cada tupla de documento-consulta en la matriz, se debe mostrar el valor correspondiente.

## Clases

**controller:** se encarga de llamar a las otras clases. Es la clase principal que sirve como controlador

**htmlparser:** se encarga de limpiar los documentos de código HTML y obtener el texto limpio.

**normalizer:** se encarga de normalizar las palabras que se han separado con tokenizer, que al ser realizado mediante la librería nltk, se ha implementado esta funcionalidad en esta misma clase, para mantener las dependencias.

Se deben normalizar las palabras en base a:

* *Mayúsculas y minúsculas* - reducir todo a minúsculas
* *Plurales y singulares* - reducir todo a singulares
* *Stop words* - eliminar las stop words
* *Símbolos* - eliminar todo tipo de símbolos que no sean palabras o números: !, >, ., “, /, -, ?, (, ), ‘, ,, :, # etc.
* *Lematización* - reducir todo a lemas
* *Stemming* - reducir todo a temas

**indexer:** se ha delegado esta función en la clase normalizer, por hacer uso de la distribución de frecuencias del nltk por motivos de mejoras de eficiencia.

**dbmanager:** se encarga de gestionar el guardado de los datos (términos, frecuencia, funciones) en base de datos

**search:** se encarga de computar todos los cálculos de los algoritmos correspondientes (producto escalar TF, producto escalar TF-IDF, coseno TF o coseno TF-IDF) dado un documento y una consulta. Se ha optado por hacer todos los cálculos de golpe por motivos de eficiencia con respecto a la recuperación de base de datos.

**cleanDB:** en caso de necesitar limpiar la base de datos para empezar de cero, ejecutar esta clase en lugar de controller y proceder luego normalmente con el setup de controller.

## Archivos y carpetas

* *queryfile.txt:* archivo txt con las consultas (una por línea)
* */docrepository/:* carpeta con los documentos HTML

## Base de datos

* Se trabajará con una base de datos MongoDB
* Se trabajará con 3 tablas principales:
	* Documento
	* Término
	* Relación
* Documento
	* doc_id
	* nombre
* Término
	* term_id
	* idf
	* ni
* Relación
	* doc_id
	* term_id
	* tf


## Otros

* El nombre del proyecto debe ser: *ModeloVectorial_3*
* Se usará Python 3.6.4
* El script se ejecutará en dos pasos:
	* 1er paso - Indización de contenido en BBDD
	* 2do paso - Cálculo de los valores de similitud
* Se permite y aconseja el uso de librerías para realizar los procesos de parseo, tokenización, normalización etc.
* No se permiten librerías externas para la creación directa del índice ni para el cálculo de la similitud entre los documentos y las consultas
* El tiempo de ejecución del script (1er paso) debe ser inferior a 10 segundos y el tiempo de ejecución del script (2do paso) debe ser inferior a 1 segundo
* El script debe estar preparado para funcionar con más documentos HTML (+2000) de forma automática
* El script debe estar prepardo para funcionar con más consultas (+20) de forma automática
* El código debe estar correctamente comentado

## Recursos

* [Frecuencias y pesos de los términos](http://ccdoc-tecnicasrecuperacioninformacion.blogspot.com.es/2012/11/frecuencias-y-pesos-de-los-terminos-de.html)

* [Modelo vectorial](http://ccdoc-tecnicasrecuperacioninformacion.blogspot.com.es/2012/12/modelo-vectorial.html)

* [TF-IDF](https://es.wikipedia.org/wiki/Tf-idf)
