##########################################
# Graphy v1.0                            #
# (C) 2023 Abdon Morales                 #
# https://github.com/abdonmorales/graphy #
# September 8, 2023                      #
##########################################

# Import the necessary modules
import tkinter as tk
from tkinter import ttk
from tkinter import simpledialog
import numpy as np
import sympy as sp
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk

# The commented-out sections of code below are going to be implemented in later releases.

class GraphingCalculator(tk.Tk):
    def __init__(self):
        super().__init__()

        # Window title
        self.title("Graphy Release I")

        # Create the input area for function
        self.func_label = ttk.Label(self, text="Enter function:")
        self.func_label.grid(row=0, column=0, padx=10, pady=5, sticky="w")

        self.func_input = ttk.Entry(self, width=30)
        self.func_input.grid(row=0, column=1, padx=10, pady=5, columnspan=3)

        # Math buttons
        self.add_button = ttk.Button(
            self, text="+", command=lambda: self.append_symbol("+"))
        self.add_button.grid(row=1, column=0, padx=5, pady=5)

        self.sub_button = ttk.Button(
            self, text="-", command=lambda: self.append_symbol("-"))
        self.sub_button.grid(row=1, column=1, padx=5, pady=5)

        self.mul_button = ttk.Button(
            self, text="*", command=lambda: self.append_symbol("*"))
        self.mul_button.grid(row=1, column=2, padx=5, pady=5)

        self.div_button = ttk.Button(
            self, text="/", command=lambda: self.append_symbol("/"))
        self.div_button.grid(row=1, column=3, padx=5, pady=5)

        self.sqrt_button = ttk.Button(
            self, text="sqrt", command=lambda: self.append_symbol("sqrt"))
        self.sqrt_button.grid(row=2, column=0, padx=5, pady=5)

        self.abs_button = ttk.Button(
            self, text="abs", command=lambda: self.append_symbol("abs"))
        self.abs_button.grid(row=2, column=1, padx=5, pady=5)

        self.pow_button = ttk.Button(
            self, text="^", command=lambda: self.append_symbol("**"))
        self.pow_button.grid(row=2, column=2, padx=5, pady=5)

        self.clear_button = ttk.Button(
            self, text="Clear", command=self.clear_input)
        self.clear_button.grid(row=2, column=3, padx=5, pady=5)

        # 2D and 3D switch (3D doesn't work yet)
        self.view_var = tk.StringVar(value="2D")
        self.view_2d_button = ttk.Radiobutton(self, text="2D", variable=self.view_var, value="2D")
        self.view_2d_button.grid(row=1, column=2, padx=5, pady=5)
        #self.view_3d_button = ttk.Radiobutton(self, text="3D", variable=self.view_var, value="3D")
        #self.view_3d_button.grid(row=1, column=3, padx=5, pady=5)

        # Plot button
        self.plot_button = ttk.Button(
            self, text="Plot", command=self.plot_function)
        self.plot_button.grid(row=3, column=0, padx=10, pady=5, columnspan=4)

        # Create an area for the graph
        self.fig = plt.figure(figsize=(5, 5))
        self.canvas = FigureCanvasTkAgg(self.fig, master=self)
        self.canvas.get_tk_widget().grid(row=4, column=0, padx=10,
                                         pady=5, columnspan=4, sticky='nsew')

        # Add the navigation toolbar
        # Add the navigation toolbar inside a frame
        self.toolbar_frame = ttk.Frame(self)
        self.toolbar_frame.grid(row=5, column=0, padx=10, pady=5, columnspan=4, sticky='nsew')

        self.toolbar = NavigationToolbar2Tk(self.canvas, self.toolbar_frame)
        self.toolbar.update()
        self.toolbar.pack()

        # Adding show table button to display the table of x and y of a function or expression
        self.show_table_button = ttk.Button(self, text="Show Table", command=self.show_table)
        self.show_table_button.grid(row=6, column=0, padx=10, pady=5, columnspan=4)

        #self.canvas.get_tk_widget().grid(row=5, column=0, padx=10, pady=5, columnspan=4)

        # Make the graph area expand with the window
        self.grid_rowconfigure(4, weight=1)
        for i in range(4):
            self.grid_columnconfigure(i, weight=1)

    def append_symbol(self, symbol):
        current_text = self.func_input.get()
        updated_text = current_text + symbol
        self.func_input.delete(0, tk.END)
        self.func_input.insert(0, updated_text)

    def clear_input(self):
        self.func_input.delete(0, tk.END)

    def plot_function(self):
        self.fig.clf()
        func_str = self.func_input.get()
        func_str = func_str.replace(
            "^", "**").replace("sqrt", "np.sqrt").replace("abs", "np.abs")
        x = np.linspace(-10, 10, 400)
        try:
            y = eval(func_str)
            ax = self.fig.add_subplot(111)
            ax.plot(x, y, label=func_str)
            ax.legend()
            ax.grid(True)
            ax.axhline(y=0, color='k')
            ax.axvline(x=0, color='k')
        except Exception as e:
            print(f"Error plotting function: {e}")
