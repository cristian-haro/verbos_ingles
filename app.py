import streamlit as st
import random
from verbs import VERBS_DB

# Configuración de página con título e icono
st.set_page_config(
    page_title="Irregular Verbs Trainer",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Inicializar variables de estado de sesión
if 'enabled_verbs' not in st.session_state:
    # Por defecto todos están habilitados
    st.session_state.enabled_verbs = {v['infinitive'] for v in VERBS_DB}

if 'exam_id' not in st.session_state:
    st.session_state.exam_id = 0

if 'current_verbs' not in st.session_state:
    st.session_state.current_verbs = []

if 'validated' not in st.session_state:
    st.session_state.validated = False

if 'wizard_step' not in st.session_state:
    st.session_state.wizard_step = 0

if 'view_mode' not in st.session_state:
    st.session_state.view_mode = "🪄 Paso a Paso (Wizard)"

if 'respuestas' not in st.session_state:
    st.session_state.respuestas = {}

# Función para iniciar un nuevo examen/práctica
def iniciar_nuevo_examen():
    # Filtrar solo verbos habilitados
    habilitados = [v for v in VERBS_DB if v['infinitive'] in st.session_state.enabled_verbs]
    n_total = len(habilitados)
    n_select = max(1, n_total // 2)
    
    if n_total > 0:
        # Seleccionar aleatoriamente la mitad
        st.session_state.current_verbs = random.sample(habilitados, n_select)
    else:
        st.session_state.current_verbs = []
        
    st.session_state.exam_id += 1
    st.session_state.validated = False
    st.session_state.wizard_step = 0
    st.session_state.respuestas = {
        v['infinitive']: {"infinitive": "", "past_simple": "", "past_participle": ""}
        for v in st.session_state.current_verbs
    }

# Si no hay verbos seleccionados actualmente, iniciar uno al cargar
if not st.session_state.current_verbs and len(st.session_state.enabled_verbs) > 0:
    iniciar_nuevo_examen()

# Asegurar inicialización de respuestas
if st.session_state.current_verbs and not st.session_state.respuestas:
    st.session_state.respuestas = {
        v['infinitive']: {"infinitive": "", "past_simple": "", "past_participle": ""}
        for v in st.session_state.current_verbs
    }

# Capturar y sincronizar respuestas de los widgets de Streamlit en session_state a st.session_state.respuestas
if st.session_state.current_verbs and st.session_state.respuestas:
    for verb in st.session_state.current_verbs:
        base_key = f"{verb['infinitive']}_{st.session_state.exam_id}"
        fields = {'inf': 'infinitive', 'past': 'past_simple', 'part': 'past_participle'}
        for field, dict_key in fields.items():
            st_key = f"{field}_{base_key}"
            if st_key in st.session_state:
                st.session_state.respuestas[verb['infinitive']][dict_key] = st.session_state[st_key]

# Inyectar estilos CSS premium adaptativos
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;600;700&display=swap');

/* Ocultar elementos de marca de Streamlit (footer, botón de deploy/fork, icono de github, botón manage app y marcas flotantes) */
footer, .stApp [class*="MadeWithStreamlit"] {
    display: none !important;
    visibility: hidden !important;
}
.stAppDeployButton, [data-testid="stAppDeployButton"] {display: none !important;}
.stToolbarActions, [data-testid="stToolbarActions"] {display: none !important;}
[data-testid="manage-app-button"] {display: none !important;}

/* Ocultar el viewer badge flotante de Streamlit Cloud (usando los selectores de clase exactos del usuario) */
._container_gzau3_1, ._viewerBadge_nim44_23, [class*="viewerBadge"], [class*="container_gzau3_1"] {
    display: none !important;
    visibility: hidden !important;
    height: 0 !important;
    width: 0 !important;
    opacity: 0 !important;
}

/* Ocultar opciones de "Print" y "Record a screencast" del menú de 3 puntos */
[data-testid="stMainMenuList"] li:nth-child(4),
[data-testid="stMainMenuList"] li:nth-child(5),
[data-testid="stMainMenuList"] ul:nth-child(4),
[data-testid="stMainMenuList"] ul:nth-child(5) {
    display: none !important;
}

/* Mantener visible el menú de tres puntos (MainMenu) para poder cambiar el tema */
#MainMenu, .stMainMenu, [data-testid="stMainMenu"] {
    visibility: visible !important;
    display: inline-block !important;
}

/* Ajustar el padding superior para equilibrar el diseño con la barra superior visible */
[data-testid="stAppViewContainer"] > section:first-child {
    padding-top: 1.5rem !important;
}

/* Aplicar la fuente global Outfit */
html, body, [data-testid="stAppViewContainer"], .stText {
    font-family: 'Outfit', sans-serif !important;
}

/* Cabecera elegante y moderna */
.header-banner {
    text-align: center;
    padding: 2.5rem 1.5rem;
    background: linear-gradient(135deg, #4f46e5 0%, #7c3aed 100%);
    color: white;
    border-radius: 16px;
    margin-bottom: 2rem;
    box-shadow: 0 10px 25px -5px rgba(79, 70, 229, 0.3);
}

.header-banner h1 {
    font-weight: 700;
    margin: 0;
    color: white !important;
    font-size: 2.5rem;
    letter-spacing: -0.02em;
}

.header-banner p {
    font-weight: 300;
    margin: 0.5rem 0 0 0;
    opacity: 0.9;
    font-size: 1.15rem;
}

/* Tarjeta de verbo */
.verb-card {
    background-color: var(--secondary-background-color, #f8f9fa);
    border-radius: 10px;
    padding: 0.6rem 1rem;
    margin-bottom: 0.75rem;
    border: 1px solid var(--border-color, #e2e8f0);
    /* border-left: 5px solid #4f46e5;*/
    box-shadow: 0 2px 4px -1px rgba(0, 0, 0, 0.04);
    transition: all 0.2s ease-in-out;
}
/*
.verb-card:hover {
    transform: translateY(-1px);
    box-shadow: 0 6px 12px -2px rgba(0, 0, 0, 0.06);
    border-left-color: #7c3aed;
}*/

/* Nombre del verbo en español */
.verb-spanish {
    font-size: 1.15rem;
    font-weight: 700;
    color: var(--text-color, #1a202c);
    margin-bottom: 0;
    display: flex;
    align-items: center;
    gap: 0.5rem;
}

.verb-spanish-badge {
    background-color: rgba(79, 70, 229, 0.1);
    color: #4f46e5;
    font-size: 0.75rem;
    padding: 0.2rem 0.6rem;
    border-radius: 20px;
    font-weight: 600;
    text-transform: uppercase;
}

/* Etiquetas de campo */
.field-label {
    font-size: 0.8rem;
    font-weight: 700;
    color: var(--text-color, #4a5568);
    opacity: 0.8;
    margin-bottom: 0.35rem;
    text-transform: uppercase;
    letter-spacing: 0.06em;
}

/* Caja de feedback de corrección */
.feedback-box {
    border-radius: 8px;
    padding: 0.5rem 0.75rem;
    margin-top: 0.5rem;
    font-size: 0.9rem;
    font-weight: 500;
    display: flex;
    align-items: center;
    gap: 0.3rem;
}

.feedback-correct {
    background-color: rgba(16, 185, 129, 0.12);
    border: 1px solid #10b981;
    color: #10b981;
}

.feedback-incorrect {
    background-color: rgba(239, 68, 68, 0.12);
    border: 1px solid #ef4444;
    color: #ef4444;
}

.correction-word {
    font-weight: 700;
    text-decoration: underline;
}

/* Panel de puntuación */
.score-card {
    background: linear-gradient(135deg, rgba(79, 70, 229, 0.05) 0%, rgba(124, 58, 237, 0.05) 100%);
    border: 2px dashed #4f46e5;
    border-radius: 16px;
    padding: 2rem;
    margin-bottom: 2rem;
    text-align: center;
}

.score-title {
    font-size: 1.4rem;
    font-weight: 700;
    margin-bottom: 0.5rem;
}

.score-big {
    font-size: 3.5rem;
    font-weight: 800;
    color: #4f46e5;
    line-height: 1;
    margin: 1rem 0;
}

.score-details {
    font-size: 1.1rem;
    opacity: 0.85;
}

/* --- ESTILOS MODERNOS PARA WIZARD --- */
.wizard-container {
    background-color: var(--secondary-background-color, #f8f9fa);
    border-radius: 16px;
    padding: 2.5rem 2rem;
    border: 1px solid var(--border-color, #e2e8f0);
    box-shadow: 0 10px 30px -10px rgba(0, 0, 0, 0.08);
    margin-bottom: 1.5rem;
    transition: all 0.3s ease;
}

.wizard-spanish-title {
    font-size: 1.9rem;
    font-weight: 700;
    color: #4f46e5;
    text-align: center;
    margin-bottom: 0.5rem;
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 0.75rem;
}

.progress-wrapper {
    margin-bottom: 2rem;
    background-color: var(--secondary-background-color, #f8f9fa);
    padding: 1rem;
    border-radius: 12px;
    border: 1px solid var(--border-color, #e2e8f0);
}

.progress-text {
    display: flex;
    justify-content: space-between;
    font-size: 0.9rem;
    font-weight: 600;
    color: var(--text-color, #4a5568);
    margin-bottom: 0.5rem;
}

.progress-bar-container {
    background-color: var(--border-color, #e2e8f0);
    border-radius: 10px;
    height: 10px;
    width: 100%;
    overflow: hidden;
}

.progress-bar-fill {
    background: linear-gradient(90deg, #4f46e5 0%, #7c3aed 100%);
    height: 100%;
    border-radius: 10px;
    transition: width 0.4s cubic-bezier(0.4, 0, 0.2, 1);
}
</style>
""", unsafe_allow_html=True)

# Banner de Cabecera Principal
st.markdown("""
<div class="header-banner">
    <h1>🎓 Entrenador de Verbos Irregulares</h1>
    <p>Domina tus verbos en inglés para el examen de la forma más interactiva</p>
</div>
""", unsafe_allow_html=True)

# Crear pestañas superiores para una interfaz muy limpia
tab_practicar, tab_gestion = st.tabs(["✍️ Practicar Examen", "⚙️ Gestionar Verbos"])

# Lógica auxiliar de validación de respuestas
def verificar_respuesta(user_input, correct_answer):
    user_val = user_input.strip().lower()
    # Separar opciones aceptables por barra '/' o coma ','
    opciones = [opt.strip().lower() for opt in correct_answer.replace(',', '/').split('/')]
    return user_val in opciones

# ==================== PESTAÑA: PRACTICAR EXAMEN ====================
with tab_practicar:
    
    # Validar si hay verbos habilitados
    total_habilitados = len(st.session_state.enabled_verbs)
    
    if total_habilitados == 0:
        st.info("⚠️ No tienes ningún verbo habilitado en este momento. Dirígete a la pestaña **Gestionar Verbos** para activar los verbos que deseas practicar.")
    else:
        # Selector de vista interactivo
        col_sel1, col_sel2 = st.columns([2, 1])
        with col_sel1:
            st.session_state.view_mode = st.radio(
                "📱 Modo de visualización:",
                ["🪄 Paso a Paso (Wizard)", "📋 Lista Completa"],
                index=0 if st.session_state.view_mode == "🪄 Paso a Paso (Wizard)" else 1,
                horizontal=True,
                key="view_mode_selector"
            )
        with col_sel2:
            st.markdown('<div style="margin-top: 1.8rem;"></div>', unsafe_allow_html=True)
            st.markdown(f"✨ **Total examen:** {len(st.session_state.current_verbs)} verbos.")

        if st.session_state.view_mode == "📋 Lista Completa":
            # ==================== LIST MODE (LISTA COMPLETA) ====================
            with st.form("exam_form", clear_on_submit=False, enter_to_submit=False):
                
                # Renderizar cada verbo seleccionado en su propia tarjeta elegante
                for index, verb in enumerate(st.session_state.current_verbs):
                    base_key = f"{verb['infinitive']}_{st.session_state.exam_id}"
                    
                    # HTML de la tarjeta del verbo
                    st.markdown(f"""
                    <div class="verb-card">
                        <div class="verb-spanish">
                            <span>{verb['spanish']}</span>
                            <span class="verb-spanish-badge">Verbo {index + 1}</span>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    # Columnas para los 3 inputs
                    col1, col2, col3 = st.columns(3)
                    
                    with col1:
                        st.markdown('<div class="field-label">1. Infinitive</div>', unsafe_allow_html=True)
                        inf_input = st.text_input(
                            "Infinitive", 
                            value=st.session_state.respuestas[verb['infinitive']]['infinitive'],
                            key=f"inf_{base_key}", 
                            label_visibility="collapsed"
                        )
                    
                    with col2:
                        st.markdown('<div class="field-label">2. Past Simple</div>', unsafe_allow_html=True)
                        past_input = st.text_input(
                            "Past Simple", 
                            value=st.session_state.respuestas[verb['infinitive']]['past_simple'],
                            key=f"past_{base_key}", 
                            label_visibility="collapsed"
                        )
                        
                    with col3:
                        st.markdown('<div class="field-label">3. Past Participle</div>', unsafe_allow_html=True)
                        part_input = st.text_input(
                            "Past Participle", 
                            value=st.session_state.respuestas[verb['infinitive']]['past_participle'],
                            key=f"part_{base_key}", 
                            label_visibility="collapsed"
                        )
                    
                    # Mostrar corrección inmediata dentro de la misma tarjeta si ya se ha validado
                    if st.session_state.validated:
                        correct_inf = verificar_respuesta(inf_input, verb['infinitive'])
                        correct_past = verificar_respuesta(past_input, verb['past_simple'])
                        correct_part = verificar_respuesta(part_input, verb['past_participle'])
                        
                        c_col1, c_col2, c_col3 = st.columns(3)
                        
                        with c_col1:
                            if correct_inf:
                                st.markdown('<div class="feedback-box feedback-correct">✅ ¡Correcto!</div>', unsafe_allow_html=True)
                            else:
                                st.markdown(f'<div class="feedback-box feedback-incorrect">❌ Corrección: <span class="correction-word">{verb["infinitive"]}</span></div>', unsafe_allow_html=True)
                                
                        with c_col2:
                            if correct_past:
                                st.markdown('<div class="feedback-box feedback-correct">✅ ¡Correcto!</div>', unsafe_allow_html=True)
                            else:
                                st.markdown(f'<div class="feedback-box feedback-incorrect">❌ Corrección: <span class="correction-word">{verb["past_simple"]}</span></div>', unsafe_allow_html=True)
                                
                        with c_col3:
                            if correct_part:
                                st.markdown('<div class="feedback-box feedback-correct">✅ ¡Correcto!</div>', unsafe_allow_html=True)
                            else:
                                st.markdown(f'<div class="feedback-box feedback-incorrect">❌ Corrección: <span class="correction-word">{verb["past_participle"]}</span></div>', unsafe_allow_html=True)
                    
                    # Espaciado extra entre tarjetas
                    st.markdown('<div style="margin-bottom: 0.75rem;"></div>', unsafe_allow_html=True)
                
                # Botones del formulario
                col_btn1, col_btn2 = st.columns([1, 4])
                with col_btn1:
                    submit_btn = st.form_submit_button("🧪 Validar Respuestas", type="primary", use_container_width=True)
                with col_btn2:
                    nuevo_examen_btn = st.form_submit_button("🔄 Siguiente Examen / Re-sortear", use_container_width=False)
                    
                if nuevo_examen_btn:
                    iniciar_nuevo_examen()
                    st.rerun()
                    
                if submit_btn:
                    st.session_state.validated = True
                    st.rerun()

        else:
            # ==================== WIZARD MODE (PASO A PASO) ====================
            n_verbs = len(st.session_state.current_verbs)
            if n_verbs > 0:
                # Clamp wizard step
                st.session_state.wizard_step = min(max(0, st.session_state.wizard_step), n_verbs - 1)
                current_verb = st.session_state.current_verbs[st.session_state.wizard_step]
                base_key = f"{current_verb['infinitive']}_{st.session_state.exam_id}"
                progress_pct = int(((st.session_state.wizard_step + 1) / n_verbs) * 100)
                
                # Barra de progreso moderna
                st.markdown(f"""
                <div class="progress-wrapper">
                    <div class="progress-text">
                        <span>Progreso de Práctica</span>
                        <span>Verbo {st.session_state.wizard_step + 1} de {n_verbs} ({progress_pct}%)</span>
                    </div>
                    <div class="progress-bar-container">
                        <div class="progress-bar-fill" style="width: {progress_pct}%;"></div>
                    </div>
                </div>
                """, unsafe_allow_html=True)
                
                # Tarjeta del verbo actual
                st.markdown(f"""
                <div class="wizard-container">
                    <div class="wizard-spanish-title">
                        <span>{current_verb['spanish']}</span>
                        <span class="verb-spanish-badge" style="font-size: 0.9rem;">Verbo {st.session_state.wizard_step + 1}</span>
                    </div>
                </div>
                """, unsafe_allow_html=True)
                
                # Inputs en columnas responsivas
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    st.markdown('<div class="field-label">1. Infinitive</div>', unsafe_allow_html=True)
                    inf_input = st.text_input(
                        "Infinitive", 
                        value=st.session_state.respuestas[current_verb['infinitive']]['infinitive'],
                        key=f"inf_{base_key}", 
                        label_visibility="collapsed"
                    )
                
                with col2:
                    st.markdown('<div class="field-label">2. Past Simple</div>', unsafe_allow_html=True)
                    past_input = st.text_input(
                        "Past Simple", 
                        value=st.session_state.respuestas[current_verb['infinitive']]['past_simple'],
                        key=f"past_{base_key}", 
                        label_visibility="collapsed"
                    )
                    
                with col3:
                    st.markdown('<div class="field-label">3. Past Participle</div>', unsafe_allow_html=True)
                    part_input = st.text_input(
                        "Past Participle", 
                        value=st.session_state.respuestas[current_verb['infinitive']]['past_participle'],
                        key=f"part_{base_key}", 
                        label_visibility="collapsed"
                    )
                
                # Mostrar corrección inmediata si ya se ha validado
                if st.session_state.validated:
                    correct_inf = verificar_respuesta(inf_input, current_verb['infinitive'])
                    correct_past = verificar_respuesta(past_input, current_verb['past_simple'])
                    correct_part = verificar_respuesta(part_input, current_verb['past_participle'])
                    
                    c_col1, c_col2, c_col3 = st.columns(3)
                    
                    with c_col1:
                        if correct_inf:
                            st.markdown('<div class="feedback-box feedback-correct">✅ ¡Correcto!</div>', unsafe_allow_html=True)
                        else:
                            st.markdown(f'<div class="feedback-box feedback-incorrect">❌ Corrección: <span class="correction-word">{current_verb["infinitive"]}</span></div>', unsafe_allow_html=True)
                            
                    with c_col2:
                        if correct_past:
                            st.markdown('<div class="feedback-box feedback-correct">✅ ¡Correcto!</div>', unsafe_allow_html=True)
                        else:
                            st.markdown(f'<div class="feedback-box feedback-incorrect">❌ Corrección: <span class="correction-word">{current_verb["past_simple"]}</span></div>', unsafe_allow_html=True)
                            
                    with c_col3:
                        if correct_part:
                            st.markdown('<div class="feedback-box feedback-correct">✅ ¡Correcto!</div>', unsafe_allow_html=True)
                        else:
                            st.markdown(f'<div class="feedback-box feedback-incorrect">❌ Corrección: <span class="correction-word">{current_verb["past_participle"]}</span></div>', unsafe_allow_html=True)
                
                # Fila de navegación
                st.markdown('<div style="margin-top: 1.5rem;"></div>', unsafe_allow_html=True)
                nav_col1, nav_col2, nav_col3 = st.columns([1, 2, 1])
                
                with nav_col1:
                    prev_disabled = st.session_state.wizard_step == 0
                    if st.button("👈 Anterior", disabled=prev_disabled, use_container_width=True, key="wizard_prev_btn"):
                        st.session_state.wizard_step -= 1
                        st.rerun()
                
                with nav_col2:
                    # Selector dropdown de salto rápido
                    opciones_jumper = [f"Verbo {i+1}: {v['spanish']}" for i, v in enumerate(st.session_state.current_verbs)]
                    jumper_val = st.selectbox(
                        "Ir directo al verbo:",
                        options=opciones_jumper,
                        index=st.session_state.wizard_step,
                        label_visibility="collapsed",
                        key="wizard_jumper_select"
                    )
                    # Trigger de salto si cambia la selección
                    selected_index = opciones_jumper.index(jumper_val)
                    if selected_index != st.session_state.wizard_step:
                        st.session_state.wizard_step = selected_index
                        st.rerun()
                
                with nav_col3:
                    if st.session_state.wizard_step < n_verbs - 1:
                        if st.button("Siguiente 👉", use_container_width=True, key="wizard_next_btn"):
                            st.session_state.wizard_step += 1
                            st.rerun()
                    else:
                        if st.button("🧪 Validar", type="primary", use_container_width=True, key="wizard_validate_step_btn"):
                            st.session_state.validated = True
                            st.rerun()
                
                # Botones generales abajo
                st.divider()
                act_col1, act_col2 = st.columns([1, 1])
                with act_col1:
                    if st.button("🧪 Validar Todo el Examen", type="primary", use_container_width=True, key="wizard_validate_full_btn"):
                        st.session_state.validated = True
                        st.rerun()
                with act_col2:
                    if st.button("🔄 Nuevo Examen / Re-sortear", use_container_width=True, key="wizard_reset_full_btn"):
                        iniciar_nuevo_examen()
                        st.rerun()

        # Mostrar panel de puntuación si se ha validado
        if st.session_state.validated:
            total_campos = len(st.session_state.current_verbs) * 3
            campos_correctos = 0
            verbos_perfectos = 0
            
            for verb in st.session_state.current_verbs:
                ans = st.session_state.respuestas[verb['infinitive']]
                c_inf = verificar_respuesta(ans['infinitive'], verb['infinitive'])
                c_past = verificar_respuesta(ans['past_simple'], verb['past_simple'])
                c_part = verificar_respuesta(ans['past_participle'], verb['past_participle'])
                
                if c_inf: campos_correctos += 1
                if c_past: campos_correctos += 1
                if c_part: campos_correctos += 1
                
                if c_inf and c_past and c_part:
                    verbos_perfectos += 1
            
            porcentaje = int((campos_correctos / total_campos) * 100) if total_campos > 0 else 0
            
            st.markdown(f"""
            <div class="score-card">
                <div class="score-title">📊 RESULTADOS DE TU EXAMEN</div>
                <div class="score-big">{porcentaje}%</div>
                <div class="score-details">
                    Has acertado <strong>{campos_correctos}</strong> de <strong>{total_campos}</strong> conjugaciones.<br>
                    ¡Lograste completar perfectamente <strong>{verbos_perfectos}</strong> de <strong>{len(st.session_state.current_verbs)}</strong> verbos!
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            # Efectos de celebración según la puntuación
            if porcentaje == 100:
                st.balloons()
                st.success("🎉 ¡Puntuación perfecta! Has dominado este bloque al 100%. ¡Excelente trabajo!")
            elif porcentaje >= 80:
                st.balloons()
                st.success("👏 ¡Excelente! Estás muy cerca de la perfección. ¡Sigue así!")
            elif porcentaje >= 50:
                st.warning("👍 ¡Buen intento! Tienes buena base, pero aún quedan algunos verbos por pulir. ¡Vuelve a intentarlo!")
            else:
                st.error("📚 Necesitas repasar un poco más. Prueba a habilitar menos verbos en la pestaña de gestión para enfocarte en grupos más pequeños.")
        
        # Inyectar script de JavaScript para navegación con Enter ultra-rápida (UX Premium)
        st.markdown(
            """<img src="x" onerror="(function() {
                const inputs = Array.from(document.querySelectorAll('input[type=text]')).filter(input => !input.closest('[data-testid=stSidebar]'));
                inputs.forEach((input, index) => {
                    if (input.dataset.enterListenerBound) return;
                    input.dataset.enterListenerBound = 'true';
                    input.addEventListener('keydown', function(e) {
                        if (e.key === 'Enter') {
                            e.preventDefault();
                            if (index < inputs.length - 1) {
                                inputs[index + 1].focus();
                            } else {
                                const buttons = Array.from(document.querySelectorAll('button'));
                                const targetBtn = buttons.find(btn => btn.textContent.includes('Siguiente') || btn.textContent.includes('Validar'));
                                if (targetBtn) {
                                    targetBtn.click();
                                }
                            }
                        }
                    });
                });
            })()" style="display:none;"/>""",
            unsafe_allow_html=True
        )

# ==================== PESTAÑA: GESTIONAR VERBOS ====================
with tab_gestion:
    st.header("⚙️ Gestor del Listado de Verbos")
    st.markdown("""
    Desde aquí puedes personalizar completamente qué verbos quieres que entren en el sorteo de tus exámenes. 
    Esto es perfecto para ir aprendiéndolos **por bloques poco a poco** en lugar de todos de golpe.
    """)
    
    # Métricas rápidas de habilitación
    col_m1, col_m2, col_m3 = st.columns(3)
    with col_m1:
        st.metric("Total Verbos Disponibles", len(VERBS_DB))
    with col_m2:
        st.metric("Verbos Habilitados actualmente", len(st.session_state.enabled_verbs))
    with col_m3:
        n_select_sim = max(1, len(st.session_state.enabled_verbs) // 2)
        st.metric("Verbos a sortear por examen (Mitad)", n_select_sim if len(st.session_state.enabled_verbs) > 0 else 0)
        
    # Acciones masivas
    st.subheader("Acciones Rápidas")
    col_act1, col_act2, col_act3, col_act4 = st.columns(4)
    
    with col_act1:
        if st.button("✅ Habilitar Todos los Verbos", use_container_width=True):
            st.session_state.enabled_verbs = {v['infinitive'] for v in VERBS_DB}
            iniciar_nuevo_examen()
            st.rerun()
            
    with col_act2:
        if st.button("❌ Deshabilitar Todos los Verbos", use_container_width=True):
            # Dejar al menos 2 habilitados para evitar fallos matemáticos de sorteo vacíos
            st.session_state.enabled_verbs = {VERBS_DB[0]['infinitive'], VERBS_DB[1]['infinitive']}
            iniciar_nuevo_examen()
            st.rerun()
            
    with col_act3:
        if st.button("🎯 Habilitar Top 20 Comunes", use_container_width=True):
            # be, become, begin, break, bring, buy, choose, come, do, drink, drive, eat, find, get, give, go, have, know, lose, make
            top_20 = {"be", "become", "begin", "break", "bring", "buy", "choose", "come", "do", "drink", 
                      "drive", "eat", "find", "get", "give", "go", "have", "know", "lose", "make"}
            st.session_state.enabled_verbs = top_20
            iniciar_nuevo_examen()
            st.rerun()

    with col_act4:
        if st.button("💪 Habilitar Cortos e Idénticos", use_container_width=True):
            # Verbos cuyas 3 formas son idénticas o cortas: bet, cost, cut, hit, hurt, let, put, read, set, shut
            identicos = {"bet", "cost", "cut", "hit", "hurt", "let", "put", "read", "set", "shut"}
            st.session_state.enabled_verbs = identicos
            iniciar_nuevo_examen()
            st.rerun()

    st.divider()
    
    # Buscador y filtros
    st.subheader("Filtro y Listado Individual")
    search_query = st.text_input("🔍 Buscar verbo por infinitivo o traducción en español...", placeholder="ej. speak, comprar, eat...")
    
    # Filtrar verbos según la búsqueda
    filtered_verbs = []
    for verb in VERBS_DB:
        q = search_query.strip().lower()
        if not q or q in verb['infinitive'].lower() or q in verb['spanish'].lower():
            filtered_verbs.append(verb)
            
    st.markdown(f"Mostrando **{len(filtered_verbs)}** de **{len(VERBS_DB)}** verbos.")
    
    # Grid de 3 columnas con checkboxes para activar/desactivar individualmente
    if filtered_verbs:
        cols_grid = st.columns(3)
        for i, verb in enumerate(filtered_verbs):
            col_target = cols_grid[i % 3]
            
            with col_target:
                # Comprobar si está actualmente habilitado
                is_enabled = verb['infinitive'] in st.session_state.enabled_verbs
                
                # Checkbox interactivo
                label = f"**{verb['infinitive']}** — *{verb['spanish']}*"
                check_val = st.checkbox(label, value=is_enabled, key=f"checkbox_manage_{verb['infinitive']}")
                
                # Actualizar el set según el estado del checkbox
                if check_val != is_enabled:
                    if check_val:
                        st.session_state.enabled_verbs.add(verb['infinitive'])
                    else:
                        # Evitar deshabilitar si nos vamos a quedar con 0 habilitados
                        if len(st.session_state.enabled_verbs) > 1:
                            st.session_state.enabled_verbs.discard(verb['infinitive'])
                        else:
                            st.warning("⚠️ Debes tener al menos 1 verbo habilitado en tu lista para el sorteo.")
                    # Generar nuevo sorteo para aplicar la nueva lista
                    iniciar_nuevo_examen()
                    st.rerun()
    else:
        st.info("No se encontraron verbos que coincidan con tu búsqueda.")
