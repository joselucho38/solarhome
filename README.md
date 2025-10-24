# solarhome
# Proyecto Web – Energía Solar

Sitio web responsivo desarrollado con **HTML + CSS + JavaScript (Bootstrap 5)**.  
Incluye calculadora de consumo/paneles, formulario de cotización, galería, tabla de datos y sección de documentación/reproducibilidad (Python).

---

## 1. Estructura del repositorio

energia-solar-site/
├─ index.html # Inicio: hero, marcas, quiénes somos, valores, certificaciones
├─ informacion.html # Cobertura nacional, garantías, formulario de cotización
├─ calculadora.html # Calculadora (resultados en Card de Bootstrap)
├─ galeria.html # Brochure de imágenes
├─ contacto.html # Tabla con datos de contacto
├─ docs.html # Documentación y reproducibilidad (Python)
├─ datos.html # Tabla que consume JSON exportado por Python
├─ styles.css # Estilos (paleta, navbar lime translúcida, botones amarillos)
├─ script.js # Lógica: menú activo, calculadora, cotización
└─ data/
└─ consumo_por_mes.json # Dataset de ejemplo (kWh/mes) consumido por datos.html

> Todo el código está **comentado en español** para facilitar la lectura y la sustentación.

---

## 2. Cómo ejecutar localmente

- Opción 1 (rápida): Abrir `index.html` con doble clic en un navegador moderno.
- Opción 2 (servida):  
  ```bash
  # macOS/Linux
  python3 -m http.server 8080
  # Windows
  py -m http.server 8080

Luego ingresar a http://localhost:8080.

No se requieren dependencias, ya que Bootstrap se carga desde CDN.

3. Navegación

Inicio (index.html): héroe con CTA, cinta de marcas (logos), quiénes somos, valores, certificaciones.

Información (informacion.html): cobertura nacional, garantías, formulario de cotización (válido en front).

Calculadora (calculadora.html): cálculo de costo mensual, consumo/costo diario y paneles requeridos (400 Wp ≈ 48 kWh/mes); resultados mostrados en Card.

Galería (galeria.html): resultados de proyectos como brochure.

Datos (datos.html): visualiza datos históricos en tabla consumiendo data/consumo_por_mes.json.

Docs (docs.html): buenas prácticas y reproducibilidad con Python (Colab/VS Code).

Contáctanos (contacto.html): tabla de contactos, dirección en Medellín y redes en el footer.


4. Calculadora – Supuestos y fórmulas

Entrada: consumo mensual (kWh) y costo por kWh.

Salida:

Costo mensual = consumo_mensual * costo_kwh

Consumo diario ≈ consumo_mensual / 30

Costo diario = consumo_diario * costo_kwh

Paneles requeridos = ceil(consumo_mensual / 48)
(suponiendo panel de 400 Wp con ~4 HSP/día ⇒ 1.6 kWh/día ⇒ ~48 kWh/mes).

Los resultados son aproximados y pueden variar por ubicación, orientación y sombras.


5. Paleta y lineamientos visuales

Navbar: verde limón translúcida (rgba(163,217,0,0.85)).

CTA/Botones: amarillo solar #FFCC00 (hover #E6B800).

Accesibilidad: tipografías del sistema, contraste elevado en CTA, menú activo iluminado.

6. Reproducibilidad con Python
6.1. Librerías sugeridas

Pandas, NumPy, Matplotlib, Seaborn (y Streamlit opcional).

6.2. Flujo de trabajo (notebook/Colab)

Cargar dataset (CSV/JSON) con series de consumo.

Procesar/Limpiar (fechas, agregaciones por mes).

Visualizar (gráficos de barras/líneas).

Exportar un resumen para la web:
import pandas as pd
df = pd.read_csv('data/consumo_solar.csv')
df['mes'] = pd.to_datetime(df['fecha']).dt.to_period('M')
df_salida = df.groupby('mes')['kwh'].sum().reset_index()
df_salida.to_json('web/data/consumo_por_mes.json', orient='records')

Abrir datos.html para ver la tabla con el JSON exportado.
Python 3.11 · pandas 2.2 · numpy 1.26 · matplotlib 3.8 · seaborn 0.13

7. Pruebas rápidas (QA)

Navbar: verificar que el enlace de la página actual quede activo.

Calculadora: probar valores válidos/ inválidos (texto, 0, negativos).

Card: asegurar que se muestre y haga scroll suave al calcular.

Cotización: probar validación de nombre/email/ciudad y confirmación en Card.

Datos: editar data/consumo_por_mes.json y confirmar que la tabla se actualiza.

Responsive: revisar en móvil (≤576px), tablet (≥768px) y escritorio (≥992px).

8. Créditos y licencia

Imágenes: demostrativas (Unsplash / Wikimedia).

Este proyecto se entrega con fines académicos. Derechos reservados © 2025.



---

# `RUBRICA.md`

```markdown
# Rúbrica de evaluación – Proyecto Web Energía Solar