#        if hasattr(self, "diff_func"):
#            y_diff_vals = [float(eval(str(self.diff_func))) for val in x_vals]
#            ax.plot(x_vals, y_diff_vals, label=f"Derivative of {func_str}", linestyle="--")
#            delattr(self, "diff_func")
    
#        if hasattr(self, "integrate_func"):
#            y_integrate_vals = [float(sp.integrate(func_str, (x, -10, val))) for val in x_vals]
#            ax.fill_between(x_vals, y_integrate_vals, label=f"Integral of {func_str}", alpha=0.3)
#            delattr(self, "integrate_func")

#        if hasattr(self, "solutions"):
#            y_solution_vals = [float(eval(func_str)) for val in self.solutions]
#            ax.scatter(self.solutions, y_solution_vals, color='red', zorder=5)
#            delattr(self, "solutions")
        self.canvas.draw()
    
    def show_table(self):
        # Create a new window to display table of values
        table_window = tk.Toplevel(self)
        table_window.title("Table of Values")
    
    # Create a Treeview to show x, y table
        tree = ttk.Treeview(table_window, columns=("X", "Y"), show="headings")
        tree.heading("X", text="X")
        tree.heading("Y", text="Y")
        tree.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)
    
    # Evaluate the function for a range of x values and populate the treeview
        func_str = self.func_input.get().replace("^", "**").replace("sqrt", "np.sqrt").replace("abs", "np.abs")
        x_values = np.linspace(-10, 10, 21)  # Example range from -10 to 10 with 0.5 interval
        for x in x_values:
            try:
                y = eval(func_str)
                tree.insert("", "end", values=(x, y))
            except Exception as e:
                print(f"Error evaluating function at x={x}: {e}")
    def solve_input(self):
        input_str = self.func_input.get().replace("^", "**").replace("sqrt", "sp.sqrt").replace("abs", "sp.Abs")
        if "=" in input_str:
            # If the input contains an equals sign, treat it as an equation to solve
            equation = input_str.split("=")
            x = sp.Symbol('x')
            try:
                solution = sp.solve(sp.Eq(eval(equation[0]), eval(equation[1])), x)
                simpledialog.messagebox.showinfo("Solution", f"Solution for {input_str}: x = {solution}")
            except Exception as e:
                simpledialog.messagebox.showerror("Error", f"Error solving equation: {e}")
        else:
            # Otherwise, treat it as an expression to evaluate
            try:
                result = eval(input_str)
                simpledialog.messagebox.showinfo("Result", f"Result for {input_str}: {result}")
            except Exception as e:
                simpledialog.messagebox.showerror("Error", f"Error evaluating expression: {e}")
#    def differentiate_function(self):
#        func_str = self.func_input.get().replace("^", "**").replace("sqrt", "sp.sqrt").replace("abs", "sp.Abs")
#        x = sp.Symbol('x')
#       try:
#            self.diff_func = sp.diff(eval(func_str), x)
#            simpledialog.messagebox.showinfo("Differentiation Result", f"d/dx of {func_str} is {self.diff_func}")
#            self.plot_function()
#        except Exception as e:
#            print(f"Error differentiating function: {e}")
#
#    def integrate_function(self):
#        func_str = self.func_input.get().replace("^", "**").replace("sqrt", "sp.sqrt").replace("abs", "sp.Abs")
#        x = sp.Symbol('x')
#        try:
#            self.integrate_func = sp.integrate(eval(func_str), x)
#            simpledialog.messagebox.showinfo("Integration Result", f"∫({func_str}) dx = {self.integrate_func}")
#            self.plot_function()
#        except Exception as e:
#            print(f"Error integrating function: {e}")
#
#    def solve_function(self):
#        func_str = self.func_input.get().replace("^", "**").replace("sqrt", "sp.sqrt").replace("abs", "sp.Abs")
#        x = sp.Symbol('x')
#        try:
#            self.solutions = [float(sol) for sol in sp.solve(eval(func_str), x) if -10 <= float(sol) <= 10]
#            simpledialog.messagebox.showinfo("Solve Result", f"Solutions of {func_str} = 0 are {self.solutions}")
#            self.plot_function()
#        except Exception as e:
#            print(f"Error solving function: {e}")
# Create and run the graphing calculator GUI
if __name__ == "__main__":
    app = GraphingCalculator()
    app.mainloop()
