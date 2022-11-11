from tkinter.scrolledtext import ScrolledText
import tkinter as tk
from tkinter import ttk
from flopper import *

texture_labels = ["rainbow", "two tone", "monotone", "straight possible", "paired"
    , "tripsed", "has card", "max bound card", "min bound card"]

filter_dict = {"rainbow": 'is_rainbow(flop)', "two tone": "is_two_tone(flop"
    , "monotone": "is_mono(flop)", "straight possible": "straight_possible(flop)"
    , "paired": "is_paired(flop)", "tripsed": "is_tripsed(flop)", "has card": "has_card(flop, '"
    , "max bound card": "max_bound_card(flop, '", "min bound card": "min_bound_card(flop, '"}


class FlopperGui(tk.Tk):

    def __init__(self):

        super().__init__()

        self.title("Holdem Flopper")
        self.geometry("380x500")
        self.resizable(False, False)

        self.texture_options = texture_labels
        self.texture_clicked = tk.StringVar(self)
        self.logical_operator_clicked = tk.StringVar(self)
        self.filter_negation_clicked = tk.StringVar(self)

        self.ranks_clicked = tk.StringVar()
        self.ranks_and_or_clicked = tk.StringVar(self)

        self.ranks_card_options = cards
        self.ranks_card_clicked = tk.StringVar()
        self.ranks_card_button_enabled = 0

        self.and_or_options = ["and ", "or "]

        self.filter_field_text = tk.StringVar(self)
        self.show_weights_clicked = tk.BooleanVar(self)

        self.flop_list_field = None
        self.filter_field = None
        self.flops_number = tk.IntVar(self)

        self.flopper = Flopper()

        self.create_widgets()
        self.print_flops()

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

        and_or_dropdown = ttk.OptionMenu(logical_frame, self.logical_operator_clicked, "and ", *self.and_or_options)
        and_or_dropdown.grid(column=1, row=2, padx=10, pady=2, columnspan=2)

        negation_label = tk.Label(logical_frame, text="Click to negate the filter", font=12)
        negation_label.grid(column=1, row=3, columnspan=2)

        negation_box = ttk.Checkbutton(logical_frame, text="NOT", variable=self.filter_negation_clicked
                                       , onvalue="not ", offvalue="")
        negation_box.grid(column=1, row=4, columnspan=2)

        add_filter_button = ttk.Button(self, text="ADD FILTER", command=self.add_filter)
        add_filter_button.grid(column=1, row=3, pady=5)

        self.filter_field = tk.Text(self, width=20, height=10, wrap=tk.WORD)
        self.filter_field.grid(column=1, row=4)

        clear_filter_button = ttk.Button(self, text="Clear filters", command=self.clear_filter)
        clear_filter_button.grid(column=1, row=5, pady=5)

        get_flops_button = tk.Button(self, text="GET FLOP LIST", command=self.print_flops, bg='light green')
        get_flops_button.grid(column=1, row=6, pady=5)

        flop_list_frame = tk.Frame(self)
        flop_list_frame.config(borderwidth=1, relief="sunken")
        flop_list_frame.grid(column=2, row=1, pady=10, padx=10, rowspan=5)

        weights_box = ttk.Checkbutton(flop_list_frame, text="Show weights", variable=self.show_weights_clicked
                                      , onvalue=True, offvalue=False)
        weights_box.grid(column=1, row=5, columnspan=2)
        self.show_weights_clicked.set(True)

        flop_list_label = tk.Label(flop_list_frame, text="Filtered canonical flop list ", font=12)
        flop_list_label.grid(column=2, row=0, columnspan=1)

        self.flop_list_field = ScrolledText(flop_list_frame, width=20, height=20)
        self.flop_list_field.grid(column=2, row=1, padx=2, rowspan=4)

        flop_list_buttons_frame = tk.Frame(self)
        flop_list_buttons_frame.config(borderwidth=1, relief="sunken")
        flop_list_buttons_frame.grid(column=2, row=6, pady=10, padx=10, rowspan=1)

        flop_number_label = tk.Label(flop_list_frame, textvariable=self.flops_number)
        flop_number_label.grid(column=2, row=6, sticky=tk.EW)

        clear_flops_button = tk.Button(flop_list_buttons_frame, text="CLEAR", command=self.clear_flops_field)
        clear_flops_button.grid(column=1, row=1, sticky=tk.W)

        clip_flops_button = tk.Button(flop_list_buttons_frame, text="COPY", command=self.copy_flops_field)
        clip_flops_button.grid(column=2, row=1, sticky=tk.W)

    def add_filter(self):
        if "card" not in self.texture_clicked.get():
            if len(self.filter_field.get('0.0', 'end')) < 2:
                self.filter_field.insert('end', self.filter_negation_clicked.get() + self.texture_clicked.get())
            else:
                self.filter_field.insert('end', "\n" + self.logical_operator_clicked.get()
                                         + self.filter_negation_clicked.get() + self.texture_clicked.get())
        else:
            if len(self.filter_field.get('0.0', 'end')) < 2:
                self.filter_field.insert('end', self.filter_negation_clicked.get() + self.texture_clicked.get()
                                         + " " + self.ranks_card_clicked.get())
            else:
                self.filter_field.insert('end', "\n" + self.logical_operator_clicked.get()
                                         + self.filter_negation_clicked.get() + self.texture_clicked.get()
                                         + " " + self.ranks_card_clicked.get())

    def clear_filter(self):
        self.filter_field.delete('0.0', 'end')

    @staticmethod
    def _parse_filters_string_to_methods(filters: str) -> str:
        filter_functions_list = []
        for element in filters.splitlines():
            for label in texture_labels:
                if label in element:
                    element = element.replace(label, filter_dict[label])
                    for card in cards:
                        if card in element[-1]:
                            element = element[:-2] + element[-1] + "')"
            filter_functions_list.append(element)
        return " ".join(filter_functions_list)

    def get_methods(self):
        return self._parse_filters_string_to_methods(self.filter_field.get('0.0', 'end'))

    def get_flops(self):

        def conditions(flop: str) -> bool:
            if len(self.filter_field.get("0.0", "end")) == 1:
                return True
            else:
                return eval(self.get_methods())

        flops = self.flopper.get_flops(cond_check=conditions)
        return flops

    def print_flops(self):
        self.flop_list_field.delete("0.0", "end")
        if self.show_weights_clicked.get():
            for element in self.get_flops():
                self.flop_list_field.insert("end", element + "\n")
        else:
            for element in self.get_flops():
                self.flop_list_field.insert("end", element[:6] + "\n")
        self.flops_number.set(len(self.get_flops()))

    def clear_flops_field(self):
        self.flop_list_field.delete("0.0", "end")

    def copy_flops_field(self):
        self.clipboard_clear()
        self.clipboard_append(self.flop_list_field.get("0.0", "end"))


gui = FlopperGui()

gui.mainloop()
