# Mejora Motor Recuperación - RAI

## Resumen

**Universidad:** Universidad Carlos III de Madrid

**Asignatura:** Recuperación y Acceso a la Información (RAI)

**Práctica:** Motor de Recuperación y Evaluación

**Descripción:** Desarrollar un motor de recuperación Web capaz de indizar y recuperar documentos Web

**Lenguaje + Versión:** Python 3.6.4

![Logo UC3M](https://madi.uc3m.es/wp-content/uploads/2015/01/Logo-uc3m.jpg)

## Inicialización de archivos
Se deben copiar los ficheros html al directorio /docrepository. Para hacer tal cosa, desde la carpeta Datos donde se encuentran los ficheros html, ejecutar el siguiente comando en terminal:

`find [directorio donde estan los html] -name '*.html' -exec cp '{}' [directorio de docsrepository] \;`

## Consultas

[fichero XML de consultas](https://github.com/FCLatorre/RAImotor/blob/develop/2010-topics.xml)

## Documentos

[docs](https://github.com/FCLatorre/RAImotor/tree/develop/docrepository)

## Funciones de similitud

**Coseno TF IDF:** Función de similitud del coseno con pesos TFxIDF

## Recursos
path management in directory - [pathlib](https://docs.python.org/3/library/pathlib.html)

pulling data out of HTML - [beautifulsoup](https://www.crummy.com/software/BeautifulSoup/bs4/doc/)

processing HTML - [lxml](https://github.com/lxml/lxml)

regular expressions (RegEX) - [re](https://docs.python.org/3.6/library/re.html)

processing human language data library - [nltk](http://www.nltk.org/)

print output to console - [tabulate](https://pypi.python.org/pypi/tabulate)

git extensions to provide high-level repository operations - [git-flow cheatsheet](https://danielkummer.github.io/git-flow-cheatsheet/)

XML parsing - [XML ElementTree](https://docs.python.org/3/library/xml.etree.elementtree.html)
