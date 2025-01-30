# Salary Plot with Draggable Annotations

This code reads an Excel file containing salary data with dates, comments, and ages, then plots a salary progression chart over time using Matplotlib. Each comment is displayed as an annotation that can be dragged with the mouse to a new location on the plot.

## How It Works
1. A file dialog opens, prompting you to select an Excel file.
2. The script checks for four columns in the file:
   - **Date** (formatted as dates)
   - **Pay** (salary values)
   - **Comment** (text displayed on the plot)
   - **Age** (any relevant numeric or textual age data)
3. The data is sorted by date, converted to Matplotlib date values, and then plotted.
4. Each annotation placed near a data point can be dragged to a new position.

## Requirements
- Python 3.x
- `pandas`
- `matplotlib`
- `tkinter` (commonly included with most Python installations)

## Setup
1. Clone or download this repository.
2. Install the required packages:
   ```bash
   pip install pandas matplotlib
   ```
3. Ensure that you have a Python environment where `tkinter` is available.

## Running the Script
1. Open a terminal or command prompt in the script's directory.
2. Run:
   ```bash
   python main.py
   ```
3. Select the Excel file when prompted. The chart then appears.
4. Drag annotations with the mouse. The final positions print after the figure closes.

## Notes
- Once you close the chart window, the script prints the final annotation positions, allowing you to track any repositioned text.
- You can modify the behavior of the draggable annotations by changing parameters or adding bounds in the code.

Feel free to adapt or extend this code to suit your specific data visualization needs. If you run into any issues or have suggestions, consider creating a pull request or opening an issue on the repository.
