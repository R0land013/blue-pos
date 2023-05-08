
# Blue POS

**Blue POS** es una aplicación de escritorio para la **gestión de gastos, productos y ventas**
para los **puntos de ventas en Cuba**. Permite realizar **reportes** de ventas y gastos a varias
escalas temporales, así como mostrar **estadísticas** de forma gráfica. Blue POS se creó
con el fin de ayudar a crecer y optimizar a los pequeños negocios de Cuba. Este software
será **gratis por siempre**.

# Funcionalidades de Blue POS

## Gestión de productos

Blue POS permite gestionar los productos existentes en el inventario. Deja crear productos
con su **precio de costo** y **su precio de venta por unidad**. Además, los productos se pueden crear
con un **nombre** y una **descripción**, para ayudar a diferenciarlos de otros productos y a
describirlos con mayor exactitud. Los productos también se insertan con el atributo de **cantidad disponible**,
el cuál refleja el número de productos de un tipo que queda en el inventario. **Este número variará de manera
automática cuando se realicen o se deshagan ventas** del producto en cuestión. Cuando un producto es creado,
el sistema le asigna un **id** único, para diferenciarlo de manera inequívoca, incluso si otros productos poseen
nombres y descripciones similares.

También se pueden **eliminar los productos**, lo que hará que desaparezcan las ventas registradas de ese producto
en el sistema.

Una vez creado un producto, a este se le puede **editar** todos sus atributos excepto el de **id**. Por ejemplo se podría
editar el campo de precio o costo, ya que estos pueden haber variado en el mundo real.

## Gestión de ventas

Esta app permite seleccionar un producto y ver todas las ventas que se han realizado del mismo.
En la vista de gestión de ventas se permite **registrar las ventas de un producto**, seleccionando
la **fecha de la venta** y la **cantidad de unidades del producto que se venderá**. Cuando se registren cierta cantidad
de ventas de un producto, la cantidad de disponible del producto en el inventario decrecerá en la misma cantidad
de unidades vendidas.

Luego de registrar una venta, el sistema le asignará un **id** para diferenciarlas de las demás. Las ventas son regsitradas
en el sistema usando los datos del producto, de allí es de donde las ventas adquieren los valores para sus atributos de
**dinero pagado** y **costo del producto**.

Una venta puede ser **editada**, en el caso de que se haya cometido algún error o en cualquier otra situación que
se desee manejar.

Las ventas se pueden **deshacer**, lo que hará que sea eliminadas del sistema, y que se **repongan** esa cantidad de ventas
en la **cantidad disponible del producto** que se había vendido.

## Gestión de gastos

El sistema permite gestionar los **gastos indirectos** que se van realizando en el negocio. Los gastos indirectos son aquellos
que no influyen en el precio final de un producto. Los gastos se pueden crear con los atributos de **nombre**,
**descripción**, **dinero gastado**, y **fecha**. A cada gasto que se inserta, e sistema le asigna un **id** único.

Los gastos pueden ser **eliminados** y **editados**.

Los **gastos son incluidos en todos los reportes** que se realicen con la aplicación.

## Reportes

La aplicación permite crear reportes de ventas:

- **Diario**
- **Semanal**
- **Mensual**
- **Anual**
- **Personalizado**

En cada uno de los distintos reportes se muestran el número de la **cantidad de ventas** realizadas,
el **dinero obtenido**, el **costo total** de todas las unidades de todos los productos que se vendieron,
las **ganacias** obtenidas entre todas las ventas realizadas, el **gasto** realizado y las **ganancias netas**.

El **reporte personalizado** es una herramienta flexible que permite crear reportes seleccionando una **fecha inicial
y otra final**. Además deja **seleccionar los productos que se incluirán en el reporte**. También permite asignarle
un **nombre** y **descripción**, para describir la información que se está mostrando en el reporte, lo cuál es muy
útil a la hora de **exportar** el reporte personalizado.

Cada uno de estos reportes se pueden **exportar** como archivo **.pdf** o **.html**.

## Estadísticas

El sistema cuenta con una sección de **estadísticas** para ver en un **gráfico** las **ganancias netas**, la **cantidad de
ventas**, y los **gastos totales**, de manera **mensual** o **anual**. Si el usuario pone el cursor sobre uno de los
puntos del gráfico se mostrará un resumen de las operaciones realizadas. Los gráficos permiten ver de manera más clara
el **crecimiento** o **decrecimiento** del negocio. Además permite observar el impacto del las decisiones tomadas en el
negocio a lo largo del tiempo.

# Contribuir

Si deseas contribuir al proyecto puedes dar sugerencias y avisar de errores escribiendo a
**<a href="mailto:blueposapp@gmail.com">blueposapp@gmail.com</a>**,
o realizando **donaciones** al número de teléfono **+53 55023808**. También puedes correr la voz sobre este proyecto en
tus redes sociales, para que más personas se beneficien.

## Si eres desarrollador

Si eres desarrolador puedes crear issues con problemas que hayas encontrado, o puedes abrir PR para arreglar errores
o para añadir otras funciones al programa.

### Ejecutar la app

Esta app es multiplataforma. Ha sido probada en Windows y Linux. Para ejecutar la app sólo es necesario tener instalada
la versión de **Python** **3.7.4** o superior. Antes de ejecutar por primera vez Blue POS es recomendable actualizar la versión de **pip**:

```
#Para Windows
python -m pip install --upgrade pip

#Para Linux
python3 -m pip install --upgrade pip
```

Luego se debe instalar las dependencias del proyecto:

```
#Para Windows
python -m pip install -r requirements.txt

#Para Linux
python3 -m pip install -r requirements.txt
```

Después se puede ejecutar la app sin ningún problema.

```
#Para Windows
python main.py

#Para Linux
python3 main.py
```

### Ejecutar tests

Para ejecutar los tests:

```
python runtests.py nombre_de_los_tests
```

Puedes reemplazar **nombre_de_los_tests** por parte del nombre de los módulos de tests que quieres ejecutar. Por ejemplo si ejecutas

```
python runtests.py product
```

se ejecutarán todas las pruebas que tienen **product** en el nombre de sus módulos. Si se omitiera
el argumento **nombre_de_los_tests** entonces se ejecutarían todos los tests dentro del
paquete **tests**

Para que el script **runtests.py** encuentre tus tests, estos deben estar dentro del
paquete **tests**, y el módulo debe tener el nombre con el siguiente formato **test\*.py**.
