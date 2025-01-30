import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from matplotlib.ticker import MultipleLocator, FuncFormatter
from matplotlib.text import Text
from matplotlib.backend_bases import MouseEvent
from tkinter import Tk
from tkinter.filedialog import askopenfilename

class DraggableAnnotation:
    def __init__(self, text: Text):
        """
        DraggableAnnotation allows a text label (annotation) to be dragged with the mouse.
        """
        self.text = text
        self.press = None

        # Connect events for interactivity
        self.cid_press = self.text.figure.canvas.mpl_connect('button_press_event', self.on_press)
        self.cid_motion = self.text.figure.canvas.mpl_connect('motion_notify_event', self.on_motion)
        self.cid_release = self.text.figure.canvas.mpl_connect('button_release_event', self.on_release)

    def on_press(self, event: MouseEvent):
        # Only start if we clicked within the annotation and within this text's axes
        if event.inaxes != self.text.axes:
            return
        bbox = self.text.get_window_extent(self.text.figure.canvas.get_renderer())
        x_disp, y_disp = event.x, event.y
        if bbox.contains(x_disp, y_disp):
            x0, y0 = self.text.get_position()
            self.press = (x0, y0, event.xdata, event.ydata)

    def on_motion(self, event: MouseEvent):
        if self.press is None:
            return
        if event.inaxes != self.text.axes:
            return

        (x0, y0, press_x, press_y) = self.press
        dx = event.xdata - press_x
        dy = event.ydata - press_y

        new_x = x0 + dx
        new_y = y0 + dy

        # Optionally clamp to axis bounds
        ax = self.text.axes
        xlim = ax.get_xlim()
        ylim = ax.get_ylim()

        if new_x < xlim[0]:
            new_x = xlim[0]
        elif new_x > xlim[1]:
            new_x = xlim[1]
        if new_y < ylim[0]:
            new_y = ylim[0]
        elif new_y > ylim[1]:
            new_y = ylim[1]

        self.text.set_position((new_x, new_y))
        self.text.figure.canvas.draw()

    def on_release(self, event: MouseEvent):
        if self.press is not None:
            self.press = None

def main():
    Tk().withdraw()
    file_path = askopenfilename(title="Select Excel File", filetypes=[("Excel files", "*.xlsx *.xls")])
    if not file_path:
        print("No file selected. Exiting...")
        return

    try:
        df = pd.read_excel(file_path)

        required_cols = {"Date", "Pay", "Comment", "Age"}
        if not required_cols.issubset(df.columns):
            print("The file must contain 'Date', 'Pay', 'Comment', and 'Age' columns.")
            return

        # Convert Date to datetime & sort
        df['Date'] = pd.to_datetime(df['Date'])
        df.sort_values(by='Date', inplace=True)
        df.reset_index(drop=True, inplace=True)

        # Convert the 'Date' column to Matplotlib’s float format
        df['mpl_date'] = mdates.date2num(df['Date'])

        # Determine the maximum pay
        max_pay = df['Pay'].max()
        # Calculate the next multiple of 10k above max_pay
        top_lim_candidate = ((int(max_pay) // 10000) + 1) * 10000
        # If within 2k of this boundary, jump up an extra 10k
        if (top_lim_candidate - max_pay) <= 2000:
            top_lim = top_lim_candidate + 10000
        else:
            top_lim = top_lim_candidate

        # Create the figure
        fig, ax = plt.subplots()
        ax.plot(df['mpl_date'], df['Pay'], marker='o', linestyle='-', label='Salary')

        # Format x-axis as dates
        ax.xaxis_date()
        ax.set_xlabel("Date (Age)")
        ax.set_ylabel("Salary ($)")
        ax.set_title("Salary Progression Over Time")

        # Set the y-axis from 0 to the new top limit
        ax.set_ylim(0, top_lim)
        # Major ticks every 10k
        ax.yaxis.set_major_locator(MultipleLocator(10000))
        # Format y ticks as currency
        ax.yaxis.set_major_formatter(FuncFormatter(lambda x, _: f"${x:,.0f}"))

        # Create the custom x tick labels with date + age
        xticks_labels = [
            f"{dt.strftime('%Y-%m-%d')} ({age})"
            for dt, age in zip(df['Date'], df['Age'])
        ]
        ax.set_xticks(df['mpl_date'])
        ax.set_xticklabels(xticks_labels, rotation=45, ha="right")

        ax.grid(True, linestyle="--", alpha=0.6)

        # Add annotations
        annotations = []
        for i, comment in enumerate(df['Comment']):
            annotation = ax.text(
                df['mpl_date'].iloc[i],
                df['Pay'].iloc[i],
                comment,
                ha='center',
                va='bottom',
                bbox=dict(
                    boxstyle="round,pad=0.3",
                    edgecolor="gray",
                    facecolor="white",
                    alpha=0.8
                )
            )
            annotations.append(DraggableAnnotation(annotation))

        # Print final positions upon closing
        def on_close(event):
            print("Final annotation positions:")
            for idx, ann in enumerate(annotations):
                final_x, final_y = ann.text.get_position()
                final_dt = mdates.num2date(final_x)
                print(f"Annotation {idx}: {final_dt}, {final_y}")

        fig.canvas.mpl_connect('close_event', on_close)

        plt.tight_layout()
        plt.show()

    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()
