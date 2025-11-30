from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from tasks.scoring import get_priority_score
import json

from datetime import datetime

def build_explanation(task):
    explanation = []

    # Importance 
    explanation.append(f"Importance: {task['importance']}")

    # urgency
    if task.get('due_date'):
        try:
            due_date = datetime.strptime(task['due_date'], '%Y-%m-%d')
            hrs_left = (due_date - datetime.now()).total_seconds() // 3600

            if hrs_left < 0:
                explanation.append('Task is already past due date, making it urgent')
            elif hrs_left < 24:
                explanation.append('Task is Due within 24hrs')
            elif hrs_left < 72:
                explanation.append('Task is Due withing 72hrs')
            else:
                explanation.append('Task is not due, do complete the task')
        
        except:
            explanation.append('Invalid date format')
    else:
        explanation.append('No due date, Good work there!')



    # Effort
    hours = task.get('estimated_hours', 1)
    if hours <= 1:
        explanation.append('Task done earlier, Congrats!!')
    elif hours <= 3:
        explanation.append('Fair time to do a task')
    else:
        explanation.append('High effort tasks to be done slowly but consistently')


    # Dependencies
    if len(task.get('dependencies', [])) > 0:
        explanation.append('Complete the past due tasks to complete the next ones')
    else:
        explanation.append('No dependencies, if other tasks are remaining do complete them')

    
    return ", ".join(explanation)
    


# Analyze the task and provide a priority score
@csrf_exempt
def analyze_task(request):
    # print(request.body, request.method)

    # return JsonResponse({"message": "Analyse response is working"})
    if request.method != 'POST':
        return JsonResponse({'error': 'Invalid Request'}, status=405)

    try:
        data = json.loads(request.body)
    except:
        return JsonResponse({'error': 'Invalid JSON Data'}, status=400)

    tasks = data if isinstance(data, list) else data.get('tasks', [])

    if not isinstance(tasks, list):
        return JsonResponse({'error': 'Task must be an array'}, status=400)

    for t in tasks:
        t['priority_score'] = get_priority_score(t, tasks)
        t['explanation'] = build_explanation(t)

    
    sorted_tasks = sorted(tasks, key=lambda x:x['priority_score'], reverse=True)

    return JsonResponse({'Sorted Tasks': sorted_tasks}, safe=False)


    # Suggest the tasks
@csrf_exempt
def suggest_tasks(request):
    if request.method != 'GET':
        return JsonResponse({'error': 'Invalid Request'}, status=405)

    try:
        body = request.body.decode('utf-8')
        tasks = json.loads(body) if body else []
    
    except:
        return JsonResponse({'error': 'Invalid JSON Data'}, status=400)
    
    if not isinstance(tasks, list):
        return JsonResponse({'error': 'Tasks should be in a list'}, status=400)

    
    # find score
    for t in tasks:
        t['priority_score'] = get_priority_score(t, tasks)
        t['explanation'] = build_explanation(t)

    # Top 3 tasks for today
    top_three = sorted(tasks, key=lambda x:x['priority_score'], reverse=True)[:-3]

    return JsonResponse({
        "suggested_tasks": top_three,
        "message": "These are the top 3 tasks picked for today"
    })
