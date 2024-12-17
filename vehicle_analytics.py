import pandas as pd
import matplotlib.pyplot as plt
from fpdf import FPDF
import tkinter as tk
from tkinter import ttk

# Load your datasets
df_cas = pd.read_csv('E:/vyomikaproject/Vehicle-alert/data/iraste_nxt_cas.csv')
df_casdms = pd.read_csv('E:/vyomikaproject/Vehicle-alert/data/iraste_nxt_casdms.csv')



# Specify the format for 'Time' (e.g., 'HH:MM:SS')
df_cas['Time'] = pd.to_datetime(df_cas['Time'], format='%H:%M:%S', errors='coerce')
df_casdms['Time'] = pd.to_datetime(df_casdms['Time'], format='%H:%M:%S', errors='coerce')

# Combine both datasets into a single DataFrame
df_combined = pd.concat([df_cas[['Alert', 'Time', 'Vehicle', 'Speed']], df_casdms[['Alert', 'Time', 'Vehicle', 'Speed']]])

# Calculate the alert score based on predefined rules or your criteria
def calculate_score(row):
    if row['Speed'] > 60:
        return 0.2
    elif row['Speed'] > 50:
        return 0.1
    else:
        return 0.05

df_combined['alert_score'] = df_combined.apply(calculate_score, axis=1)

# Function to generate the bar chart for the selected alert
def generate_alert_graph(selected_alert):
    # Filter data based on selected alert
    df_filtered = df_combined[df_combined['Alert'] == selected_alert]

    # Check if data exists for the selected alert
    if df_filtered.empty:
        print(f"No data found for the alert: {selected_alert}")
        return

    # Generate the bar chart for alert scores
    alert_scores = df_filtered.groupby('Vehicle')['alert_score'].sum()  # Summing up alert scores by vehicle
    plt.figure(figsize=(10, 6))
    alert_scores.plot(kind='bar', color='skyblue')
    plt.title(f"Alert Scores for {selected_alert}")
    plt.xlabel('Vehicle')
    plt.ylabel('Total Alert Score')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.gca().set_xticklabels([])

    # Display the plot
    plt.show()

    # Generate PDF report for the selected alert
    pdf = FPDF()
    pdf.add_page()

    # Set font for the title and body
    pdf.set_font("Arial", size=12)

    # Title
    pdf.cell(200, 10, txt=f"Vehicle Alert Score Report for {selected_alert}", ln=True, align='C')

    # Add table headers
    pdf.ln(10)  # Add a line break
    pdf.cell(40, 10, "Alert", border=1)
    pdf.cell(40, 10, "Vehicle", border=1)
    pdf.cell(40, 10, "Speed", border=1)
    pdf.cell(40, 10, "Alert Score", border=1)
    pdf.ln()

    # Add data to the PDF for the selected alert
    for index, row in df_filtered.iterrows():
        pdf.cell(40, 10, str(row['Alert']), border=1)
        pdf.cell(40, 10, str(row['Vehicle']), border=1)
        pdf.cell(40, 10, str(row['Speed']), border=1)
        pdf.cell(40, 10, str(row['alert_score']), border=1)
        pdf.ln()

    # Output the PDF
    pdf_output_path = f'C:/Desktop/majproj/Vehicle-Alert-Data-Analytics-main/data/{selected_alert}_alert_score_report.pdf'
    pdf.output(pdf_output_path)

    print(f"PDF report generated at: {pdf_output_path}")

# Tkinter window for dropdown selection
def on_alert_select(event):
    selected_alert = alert_dropdown.get()
    generate_alert_graph(selected_alert)

# Set up Tkinter window
root = tk.Tk()
root.title("Alert Type Selection")

# Create a label
label = tk.Label(root, text="Select an Alert Type:")
label.pack(pady=10)

# Create a dropdown with alert types
alert_types = df_combined['Alert'].unique().tolist()
alert_dropdown = ttk.Combobox(root, values=alert_types, state="readonly")
alert_dropdown.pack(pady=10)

# Bind the event to handle dropdown selection
alert_dropdown.bind("<<ComboboxSelected>>", on_alert_select)

# Run the Tkinter main loop
root.mainloop()