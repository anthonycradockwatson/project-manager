from gui.shared.base_view_model import BaseViewModel


class ProjectViewModel(BaseViewModel):
    def get_project(self, project_id):
        return self.get_item(project_id)

    def get_task_rows(self, project):
        return [
            {
                "task": task,
                "subtasks": task.subtasks,
            }
            for task in project.tasks
        ]
