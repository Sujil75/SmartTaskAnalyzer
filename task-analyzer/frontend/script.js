document.getElementById("analyzeBtn").addEventListener("click", async () => {
    const rawInput = document.getElementById("taskInput").value.trim();
    const strategy = document.getElementById("sortingStrategy").value;
    const resultsBox = document.getElementById("results");

    let tasks;

    try {
        tasks = JSON.parse(rawInput);
    } catch (e) {
        resultsBox.innerHTML = "<p style='color:red;'>Invalid JSON format!</p>";
        return;
    }

    try {
        const res = await fetch("http://127.0.0.1:8000/api/tasks/analyze/", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(tasks)
        }) //.then(response => response.json()).then(console.log)

        // console.log(res)
        const data = await res.json();
        const sorted = data["Sorted Tasks"];

        // Apply frontend sorting strategy
        let finalTasks = [...sorted];

        if (strategy === "fastest") {
            finalTasks.sort((a, b) => a.estimated_hours - b.estimated_hours);
        } else if (strategy === "deadline") {
            finalTasks.sort((a, b) => new Date(a.due_date) - new Date(b.due_date));
        }

        resultsBox.innerHTML = "";
        finalTasks.forEach(task => createTaskCard(task));

    } catch (error) {
        resultsBox.innerHTML = "<p style='color:red;'>Server error</p>";
    }
});


// Function to generate dynamic HTML cards
function createTaskCard(task) {
    const parent = document.getElementById("results");

    let priorityClass =
        task.priority_score >= 70 ? "high" :
        task.priority_score >= 40 ? "medium" : "low";

    const card = document.createElement("div");
    card.className = `task-card ${priorityClass}`;

    card.innerHTML = `
        <div class="task-title">${task.title}</div>
        <p><strong>Score:</strong> ${task.priority_score}</p>
        <p><strong>Due:</strong> ${task.due_date}</p>
        <p><strong>Importance:</strong> ${task.importance}</p>
        <p><strong>Estimated Hours:</strong> ${task.estimated_hours}</p>
        <p><strong>Dependencies:</strong> ${task.dependencies.join(", ") || "None"}</p>
        <p class="explanation">${task.explanation}</p>
    `;

    parent.appendChild(card);
}
