from tkinter.scrolledtext import ScrolledText
import tkinter as tk
from tkinter import ttk
from holdem_flopper.common import conditions
from holdem_flopper.common.basics import ranks
from holdem_flopper.common.tools import FlopFilter, WeightAdder

labels_functions = {"rainbow": conditions.is_rainbow,
                    "two tone": conditions.is_two_tone,
                    "monotone": conditions.is_mono,
                    "straight possible": conditions.is_straight_possible,
                    "straight draw possible": conditions.is_straight_draw_possible,
                    "paired": conditions.is_paired,
                    "tripsed": conditions.is_tripsed,
                    "has rank": conditions.has_rank,
                    "max bound rank is": conditions.is_not_higher_than,
                    "min bound rank is": conditions.is_not_lower_than,
                    "paired rank is": conditions.has_paired_rank}


class FlopperGui(tk.Tk):

    def __init__(self):

        super().__init__()

        self.title("Holdem Flopper")
        self.geometry("420x500")
        self.resizable(False, False)
        self.texture_options = tuple(x for x in labels_functions)
        self.texture_clicked = tk.StringVar(self)
        self.logical_operator_clicked = tk.StringVar(self)
        self.filter_negation_clicked = tk.BooleanVar(self)
        self.filter_negation_clicked.set(False)
        self.ranks_clicked = tk.StringVar()
        self.ranks_and_or_clicked = tk.StringVar(self)
        self.ranks_card_options = ranks
        self.ranks_card_clicked = tk.StringVar()
        self.ranks_card_button_enabled = 0
        self.and_or_options = ["and", "or"]
        self.show_weights_clicked = tk.BooleanVar(self)
        self.flops_number = tk.IntVar(self)

        # Flop texture selection frame
        self.texture_frame = tk.Frame(self)
        self.texture_frame.config(width=26, borderwidth=1, relief='sunken')
        self.texture_frame.grid(column=1, row=1, pady=10, sticky=tk.EW)
        self.texture_frame.columnconfigure(0, weight=3)
        self.texture_frame.columnconfigure(1, weight=1)
        self.texture_label = tk.Label(self.texture_frame, text="Flop texture filter", font=12)
        self.texture_label.grid(column=0, row=0, columnspan=2)
        self.texture_dropdown = ttk.OptionMenu(self.texture_frame,
                                               self.texture_clicked,
                                               "monotone",
                                               *self.texture_options)
        self.texture_dropdown.grid(column=0, row=1, pady=2)
        self.ranks_card_dropdown = ttk.OptionMenu(self.texture_frame,
                                                  self.ranks_card_clicked,
                                                  "A",
                                                  *self.ranks_card_options)
        self.ranks_card_dropdown.config(state="disabled")
        self.ranks_card_dropdown.grid(column=1, row=1, pady=2)
        self.texture_clicked.trace("w", self.disable_rank_selection)

        # Logical operator selection frame
        self.logical_frame = tk.Frame(self)
        self.logical_frame.grid(column=1, row=2, pady=10, sticky=tk.EW)
        self.logical_frame.config(width=34, borderwidth=1, relief='sunken')
        self.logical_frame.columnconfigure(0, weight=3)
        self.logical_frame.columnconfigure(1, weight=1)
        self.logical_label = tk.Label(self.logical_frame,
                                      text="Logical operator",
                                      font=12)
        self.logical_label.grid(column=0, row=0, columnspan=2)
        self.and_or_dropdown = ttk.OptionMenu(self.logical_frame,
                                              self.logical_operator_clicked, "and",
                                              *self.and_or_options)
        self.and_or_dropdown.grid(column=0, row=1, padx=10, pady=2, columnspan=2)
        self.negation_label = tk.Label(self.logical_frame,
                                       text="Click to negate the filter", font=12)
        self.negation_label.grid(column=0, row=2, columnspan=2)
        self.negation_box = ttk.Checkbutton(self.logical_frame, text="NOT",
                                            variable=self.filter_negation_clicked,
                                            onvalue=True, offvalue=False)
        self.negation_box.grid(column=0, row=3, columnspan=2)

        # Filter prompts text field
        self.filter_field = tk.Text(self, width=26, height=10, wrap=tk.WORD)
        self.filter_field.config(state="disabled")
        self.filter_field.grid(column=1, row=4)

        # Flop list presentation frame
        self.flop_list_frame = tk.Frame(self)
        self.flop_list_frame.config(borderwidth=1, relief="sunken")
        self.flop_list_frame.grid(column=2, row=1, pady=10, padx=10, rowspan=5)
        self.weights_box = ttk.Checkbutton(self.flop_list_frame, text="Show weights",
                                           variable=self.show_weights_clicked,
                                           onvalue=True, offvalue=False)
        self.weights_box.grid(column=1, row=5, columnspan=2)
        self.show_weights_clicked.set(False)

        self.flop_list_label = tk.Label(self.flop_list_frame,
                                        text="Filtered canonical flop list ", font=12)
        self.flop_list_label.grid(column=2, row=0, columnspan=1)
        self.flop_list_field = ScrolledText(self.flop_list_frame, width=20, height=20)
        self.flop_list_field.grid(column=2, row=1, padx=2, rowspan=4)

        self.flop_list_buttons_frame = tk.Frame(self)
        self.flop_list_buttons_frame.config(borderwidth=1, relief="sunken")
        self.flop_list_buttons_frame.grid(column=2, row=6, pady=10, padx=10, rowspan=1)

        self.flop_number_label = tk.Label(self.flop_list_frame, textvariable=self.flops_number)
        self.flop_number_label.grid(column=2, row=6, sticky=tk.EW)

        # Buttons
        self.add_filter_button = ttk.Button(self, text="ADD FILTER",
                                            command=self.add_filter)
        self.add_filter_button.grid(column=1, row=3, pady=5)
        self.clear_filter_button = ttk.Button(self, text="Clear filters",
                                              command=self.clear_filter)
        self.clear_filter_button.grid(column=1, row=5, pady=5)
        self.clip_flops_button = tk.Button(self.flop_list_buttons_frame,
                                           text="COPY", command=self.copy_flops_field)
        self.clip_flops_button.grid(column=2, row=1, sticky=tk.W)

        self.flop_filter = FlopFilter()
        self.print_flops()

    def disable_rank_selection(self, var, index, mode):
        if "rank" in self.texture_clicked.get():
            self.ranks_card_dropdown.config(state="normal")
        else:
            self.ranks_card_dropdown.config(state="disabled")

    def add_filter(self):  # todo
        self.filter_field.config(state="normal")
        selected_filter = self.texture_clicked.get()
        selected_operator = self.logical_operator_clicked.get()
        selected_negator = self.filter_negation_clicked.get()
        rank_enabled = str(self.ranks_card_dropdown.cget("state")) == "normal"
        selected_figure = self.ranks_card_clicked.get() if rank_enabled else ""
        function_match = labels_functions[selected_filter]

        not_empty = (len(self.filter_field.get("1.0", "end").strip()) != 0)

        filter_prompt = f'{int(not_empty) * (selected_operator + " ")}' \
                        f'{int(selected_negator) * "not "}' \
                        f'{selected_filter} {selected_figure}\n'

        self.filter_field.insert("end", filter_prompt)
        self.filter_field.config(state="disabled")
        self.flop_filter.add_filter(function_match,
                                    selected_figure,
                                    selected_negator,
                                    selected_operator)
        self.print_flops()

    def clear_filter(self):
        self.filter_field.config(state="normal")
        self.filter_field.delete('1.0', 'end')
        self.filter_field.config(state="disabled")
        del self.flop_filter
        self.flop_filter = FlopFilter()
        self.print_flops()

    def print_flops(self):
        self.flop_list_field.delete("1.0", "end")
        flop_list = self.flop_filter.get_flops()
        if self.show_weights_clicked.get():
            flop_list = WeightAdder(flop_list).get_flops_with_weights()
        self.flops_number.set(len(flop_list))
        for flop in flop_list:
            self.flop_list_field.insert("end", flop + "\n")

    def clear_flops_field(self):
        self.flop_list_field.delete("1.0", "end")

    def copy_flops_field(self):
        self.clipboard_clear()
        self.clipboard_append(self.flop_list_field.get("1.0", "end"))


gui = FlopperGui()

if __name__ == '__main__':
    gui.mainloop()
