import time

import streamlit as st

from components.Tasks.task_component import render_task_buttons, render_task
from models.task_model import DatabaseManager
import traceback


class TaskManagerApp:
    def __init__(self):
        self.db_manager = DatabaseManager()
        self.init_session_state()

    def init_session_state(self):
        if 'view_mode' not in st.session_state:
            st.session_state.view_mode = 'all'

        if "uploaded_file" not in st.session_state:
            st.session_state["uploaded_file"] = None

        if "file_uploader_key" not in st.session_state:
            st.session_state["file_uploader_key"] = 0

    def render_add_task_section(self):
        st.header("Agregar Nueva Tarea")
        with st.form(key='add_task_form'):
            title = st.text_input("Título de la Tarea")
            description = st.text_area("Descripción")
            submit_button = st.form_submit_button(label='Agregar Tarea')

            if submit_button:
                try:
                    if not title:
                        st.error("El título de la tarea es obligatorio")
                    else:
                        self.db_manager.add_task(title, description)
                        success_message = st.success(f"Tarea '{title}' agregada exitosamente")
                        time.sleep(1)
                        success_message.empty()
                except Exception as e:
                    st.error(f"Error al agregar tarea: {e}")



    def render_tasks_section(self):
        st.header("Mis Tareas")

        render_task_buttons()

        tasks = self.db_manager.get_all_tasks()
        filtered_tasks = []

        if st.session_state.view_mode == 'pending':
            filtered_tasks = [task for task in tasks if not task.completed]
        elif st.session_state.view_mode == 'completed':
            filtered_tasks = [task for task in tasks if task.completed]
        else:
            filtered_tasks = tasks

        for task in filtered_tasks:
            render_task(task, self.db_manager)



    def render_actions_section(self):
        st.subheader("Eliminar Tareas Completadas")
        col = st.columns(1)[0]  # Columna única

        with col:
            if st.button("Eliminar Tareas Completadas"):
                try:
                    self.db_manager.delete_completed_tasks()
                    st.success("Tareas completadas eliminadas")
                    time.sleep(1)
                    st.rerun()
                except Exception as e:
                    st.error(f"Error al eliminar tareas: {e}")

        st.divider()
        st.header("Exportar/Importar Tareas")
        col1, col2 = st.columns(2)

        with col1:
            export_filename = st.text_input("Nombre de archivo para exportar", value="tasks.json")
            if st.button("Exportar Tareas"):
                try:
                    json_data = self.db_manager.export_tasks_to_json()

                    st.download_button(
                        label="📥 Descarga",
                        data=json_data,
                        file_name=export_filename,
                        mime="application/text"
                    )


                except Exception as e:
                    st.error(f"Error al exportar tareas: {e}")

        with col2:
            uploaded_file = st.file_uploader("Importar Tareas desde JSON", type=['json'], key=st.session_state["file_uploader_key"])

            if uploaded_file is not None:
                st.session_state["uploaded_file"] = uploaded_file

            if st.session_state["uploaded_file"] is not None:
                try:
                    import json
                    file_content = st.session_state["uploaded_file"].getvalue().decode("utf-8")
                    tasks_data = json.loads(file_content)

                    self.db_manager.import_tasks_from_json(tasks_data=tasks_data)
                    st.success("Tareas importadas exitosamente")

                    # fix para que no se quede el archivo cargado y pueda refrescar con rerun. (alternativa sería intentar usar estados para el file_uploader...)
                    st.session_state["uploaded_file"] = None
                    st.session_state["file_uploader_key"] += 1  # Cambiar la clave para "resetear" el uploader
                    time.sleep(1)
                    st.rerun()

                except Exception as e:
                    st.error(f"Error al importar tareas: {e}")

    def run(self):
        st.title("📋 TODO App")

        self.render_add_task_section()
        self.render_tasks_section()
        self.render_actions_section()


