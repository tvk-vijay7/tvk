// Autocomplete functionality for location input
document.addEventListener('DOMContentLoaded', function() {
    const input = document.getElementById("locationInput");
    const suggestions = document.getElementById("suggestions");
    
    if (!input || !suggestions) {
        return; // Exit if elements don't exist on this page
    }

    // Handle input events for autocomplete
    input.addEventListener("input", function() {
        const query = input.value.trim().toLowerCase();
        suggestions.innerHTML = "";
        
        if (!query) {
            return;
        }

        // Filter locations that match the query
        const matches = locations.filter(location => 
            location.toLowerCase().includes(query)
        );

        // Show up to 10 matches
        matches.slice(0, 10).forEach(match => {
            const li = document.createElement("li");
            li.textContent = match;
            li.addEventListener("click", function() {
                input.value = match;
                suggestions.innerHTML = "";
            });
            suggestions.appendChild(li);
        });
    });

    // Hide suggestions when clicking outside
    document.addEventListener("click", function(event) {
        if (event.target !== input && !suggestions.contains(event.target)) {
            suggestions.innerHTML = "";
        }
    });

    // Handle keyboard navigation
    input.addEventListener("keydown", function(event) {
        const items = suggestions.querySelectorAll("li");
        let activeItem = suggestions.querySelector("li.active");
        
        if (event.key === "ArrowDown") {
            event.preventDefault();
            if (activeItem) {
                activeItem.classList.remove("active");
                activeItem = activeItem.nextElementSibling || items[0];
            } else {
                activeItem = items[0];
            }
            if (activeItem) {
                activeItem.classList.add("active");
            }
        } else if (event.key === "ArrowUp") {
            event.preventDefault();
            if (activeItem) {
                activeItem.classList.remove("active");
                activeItem = activeItem.previousElementSibling || items[items.length - 1];
            } else {
                activeItem = items[items.length - 1];
            }
            if (activeItem) {
                activeItem.classList.add("active");
            }
        } else if (event.key === "Enter") {
            if (activeItem) {
                event.preventDefault();
                input.value = activeItem.textContent;
                suggestions.innerHTML = "";
            }
        } else if (event.key === "Escape") {
            suggestions.innerHTML = "";
        }
    });

    // Add CSS for active item highlighting
    const style = document.createElement('style');
    style.textContent = `
        .suggestions li.active {
            background-color: #e60000 !important;
            color: white !important;
        }
    `;
    document.head.appendChild(style);
});