## 1) Código limpio y comentado (Web)
- **HTML**: etiquetas semánticas, estructura clara, comentarios en secciones clave.  
  - Archivos: `index.html`, `informacion.html`, `calculadora.html`, `galeria.html`, `datos.html`, `docs.html`, `contacto.html`.
- **CSS**: variables CSS (paleta), bloques comentados (navbar, botones, card, galería).  
  - Archivo: `styles.css`.
- **JS**: funciones pequeñas, nombres descriptivos, comentarios línea a línea en cálculo y DOM.  
  - Archivo: `script.js`.

**Evidencia:** comentarios en español en todos los archivos.

---

## 2) Organización lógica (flujo)
- **Entradas → Procesamiento → Salidas**:
  - Formulario (inputs) → **`Calcular_Consumo()`** → escritura en DOM (`innerText`) + **Card Bootstrap**.
- **Navegación clara** con **navbar** y páginas separadas por tema.

**Evidencia:** `calculadora.html` + `script.js`.

---

## 3) Reproducibilidad (Python)
- Sección **Docs** explica librerías, flujo y exportación de **JSON** para la web.  
- Sugerencia de versiones y estructura de carpetas.

**Evidencia:** `docs.html` (bloque de código y pasos) y `datos.html` (consumo de JSON).

---

## 4) Uso de librerías estándar (Python)
- **Pandas/NumPy/Matplotlib/Seaborn** (y **Streamlit** opcional) propuestos en `docs.html`.
- Ejemplo de **exportación** de resultados para integración con la **web**.

---

## 5) Página web (JS/Bootstrap)
- **Bootstrap** para responsividad, navbar translúcida **verde limón**, botones **amarillos** (paleta Erco-like).  
- **Calculadora** con resultados en **Card** (sin `alert`).  
- **Tabla de datos** en `datos.html`.  
- **Formulario** de cotización con validación.  
- **Galería** tipo brochure.  
- **Footer** con redes sociales y dirección Medellín.

---

## 6) Contenido pertinente al proyecto (solar)
- Cobertura nacional, garantías (10 años instalación), certificaciones, valores, clientes.

---

## 7) Interacción JS construida en clase
- Eventos de click, lectura de inputs, validaciones, actualización del DOM, **scroll suave** a resultados.

---

## 8) Criterios visuales y de UX
- Paleta consistente (navbar lime translúcida, CTA amarillos, contraste).  
- Animación sutil en tarjetas y carrusel de marcas.  
- Legibilidad y orden.

---

## Checklist del jurado/docente
- [ ] La calculadora funciona y muestra la **Card** de resultado.  
- [ ] `datos.html` lee **`data/consumo_por_mes.json`** y pinta **tabla**.  
- [ ] `docs.html` describe claramente la **reproducibilidad** y el **flujo** en Python.  
- [ ] Código **comentado** y **organizado** (HTML/CSS/JS).  
- [ ] Navegación completa entre secciones.  
- [ ] Diseño **responsive** y consistente con la paleta definida.  
- [ ] Formulario de **cotización** con validación básica.  
- [ ] Footer con redes y dirección.  

