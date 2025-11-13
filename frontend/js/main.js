const API_URL = "http://127.0.0.1:8000/expenses";

document.getElementById("expenseForm").addEventListener("submit", async (e) => {
  e.preventDefault();
  const expense = {
    title: document.getElementById("title").value,
    amount: parseFloat(document.getElementById("amount").value),
    type: document.getElementById("type").value,
    date: new Date().toISOString(),
  };
  await fetch(API_URL, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(expense),
  });
  loadExpenses();
});

async function loadExpenses() {
  const res = await fetch(API_URL);
  const data = await res.json();
  document.getElementById("expenseList").innerHTML =
    data.map(x => `
      <div class="bg-white p-3 mb-2 shadow rounded flex justify-between">
        <span>${x.title} (${x.type})</span>
        <span>${x.amount} PKR</span>
      </div>`).join('');
}
loadExpenses();
