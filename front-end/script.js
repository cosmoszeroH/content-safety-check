async function checkContent() {
    const text = document.getElementById("userInput").value;
    
    const response = await fetch("http://127.0.0.1:8000/check", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ text: text })
    });
    
    const data = await response.json();
    document.getElementById("result").innerText = JSON.stringify(data, null, 2);
}
