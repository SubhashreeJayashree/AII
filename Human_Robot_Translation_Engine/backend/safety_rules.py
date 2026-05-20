def is_task_safe(task):
    danger = ["kill", "destroy", "burn", "knife", "bomb", "hurt", "attack"," steal"," illegal", "hack", "throw"]

    for word in danger:
        if word in task.lower():
            return False, f"The word '{word}' indicates danger."

    return True, "Task is safe."
