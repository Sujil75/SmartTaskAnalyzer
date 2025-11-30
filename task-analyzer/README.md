# 📘 README.md Template (Polished & Recruiter-Ready)

## Smart Task Analyzer – Internship Assignment
### 📌 Overview
This project implements an intelligent task scoring system that helps users identify which tasks they should work on first. It uses Django for the backend and JavaScript/HTML/CSS for the frontend.

The heart of the system is a custom priority algorithm that weighs urgency, importance, effort, and dependencies.

---
---

### 🧠 How the Algorithm Works

The scoring algorithm considers several factors:

### 1. Urgency (High Weight)

Tasks closer to their due date receive higher priority.

  - Past due tasks → highest boost

  - Due within 24 hours → high urgency

  - Due within 3 days → medium

  - More than 3 days → low urgency

**Reason**: Urgency directly affects deadlines and is more time-critical than effort.

---

### 2. Importance (Medium-High Weight)

Importance is on a 1–10 scale.

- More important tasks get more points.

**Reason**: Important work should not be neglected even if effort is higher.

---

### 3. Effort (Low-Medium Weight)


Small tasks get a slight boost (quick wins).

- <= 1 hour → quick win

- <= 3 hours → moderate

- 3 hours → slight penalty

**Reason**: Quick wins help productivity but shouldn't outweigh urgency.

---

### 4. Dependencies

Tasks that block others get a boost.

**Reason**: Removing bottlenecks helps the overall workflow.

---

### 5. Circular Dependency Handling

If tasks create a dependency loop:

- The task is penalized heavily.

**Reason**: Circular dependencies stop progress entirely and must be fixed first.

---
---

## 🔍 Edge Case Handling

### 1. Task due in 1990

Old tasks are treated as extremely urgent, because:

- They are past-due

- They may block other tasks

- They likely need attention immediately

---

### 2. Missing Importance

If importance is missing or invalid:

```
importance = task.get("importance", 5)
```

Default importance = 5 (medium).

### 3. Invalid or missing due date

Invalid dates do not crash the app. They receive minimal urgency.

### 4. Missing estimated time

Defaults to 1 hour.

### 5. Circular dependencies

Automatically detected and penalized.

---
---

## 🚀 Running the Project

### 1. Install Dependencies
```
bash
pip install -r requirements.txt
```

### 2. Run Django server

```
python manage.py runserver
```

#### Starts at:
http://127.0.0.1:8000/


### 3. Open the frontend
Open frontend/index.html using your browser or Live Server.

---
---

## Running Unit Tests
```
python manage.py test
```

Tests include:
- Past due date
- Missing importance
- Circular dependency
- Low/high effort scoring

---
---

### Future Improvements
- Add user-defined weighting
- Add login & user profiles
- Integrate charts for better visualization
- Improve ML-based task suggestions