import cmath
import sys
import numpy as np
import matplotlib.pyplot as plt
from PyQt5.QtWidgets import (QApplication, QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, QHBoxLayout,
                             QMessageBox, QFileDialog)
from PyQt5.QtCore import Qt, QTimer
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT
import datetime


# Rasm nemodar
rasm_nemodarstart = 50
rasm_nemodarend = 50
narmi_khat = 1000

# Target Time
target = datetime.datetime(2025, 2, 10, 12, 0, 0)

tel = "@RxA66"
telegram = f"Telegram : {tel}"


class PlotWindow(QWidget):
    def __init__(self, a, b, c, delta_zero=False, roots=None):
        super().__init__()

        self.setWindowTitle("R.A : Quadratic Equation Graph")
        self.setGeometry(100, 100, 800, 600)  # Size and position of the new window

        # Create the plot canvas
        self.canvas = FigureCanvas(plt.figure())
        self.plot_graph(a, b, c, delta_zero, roots)

        # Create the Navigation Toolbar
        self.toolbar = NavigationToolbar2QT(self.canvas, self)

        # Layout for the new window
        vbox = QVBoxLayout()
        vbox.addWidget(self.toolbar)
        vbox.addWidget(self.canvas)

        self.setLayout(vbox)

    def plot_graph(self, a, b, c, delta_zero, roots):
        fig = self.canvas.figure
        ax = fig.add_subplot(111)
        ax.clear()  # Clear previous plot

        # Plotting the quadratic equation graph
        x = np.linspace(-rasm_nemodarstart, rasm_nemodarend, narmi_khat)
        y = a * x ** 2 + b * x + c

        # Plot the parabola
        ax.plot(x, y, label=f'{a}x² + {b}x + {c}')
        ax.axhline(0, color='black', linewidth=1)
        ax.axvline(0, color='black', linewidth=1)

        # If delta is zero or roots are provided, plot them
        if roots:
            for root in roots:
                ax.scatter(root, 0, color='red', zorder=5)  # Plot root
                ax.text(root, 0.5, f'Root = {root:.2f}', color='red', ha='center', fontsize=12)  # Display root value

        if delta_zero:
            ax.set_title(f"Quadratic Equation with a Double Root at x = {roots[0]}")
        else:
            ax.set_title("R.A : Quadratic Equation Graph")

        ax.set_xlabel("x")
        ax.set_ylabel("y")
        ax.legend()

        # Prevent invalid log10 issues by setting axis limits
        ax.set_xlim([-rasm_nemodarstart, rasm_nemodarend])

        # Set dynamic y-limits based on y data but ensure it's positive or zero
        ax.set_ylim(min(y) - 10, max(y) + 10)

        # Redraw the canvas
        self.canvas.draw()


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.ra_label = QLabel("Created by : Reza Afrasyabi")
        self.zaman_Label = QLabel(self)
        self.a_input = QLineEdit(self)
        self.b_input = QLineEdit(self)
        self.c_input = QLineEdit(self)
        self.calculate_button = QPushButton("Calculate")
        self.exit_button = QPushButton("Exit", self)

        # History label to display the history
        self.history_label = QLabel(" ", self)
        self.history_label.setStyleSheet("""
            QLabel {
                font-size: 18px;
                color: #FFD700;
                font-family: "Comic Sans MS", cursive, sans-serif;
                text-align: left;
            }
        """)

        self.history = []  # List to store calculation history
        self.initUI()

    def initUI(self):
        self.setWindowTitle("R.A 2.Dereceden Denklemler")

        # Layouts
        vbox = QVBoxLayout()
        hbox = QHBoxLayout()

        # Adding QLabel for the quadratic equation representation
        equation_label = QLabel(""" 
        <html><body style="font-family: Arial; font-size: 24px; color: #FFD700;">
        <p style="text-align: center;">ax<sup>2</sup> + bx + c = 0</p>
        </body></html>
        """)

        # Adding elements to the layouts
        vbox.addWidget(equation_label)
        vbox.addWidget(self.ra_label)
        vbox.addWidget(self.zaman_Label)

        vbox.addWidget(QLabel("Enter a:"))
        vbox.addWidget(self.a_input)

        vbox.addWidget(QLabel("Enter b:"))
        vbox.addWidget(self.b_input)

        vbox.addWidget(QLabel("Enter c:"))
        vbox.addWidget(self.c_input)

        vbox.addWidget(self.calculate_button)

        # History section
        vbox.addWidget(self.history_label)

        hbox.addStretch(1)
        hbox.addWidget(self.exit_button)
        vbox.addLayout(hbox)

        self.setLayout(vbox)

        # Styling
        self.setStyleSheet("""
            QWidget {
                background-color: #282828;
                color: white;
                border-radius: 10px;
            }

            QLabel {
                font-size: 22px;
                color: #FFB6C1;
                text-align: center;
                font-family: "Comic Sans MS", cursive, sans-serif;
            }

            QLineEdit {
                font-size: 18px;
                padding: 10px;
                background-color: #3a3a3a;
                color: #FFD700;
                border-radius: 8px;
                border: 2px solid #FF1493;
            }

            QLineEdit:focus {
                border-color: #FF69B4;
            }

            QPushButton {
                font-size: 20px;
                font-weight: bold;
                background-color: #FF6347;
                color: white;
                border: 2px solid #FF4500;
                border-radius: 15px;
                padding: 15px;
                margin: 10px;
                transition: background-color 0.3s, transform 0.2s;
            }

            QPushButton:hover {
                background-color: #FF4500;
                transform: scale(1.1);
            }

            QPushButton:pressed {
                background-color: #FF1493;
                transform: scale(1);
            }

            QPushButton#exit_button {
                background-color: #32CD32;
                border-color: #228B22;
            }

            QPushButton#exit_button:hover {
                background-color: #228B22;
            }

            QPushButton#exit_button:pressed {
                background-color: #006400;
            }

            QLabel#zaman_Label {
                font-size: 25px;
                color: #32CD32;
            }
        """)

        self.setFixedSize(800, 800)

        # Connecting buttons to methods
        self.calculate_button.clicked.connect(self.calculate)
        self.exit_button.clicked.connect(self.close)

        # Set up a QTimer to update the remaining time every second
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_time)
        self.timer.start(1000)

    def update_time(self):
        now = datetime.datetime.now()
        Zamane_baghi = target - now

        if Zamane_baghi.total_seconds() <= 0:
            self.show_error()
            self.close()

        days = Zamane_baghi.days
        hours = Zamane_baghi.seconds // 3600
        minutes = (Zamane_baghi.seconds // 60) % 60
        seconds = Zamane_baghi.seconds % 60

        time_left = f"{days} D, {hours} H, {minutes} M, {seconds} S"
        self.zaman_Label.setText(f"Modat zaman baghi mande: {time_left} \n > {telegram}")

    def show_error(self):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Critical)
        msg.setText(f"Eshterak shoma be payan reside ast! baraye kharid be {telegram} payam bedahid.")
        msg.setWindowTitle("payane eshterak!")
        msg.exec_()

    def calculate(self):
        try:
            a = float(self.a_input.text())
            b = float(self.b_input.text())
            c = float(self.c_input.text())
        except ValueError:
            QMessageBox.warning(self, "Input Error", "Please enter valid numbers for a, b, and c!")
            return

        # Check if 'a' is zero
        if a == 0:
            QMessageBox.warning(self, "Input Error", "Value of 'a' cannot be zero for a quadratic equation!")
            return

        # Calculate delta
        d1 = b * b
        d2 = 4 * a * c
        D = d1 - d2

        if D < 0:
            QMessageBox.warning(self, "Error", f"DELTA < 0: {D}")
            return

        if D == 0:
            x1 = -b / (2 * a)
            QMessageBox.information(self, "Solution", f"DELTA = {D}\nX1 = X2 = {x1}")
            self.add_to_history(a, b, c, D, [x1])  # Add to history
            self.plot_window = PlotWindow(a, b, c, delta_zero=True, roots=[x1])
            self.plot_window.show()
            return

        delta = cmath.sqrt(D)
        x1 = (-b + delta) / (2 * a)
        x2 = (-b - delta) / (2 * a)

        if x1.imag == 0:
            x1 = x1.real
        if x2.imag == 0:
            x2 = x2.real

        self.add_to_history(a, b, c, D, [x1, x2])  # Add to history
        self.plot_window = PlotWindow(a, b, c, roots=[x1, x2])
        self.plot_window.show()

        QMessageBox.information(self, "Solution", f"Solution: \n #DELTA = {D}\nX1 = {x1}\nX2 = {x2}")

    def add_to_history(self, a, b, c, delta, roots):
        # Add the calculation to the history list
        history_item = f"Equation: {a}x² + {b}x + {c} = 0\nDelta: {delta}\nRoots: {roots}\n"
        self.history.append(history_item)

        # Update the history label to display the latest calculations
        history_text = "\n".join(self.history[-5:])  # Display only the last 5 calculations
        self.history_label.setText(f"History:\n{history_text}")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
