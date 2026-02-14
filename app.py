import numpy as np
import gradio as gr


def generate_expenses(n_days):
    n_days = int(n_days)

    categories_list = np.array(
        ["Food", "Transport", "Shopping", "Bills", "Entertainment"]
    )

    days = np.array([f"Day {i+1}" for i in range(n_days)])
    expenses = np.random.randint(100, 2001, size=n_days)
    categories = np.random.choice(categories_list, size=n_days)

    data = np.column_stack((days, expenses, categories))

    return data, data


def expense_summary(data):
    data = np.array(data)
    expenses = data[:, 1].astype(float)

    total = np.sum(expenses)
    avg = np.mean(expenses)

    highest_idx = np.argmax(expenses)
    highest_day = data[highest_idx, 0]
    highest_amount = expenses[highest_idx]

    above_avg = np.sum(expenses > avg)

    return f"""
### 📊 Expense Summary

**Total Spending:** ₹{total:.2f}  
**Average Daily Spending:** ₹{avg:.2f}  

---

**Highest Spending Day:**  
{highest_day} — ₹{highest_amount:.2f}

---

**Days Above Average:** {above_avg}
"""


def category_breakdown(data):
    data = np.array(data)
    categories = data[:, 2]
    expenses = data[:, 1].astype(float)

    unique = np.unique(categories)

    result = "### 🗂 Category Breakdown\n\n"
    totals = []

    for cat in unique:
        total = np.sum(expenses[categories == cat])
        totals.append(total)
        result += f"**{cat}** — ₹{total:.2f}\n\n"

    totals = np.array(totals)

    highest = unique[np.argmax(totals)]
    lowest = unique[np.argmin(totals)]

    result += "---\n\n"
    result += f"**Highest Spending Category:** {highest}\n\n"
    result += f"**Lowest Spending Category:** {lowest}"

    return result


def high_spending(data, threshold):
    data = np.array(data)
    expenses = data[:, 1].astype(float)
    days = data[:, 0]

    threshold = float(threshold)

    mask = expenses > threshold
    filtered_days = days[mask]
    filtered_expenses = expenses[mask]

    result = "### 🔥 High Spending Days\n\n"

    if len(filtered_days) == 0:
        return result + "No days exceeded the threshold."

    for d, e in zip(filtered_days, filtered_expenses):
        result += f"{d} — ₹{e:.2f}\n"

    return result


with gr.Blocks(title="Expense Tracker") as demo:

    gr.Markdown(
        """
        # 💰 Expense Tracker Dashboard
        Analyze your monthly spending using NumPy-powered analytics.
        """
    )

    data_state = gr.State()

    with gr.Row():
        days_input = gr.Number(value=30, label="Number of Days")
        generate_btn = gr.Button("Generate Expenses", variant="primary")

    expense_table = gr.Dataframe(
        headers=["Day", "Expense (₹)", "Category"],
        interactive=False
    )

    generate_btn.click(
        generate_expenses,
        inputs=days_input,
        outputs=[expense_table, data_state]
    )

    gr.Markdown("---")

    with gr.Tab("📊 Summary"):
        summary_btn = gr.Button("Compute Summary", variant="primary")
        summary_output = gr.Markdown()
        summary_btn.click(expense_summary, inputs=data_state, outputs=summary_output)

    with gr.Tab("🗂 Categories"):
        category_btn = gr.Button("Analyze Categories", variant="primary")
        category_output = gr.Markdown()
        category_btn.click(category_breakdown, inputs=data_state, outputs=category_output)

    with gr.Tab("🔥 High Spending"):
        threshold_input = gr.Number(value=1500, label="Threshold (₹)")
        high_btn = gr.Button("Find High Spending Days", variant="primary")
        high_output = gr.Markdown()
        high_btn.click(
            high_spending,
            inputs=[data_state, threshold_input],
            outputs=high_output
        )

demo.launch(theme=gr.themes.Soft())
