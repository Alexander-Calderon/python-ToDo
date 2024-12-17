# import config.settings
from config import settings
from sqlalchemy import create_engine, Column, Integer, String, Boolean, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime

Base = declarative_base()

class Task(Base):
    __tablename__ = 'tasks'

    id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False)
    description = Column(String)
    completed = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.now)
    completed_at = Column(DateTime, nullable=True)

    def __repr__(self):
        return f"<Task(id={self.id}, title='{self.title}', completed={self.completed})>"


class DatabaseManager:
    def __init__(self, db_path='todo.db'):
        self.engine = create_engine(f'sqlite:///{settings.DB_PATH}')
        Base.metadata.create_all(self.engine)
        self.Session = sessionmaker(bind=self.engine)

    def add_task(self, title, description):
        session = self.Session()
        try:
            new_task = Task(title=title, description=description)
            session.add(new_task)
            session.commit()
            return new_task
        except Exception as e:
            session.rollback()
            raise e
        finally:
            session.close()

    def get_all_tasks(self):
        session = self.Session()
        try:
            tasks = session.query(Task).all()
            return tasks
        finally:
            session.close()

    def mark_task_completed(self, task_id):
        session = self.Session()
        try:
            task = session.query(Task).get(task_id)
            if task:
                task.completed = True
                task.completed_at = datetime.now()
                session.commit()
            return task
        except Exception as e:
            session.rollback()
            raise e
        finally:
            session.close()

    def delete_completed_tasks(self):
        session = self.Session()
        try:
            session.query(Task).filter(Task.completed == True).delete()
            session.commit()
        except Exception as e:
            session.rollback()
            raise e
        finally:
            session.close()

    def export_tasks_to_json(self, filename='dumped/tasks.json'):
        import json
        session = self.Session()
        try:
            tasks = session.query(Task).all()
            tasks_data = [{
                'id': task.id,
                'title': task.title,
                'description': task.description,
                'completed': task.completed,
                'created_at': task.created_at.isoformat(),
                'completed_at': task.completed_at.isoformat() if task.completed_at else None
            } for task in tasks]

            # with open(filename, 'w') as f:
            #     json.dump(tasks_data, f, indent=4)
            json_data = json.dumps(tasks_data, indent=4)
            return json_data

        finally:
            session.close()

    def import_tasks_from_json(self, filename='tasks.json', tasks_data=None):
        import json
        session = self.Session()
        try:
            if tasks_data is None:
                with open(filename, 'r') as f:
                    tasks_data = json.load(f)

            for task_data in tasks_data:
                existing_task = session.query(Task).filter_by(title=task_data['title']).first()
                if existing_task:
                    continue

                task = Task(
                    title=task_data['title'],
                    description=task_data['description'],
                    completed=task_data['completed']
                )
                session.add(task)

            session.commit()
        except Exception as e:
            session.rollback()
            raise e
        finally:
            session.close()

