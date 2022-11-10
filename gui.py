from tkinter.scrolledtext import ScrolledText
import tkinter as tk
from tkinter import ttk
from flopper import *

texture_labels = ["rainbow", "two tone", "monotone", "straight possible", "paired", "tripsed"
                 , "card present", "lowest card", "highest card"]


class FlopperGui(tk.Tk):

    def __init__(self):

        super().__init__()

        self.title("Holdem Flopper")
        self.geometry("380x600")
        self.resizable(0, 0)
        # self.rowconfigure(7)
        # self.columnconfigure(2)


        self.texture_options = texture_labels
        self.texture_clicked = tk.StringVar(self)
        self.logical_operator_clicked = tk.StringVar(self)
        self.filter_negation_clicked = tk.StringVar(self)


        self.ranks_clicked = tk.StringVar()
        self.ranks_and_or_clicked = tk.StringVar(self)

        self.ranks_card_options = cards
        self.ranks_card_clicked = tk.StringVar()
        self.ranks_card_button_enabled = 0

        self.and_or_options = ["AND ", "OR "]

        self.filter_field_text = tk.StringVar(self)
        self.filter_field = tk.Text(self, width=20, height=10)

        self.create_widgets()

    def create_widgets(self):

        texture_frame = tk.Frame(self)
        texture_frame.config(borderwidth=1, relief='sunken')
        texture_frame.grid(column=1, row=1, pady=10, sticky=tk.EW)

        texture_label = tk.Label(texture_frame, text="Select flop texture filter", font=12)
        texture_label.grid(column=1, row=0, columnspan=2)

        texture_dropdown = ttk.OptionMenu(texture_frame, self.texture_clicked, "monotone", *self.texture_options)
        texture_dropdown.grid(column=1, row=1, pady=2)
        ranks_card_dropdown = ttk.OptionMenu(texture_frame, self.ranks_card_clicked, "A", *self.ranks_card_options)

        ranks_card_dropdown.grid(column=2, row=1, pady=2)

        logical_frame = tk.Frame(self)
        logical_frame.grid(column=1, row=2, pady=10, sticky=tk.EW)
        logical_frame.config(borderwidth=1, relief='sunken')

        logical_label = tk.Label(logical_frame, text="Select logical operator", font=12)
        logical_label.grid(column=1, row=1, columnspan=2)

        and_or_dropdown = ttk.OptionMenu(logical_frame, self.logical_operator_clicked, "AND ", *self.and_or_options)
        and_or_dropdown.grid(column=1, row=2, padx=10, pady=2, columnspan=2)

        negation_label = tk.Label(logical_frame, text="Click to negate the filter", font=12)
        negation_label.grid(column=1, row=3, columnspan=2)

        negation_box = ttk.Checkbutton(logical_frame, text="NOT", variable=self.filter_negation_clicked, onvalue="NOT ", offvalue="")
        negation_box.grid(column=1, row=4, columnspan=2)

        add_filter_button = ttk.Button(self, text="ADD FILTER", command=self.add_filter)
        add_filter_button.grid(column=1, row=3, pady=5)

        self.filter_field.grid(column=1, row=4)

        get_flops_button = tk.Button(self, text="GET FLOP LIST", command='', bg='light green')
        get_flops_button.grid(column=1, row=5, pady=5)

        flop_list_frame = tk.Frame(self)
        flop_list_frame.config(borderwidth=1, relief="sunken")
        flop_list_frame.grid(column=2, row=1, pady=10,padx=10, rowspan=5)

        flop_list_label = tk.Label(flop_list_frame, text="Filtered canonical flop list ", font=12)
        flop_list_label.grid(column=2, row=0, columnspan=1)

        flop_list_field = ScrolledText(flop_list_frame, width=20, height=30)
        flop_list_field.grid(column=2, row=1, padx=2, rowspan=4)

    def add_filter(self):
        if "card" not in self.texture_clicked.get():
            if len(self.filter_field.get('0.0', 'end')) < 2:
                self.filter_field.insert('end', self.filter_negation_clicked.get() + self.texture_clicked.get() + "\n")
            else:
                self.filter_field.insert('end', self.logical_operator_clicked.get() + self.filter_negation_clicked.get()  + self.texture_clicked.get() + "\n")
        else:
            if len(self.filter_field.get('0.0', 'end')) < 2:
                self.filter_field.insert('end', self.filter_negation_clicked.get() + self.texture_clicked.get()  + " " + self.ranks_card_clicked.get() + "\n")
            else:
                self.filter_field.insert('end', self.logical_operator_clicked.get() + self.filter_negation_clicked.get()  + self.texture_clicked.get() + " " + self.ranks_card_clicked.get() + "\n")


gui = FlopperGui()
gui.mainloop()
