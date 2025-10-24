/* =========================================================
   JS COMÚN DEL SITIO - Proyecto Energía Solar
   ---------------------------------------------------------
   1) Menú activo           2) Calculadora (CARD Bootstrap)
   3) Envío de cotización   4) Utilidades sencillas
   ========================================================= */

/* -------- 1) MENÚ ACTIVO -------- */
(function marcarActivo() {
  try {
    const path = location.pathname.split('/').pop() || 'index.html';
    document.querySelectorAll('.navbar .nav-link').forEach(a => {
      const href = a.getAttribute('href');
      if (href && href.endsWith(path)) a.classList.add('active');
    });
  } catch (_) { /* silencioso */ }
})();

/* -------- 2) CALCULADORA: resultados en CARD --------
   Requiere en HTML:
   - Inputs:  #consumo_mensual, #costo_kwh
   - Textos:  #resultado, #consumo_diario, #costo_diario
   - Card:    #cardResultado, #cardTitulo, #cardResumen,
              #cardConsumoLinea, #cardCostoLinea,
              #cardPanelesLinea, #cardSugerencia
------------------------------------------------------ */
function Calcular_Consumo() {
  // Entradas
  const consumo = parseFloat(document.getElementById('consumo_mensual')?.value);
  const costo   = parseFloat(document.getElementById('costo_kwh')?.value);

  // Validaciones
  if (!Number.isFinite(consumo) || !Number.isFinite(costo)) {
    mostrarCardError('⚠️ Por favor ingresa números válidos en consumo y costo por kWh.');
    return;
  }
  if (consumo <= 0 || costo <= 0) {
    mostrarCardError('⚠️ Los valores deben ser mayores que 0.');
    return;
  }

  // Cálculos básicos
  const total          = consumo * costo;
  const consumo_diario = consumo / 30;
  const costo_diario   = consumo_diario * costo;

  // Estimación paneles: 400Wp ~ 48 kWh/mes
  const KWH_POR_PANEL_MES = 48;
  const paneles = Math.ceil(consumo / KWH_POR_PANEL_MES);

  // Sugerencia por rango
  let sugerencia = '';
  if (consumo <= 200)      sugerencia = 'Instalación pequeña (~4 paneles).';
  else if (consumo <= 400) sugerencia = 'Instalación media (6 a 9 paneles).';
  else                     sugerencia = 'Instalación avanzada (10+ paneles).';

  // Salidas rápidas bajo el formulario
  setTextSafe('resultado',      `💰 Costo mensual: $${total.toFixed(2)}`);
  setTextSafe('consumo_diario', `📊 Consumo diario: ${consumo_diario.toFixed(2)} kWh`);
  setTextSafe('costo_diario',   `💵 Costo diario: $${costo_diario.toFixed(2)}`);

  // Render en la Card
  renderCardResultado({ consumo_mensual: consumo, total, panelesRequeridos: paneles, sugerencia });
}

/* ---- Pinta la Card de resultado ---- */
function renderCardResultado({ consumo_mensual, total, panelesRequeridos, sugerencia }) {
  const card          = document.getElementById('cardResultado');
  const titulo        = document.getElementById('cardTitulo');
  const resumen       = document.getElementById('cardResumen');
  const liConsumo     = document.getElementById('cardConsumoLinea');
  const liCosto       = document.getElementById('cardCostoLinea');
  const liPaneles     = document.getElementById('cardPanelesLinea');
  const sugerenciaBox = document.getElementById('cardSugerencia');

  if (!card || !titulo || !resumen || !liConsumo || !liCosto || !liPaneles || !sugerenciaBox) return;

  titulo.textContent    = 'Estimación de paneles solares';
  resumen.textContent   = `Resumen: Consumo mensual ${consumo_mensual.toFixed(2)} kWh · Costo mensual $${total.toFixed(2)}`;
  liConsumo.textContent = `• Consumo mensual: ${consumo_mensual.toFixed(2)} kWh`;
  liCosto.textContent   = `• Costo mensual: $${total.toFixed(2)}`;
  liPaneles.textContent = `• Paneles requeridos (100% cobertura): ${panelesRequeridos}`;
  sugerenciaBox.textContent = `💡 ${sugerencia}  *Nota: cálculo aproximado; puede variar por ubicación, orientación y sombras.*`;

  card.classList.remove('d-none');
  card.scrollIntoView({ behavior: 'smooth', block: 'center' });
}

/* ---- Muestra errores dentro de la Card ---- */
function mostrarCardError(msg) {
  const card = document.getElementById('cardResultado');
  setTextSafe('cardTitulo', 'Validación de datos');
  setTextSafe('cardResumen', msg);
  setTextSafe('cardConsumoLinea', '');
  setTextSafe('cardCostoLinea', '');
  setTextSafe('cardPanelesLinea', '');
  setTextSafe('cardSugerencia', 'Revisa los campos e intenta de nuevo.');
  if (card) { card.classList.remove('d-none'); card.scrollIntoView({ behavior: 'smooth', block: 'center' }); }
}

/* ---- Utilidad segura para escribir texto si el elemento existe ---- */
function setTextSafe(id, text) { const el = document.getElementById(id); if (el) el.textContent = text; }

/* -------- 3) ENVÍO SIMULADO DE COTIZACIÓN -------- */
function enviarCotizacion(e){
  e?.preventDefault?.();
  const nombre = document.getElementById('cot-nombre')?.value?.trim();
  const email  = document.getElementById('cot-email')?.value?.trim();
  const ciudad = document.getElementById('cot-ciudad')?.value?.trim();
  if(!nombre || !email || !ciudad){
    mostrarCardError('⚠️ Por favor completa: Nombre, Email y Ciudad.');
    return false;
  }
  renderCardResultado({
    consumo_mensual: 0, total: 0, panelesRequeridos: 0,
    sugerencia: 'Solicitud enviada correctamente.'
  });
  setTextSafe('cardTitulo', 'Solicitud de cotización recibida');
  setTextSafe('cardResumen', `✅ Gracias, ${nombre}. Te contactaremos a ${email}.`);
  setTextSafe('cardConsumoLinea',''); setTextSafe('cardCostoLinea',''); setTextSafe('cardPanelesLinea','');
  setTextSafe('cardSugerencia', 'Nuestro equipo te contactará en horario laboral.');
  return false;
}
