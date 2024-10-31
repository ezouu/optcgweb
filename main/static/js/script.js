async function fetchCards() {
    try {
        // Fetch data from the /cards endpoint
        const response = await fetch('/cards');
        
        // Check if the response is OK (status code 200)
        if (!response.ok) throw new Error("Failed to fetch cards.");

        // Parse the JSON data
        const cards = await response.json();

        // Select the #cards-list div
        const listDiv = document.getElementById("cards-list");
        listDiv.innerHTML = ''; // Clear any existing content

        // Display each card as a paragraph
        cards.forEach(card => {
            listDiv.innerHTML += `
                <p>
                    <strong>Rarity:</strong> ${card.Rarity}<br>
                    <strong>Number:</strong> ${card.Number}<br>
                    <strong>Price:</strong> ${card.Price}
                </p>`;
        });
    } catch (error) {
        console.error("Error:", error);
    }
}
