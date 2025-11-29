from datetime import datetime

def has_circular_dependency(task, tasks, visited=None):
    if not visited:
        visited = set()
    
    task_id = task.get('id')
    if not task_id:
        return False
    
    visited.add(task_id)

    for dependency_id in task.get('dependencies', []):
        for t in tasks:
            if t.get('id') == dependency_id:
                if has_circular_dependency(t, tasks, visited):
                    return True
    
    return False
    

def get_priority_score(task, tasks):
    # importance: 1-10
    score = 0
    importance = task["importance"]
    score += importance * 5

    # urgency
    due_date_str = task["due_date"]
    if due_date_str:
        try:
            due_date = datetime.strptime(due_date_str, "%Y-%m-%d")
            hours_left = (due_date - datetime.now()).total_seconds() // 3600

            if hours_left < 0:
                score += 40
            elif hours_left < 24:
                score += 30
            elif hours_left < 72:
                score += 20
            else:
                score += 10
        except ValueError:
            score += 0
    else:
        score += 5

    # estimated time
    hours = task.get("estimated_hours", 1)
    if hours <= 1:
        score += 10
    elif hours <= 3:
        score += 7
    else:
        score += 3
    
    # Dependency score
    task_id = task.get('id')
    if task_id:
        count = 0
        for t in tasks:
            if task_id in t.get('dependencies', []):
                count += 1
        score += min(count * 5, 10)
    
    if has_circular_dependency(task, tasks):
        score -= 10
    
    return score
    

if __name__ == '__main__':
    tasks = [
        {"id": 1, "title": "Fix Bug", "due_date": "2025-11-29", "estimated_hours": 2, "importance": 10, "dependencies": []},
        {"id": 2, "title": "Update Readme", "due_date": "2025-12-30", "estimated_hours": 1, "importance": 5, "dependencies": []},
        {"id": 3, "title": "Big Project", "due_date": "2026-01-01", "estimated_hours": 15, "importance": 8, "dependencies": [1]},
        {"id": 4, "title": "Task A", "due_date": "2025-12-15", "estimated_hours": 3, "importance": 7, "dependencies": []},
        {"id": 5, "title": "Task B", "due_date": "2025-12-16", "estimated_hours": 2, "importance": 6, "dependencies": [4]},
    ]

    for t in tasks:
        t['priority_score'] = get_priority_score(t, tasks)

    sorted_tasks = sorted(tasks, key=lambda x:x['priority_score'], reverse=True)
    
    for t in sorted_tasks:
        print(t["title"], "is", t['priority_score'])