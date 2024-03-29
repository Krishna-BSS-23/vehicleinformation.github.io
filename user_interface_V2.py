import gradio as gr
import pandas as pd

# Read the CSV file containing the vehicle details
df = pd.read_csv("all_vehicle_details.csv")

# Get unique vehicle numbers from the DataFrame
vehicle_numbers = df["Registration Number"].unique()

# Create a Dropdown component for vehicle number selection
dropdown = gr.Dropdown(
    choices=list(vehicle_numbers),
    label="Select or type vehicle number"
)

# Function to display vehicle details based on the input vehicle number
def display_vehicle_details(vehicle_number):
    # Convert the input vehicle number to uppercase
    vehicle_number = vehicle_number.upper()

    # Search for the corresponding row in the DataFrame
    vehicle_info = df[df["Registration Number"].str.upper() == vehicle_number]

    # If vehicle info found, return details as HTML table
    if not vehicle_info.empty:
        details = "<table border='1'>"
        for index, row in vehicle_info.iterrows():
            details += "<tr><td><b>Registration Number:</b></td><td>" + str(row['Registration Number']) + "</td></tr>"
            details += "<tr><td><b>RC Status:</b></td><td>" + str(row['RC Status']) + "</td></tr>"
            details += "<tr><td><b>Vehicle Class:</b></td><td>" + str(row['Vehicle Class']) + "</td></tr>"
            details += "<tr><td><b>Fuel Type:</b></td><td>" + str(row['Fuel Type']) + "</td></tr>"
            details += "<tr><td><b>Model Name:</b></td><td>" + str(row['Model Name']) + "</td></tr>"
            details += "<tr><td><b>Manufacturer Name:</b></td><td>" + str(row['Manufacturer Name']) + "</td></tr>"
            details += "<tr><td><b>Registering Authority:</b></td><td>" + str(
                row['Registering Authority']) + "</td></tr>"
            details += "<tr><td><b>Owner's Name:</b></td><td>" + str(row["Owner's Name"]) + "</td></tr>"
            details += "<tr><td><b>Registration Date:</b></td><td>" + str(row['Registration Date']) + "</td></tr>"
            details += "<tr><td><b>Fitness/Registration Validity:</b></td><td>" + str(
                row['Fitness/Registration Validity']) + "</td></tr>"
            details += "<tr><td><b>MV Tax Validity:</b></td><td>" + str(row['MV Tax Validity']) + "</td></tr>"
            details += "<tr><td><b>PUCC Validity:</b></td><td>" + str(row['PUCC Validity']) + "</td></tr>"
            details += "<tr><td><b>Insurance Company:</b></td><td>" + str(row['Insurance Company']) + "</td></tr>"
            details += "<tr><td><b>Insurance Validity:</b></td><td>" + str(row['Insurance Validity']) + "</td></tr>"
            details += "<tr><td><b>Policy Number:</b></td><td>" + str(row['Policy Number']) + "</td></tr>"
        details += "</table>"
    else:
        details = "Vehicle not found"

    return details

# Create a Gradio interface
iface = gr.Interface(
    fn=display_vehicle_details,
    inputs=dropdown,
    outputs="html",
    title="Vehicle Details",
    description="Select or type the vehicle number to view its details."
)

# Launch the interface
iface.launch()
