import random

# Function that generates the HTML file for visualizing the output
def generate_html_file(output_file, input_file, html_file):
    """
    Generate an HTML file to display the input, output, and a Gantt chart of the scheduling process.

    Parameters:
    output_file (str): The name of the output file.
    input_file (str): The name of the input file.
    html_file (str): The name of the HTML file to be generated.
    """
    # Read the input file content
    with open(input_file, 'r') as file:
        input_content = file.read()

    # Read the output file content
    with open(output_file, 'r') as file:
        output_content = file.readlines()

    # Extract process names and events for the Gantt chart
    events = []
    max_time = 0
    for line in output_content:
        if line.startswith("Time"):
            time, event = line.split(" : ")
            time = int(time.strip().split()[1])
            event = event.strip()
            events.append((time, event))
            if "finished" in event:
                max_time = max(max_time, time)

    # Create a dictionary to hold the Gantt chart data
    gantt_data = {}
    process_colors = {}
    predefined_colors = [
        "#FF6347", "#4682B4", "#32CD32", "#FFD700", "#8A2BE2", "#FF1493",
        "#00CED1", "#FF8C00", "#ADFF2F", "#4B0082", "#FF4500", "#7CFC00"
    ]
    current_process = None

    for i in range(max_time + 1):
        gantt_data[i] = "Idle"
        for time, event in events:
            if time == i:
                if "arrived" in event:
                    pass
                elif "selected" in event:
                    current_process = event.split()[0]
                    gantt_data[i] = current_process
                elif "finished" in event:
                    gantt_data[i] = current_process
                    current_process = None
            elif current_process:
                gantt_data[i] = current_process

    # Assign colors to processes
    unique_processes = set(gantt_data.values()) - {"Idle"}
    random.shuffle(predefined_colors)
    for idx, process in enumerate(unique_processes):
        process_colors[process] = predefined_colors[idx % len(predefined_colors)]

    # Initialize the HTML content
    html_content = f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Scheduling Simulation Results</title>
        <style>
            body {{{{ font-family: Arial, sans-serif; }}}}
            h1 {{{{ text-align: center; }}}}
            h2 {{{{ margin-top: 50px; }}}}
            pre {{{{ background-color: #f4f4f4; padding: 15px; border: 1px solid #ccc; }}}}
            table {{{{ width: 100%; border-collapse: collapse; margin-top: 20px; }}}}
            th, td {{{{ padding: 10px; border: 1px solid #ccc; text-align: center; }}}}
            .idle {{{{ background-color: #f0f0f0; }}}}
            .chart-table {{{{ border: 1px solid black; border-collapse: collapse; width: 100%; }}}}
            .chart-table td {{{{ border: 1px solid black; text-align: center; padding: 5px; }}}}
    """

    # Add styles for each process
    for process, color in process_colors.items():
        html_content += f".{process} {{{{ background-color: {color}; }}}}\n"

    html_content += """
        </style>
    </head>
    <body>
        <h1>Scheduling Simulation Results</h1>
        <h2>Input</h2>
        <pre>{input_content}</pre>
        <h2>Output</h2>
        <pre>{output_content}</pre>
        <h2>Time Frame</h2>
        <table>
            <tr>
                <th>Time</th>
                <th>Event</th>
            </tr>
    """

    # Process the output content to extract events and visualize them
    for line in output_content:
        if line.startswith("Time"):
            time, event = line.split(" : ")
            time = time.strip()
            event = event.strip()
            css_class = "idle" if event == "Idle" else gantt_data[int(time.split()[1])]
            html_content += f"""
            <tr class="{css_class}">
                <td>{time}</td>
                <td>{event}</td>
            </tr>
            """

    # Add the Gantt chart
    html_content += """
        </table>
        <h2>Gantt Chart</h2>
        <table class="chart-table">
            <tr>
    """

    # Add time labels to the Gantt chart
    for i in range(max_time + 1):
        html_content += f"<td>{i}</td>"
    html_content += "</tr><tr>"

    # Add process labels to the Gantt chart
    for i in range(max_time + 1):
        process = gantt_data[i]
        css_class = "idle" if process == "Idle" else process
        html_content += f"<td class='{css_class}'>{process}</td>"

    # Close the HTML tags
    html_content += """
            </tr>
        </table>
    </body>
    </html>
    """

    # Write the HTML content to the file
    with open(html_file, 'w') as file:
        file.write(html_content.format(input_content=input_content, output_content=''.join(output_content)))
