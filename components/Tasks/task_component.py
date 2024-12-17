import streamlit as st

def render_task_buttons():
    """Renderiza los botones (del encabezao) para filtrar tareas."""
    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("Todas las Tareas"):
            st.session_state.view_mode = 'all'
    with col2:
        if st.button("Pendientes"):
            st.session_state.view_mode = 'pending'
    with col3:
        if st.button("Completadas"):
            st.session_state.view_mode = 'completed'

def render_task(task, db_manager):
    """Renderiza un único elemento de tarea."""
    with st.expander(f"🔹 {task.title}"):
        st.write(f"**Descripción:** {task.description or 'Sin descripción'}")
        st.write(f"**Estado:** {'✅ Completada' if task.completed else '⏳ Pendiente'}")

        col1, _ = st.columns(2)
        with col1:
            if not task.completed:
                if st.button(f"Marcar Completada (ID: {task.id})"):
                    try:
                        db_manager.mark_task_completed(task.id)
                        st.rerun()
                    except Exception as e:
                        st.error(f"Error al marcar tarea: {e}")
