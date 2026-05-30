// This script updates history sending request with fetch

// Send data via AJAX
async function update_history(url, data) {
    const response = await fetch(url, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(data)
    });
    const result = await response.json();

    console.log(result);

    // Handle the response
    if (result["success"]) {
        return true;
    } else {
        alert("Error: " + result["error"]);
        return false;
    }

}

const forms_history = document.querySelectorAll('.history')

// This snippet of code with help of cs50.ai
for (let form of forms_history) {

    form.addEventListener('submit', async function(event) {
        event.preventDefault(); // Prevent the default form submission

        // Collect form data
        const formData = new FormData(this);
        const data = Object.fromEntries(formData.entries());

        // Call the async function
        result = await update_history("/update_history", data)

        if (result) {
            // Find the input and button elements
            let actionInput = form.querySelector("input[name='action']");
            let button = form.querySelector("button[type='submit']");

            // Toggle the input value and button class
            if (actionInput.value === "remove") {
                actionInput.value = "add";
                button.classList.remove("btn-danger");
                button.classList.add("btn-success");
                button.textContent = "Add exercise";
            } else {
                actionInput.value = "remove";
                button.classList.remove("btn-success");
                button.classList.add("btn-danger");
                button.textContent = "Remove exercise";
            }
        }
    });
}
