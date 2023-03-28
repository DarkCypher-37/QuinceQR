import os
import tkinter as tk
from tkinter import ttk
from tkinter.scrolledtext import ScrolledText
from PIL import Image, ImageTk
from tkinter import font

import QuinceQr as QR

# from dataclasses import dataclass
# @dataclass
# class Colors:
#     background: str = "#6d6d6d"
#     text: str = "#c8c8c8"
#     blue1: str = "#5686c5"  # Blueish accent color
#     grey1: str = "#868686"
#     grey2: str = "#a2a2a2"
#     button_color: str = "#4d4d4d"
#     button_text_color: str = "#f2f2f2"
#     selected_color: str = "#3d3d3d"
#     mouse_highlighter: str = "#ffb347"  # Bright orange


DEFAULT_QR_TEXT = "QR-Code text here ..."
DEFAULT_SAVE_FILEPATH_TEXT = "Filepath here ..."
DEFAULT_LOGO_FILEPATH_TEXT = "Filepath here ..."
SHIFT_MODIFIER = 0x1
CONTROL_MODIFIER = 0x4

ecl_map = {
    "7% (L)" : QR.ErrorCorrectionLevel.L,
    "15% (M)" : QR.ErrorCorrectionLevel.M,
    "25% (Q)" : QR.ErrorCorrectionLevel.Q,
    "30% (H)" : QR.ErrorCorrectionLevel.H
}

class Window(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("QuinceQR GarbageGUI")
        self.configure(background="#e2e2e2")

        # Create a text input field
        self.text_input = ScrolledText(self, width=70, height=5, foreground='grey')
        # self.text_input.vbar.config(background="#FF0000", troughcolor="#FF0000")
        # self.text_input.vbar.configure(troughcolor = 'red', bg = 'blue')
        self.text_input.grid(column=0, row=0, padx=10, pady=10, columnspan=3)
        self.text_input.insert('1.0', DEFAULT_QR_TEXT)

        self.text_input.bind("<FocusIn>", self.qr_text_handle_focus_in)
        self.text_input.bind("<FocusOut>", self.qr_text_handle_focus_out)
        self.text_input.bind("<Control-Return>", self.general_handle_enter)


        # Dropdown: Error correction
        self.error_correction_label = ttk.Label(self, text="Error Correction:")
        self.error_correction_label.grid(column=0, row=1, padx=10, pady=10, sticky=tk.W)

        self.error_correction_box = ttk.Combobox(self, state= "readonly")
        self.error_correction_box['values'] = ("7% (L)", "15% (M)", "25% (Q)", "30% (H)")
        self.error_correction_box.current(0)
        self.error_correction_box.grid(column=1, row=1, padx=10, pady=10, sticky=tk.W)
        self.error_correction_box.bind("<Return>", self.general_handle_enter)

        # Dropdown: Version
        self.version_label = ttk.Label(self, text="Version:")
        self.version_label.grid(column=0, row=2, padx=10, pady=10, sticky=tk.W)

        self.version_box = ttk.Combobox(self, state= "readonly")
        self.version_box['values'] = ["Auto"] + [f"{i}" for i in range(1, 41)]
        self.version_box.current(0)
        self.version_box.grid(column=1, row=2, padx=10, pady=10, sticky=tk.W)
        self.version_box.bind("<Return>", self.general_handle_enter)

        # Dropdown: Mask Pattern
        self.mask_pattern_label = ttk.Label(self, text="Mask Pattern:")
        self.mask_pattern_label.grid(column=0, row=3, padx=10, pady=10, sticky=tk.W)

        self.mask_pattern_box = ttk.Combobox(self, state= "readonly")
        self.mask_pattern_box['values'] = ["Auto"] + [f"{i}" for i in range(0, 8)]
        self.mask_pattern_box.current(0)
        self.mask_pattern_box.grid(column=1, row=3, padx=10, pady=10, sticky=tk.W)
        self.mask_pattern_box.bind("<Return>", self.general_handle_enter)


        # Button: generate
        self.generate_button = tk.Button(self, text="Generate Qr-Code!", command=self.make_qr, background="#5686c5", activebackground="#1676b5")
        self.generate_button.grid(column=2, row=1, padx=10, pady=10, sticky=tk.W)
        self.generate_button.bind("<Return>", self.button_handle_enter)

        # Button: save
        self.save_button = tk.Button(self, text="save", command=self.save)
        self.save_button.grid(column=2, row=2, padx=10, pady=10, sticky=tk.W)
        self.save_button.bind("<Return>", self.button_handle_enter)

        # Entry: save filepath
        self.save_filepath_input = ttk.Entry(self, width=40, foreground='grey')
        self.save_filepath_input.grid(column=2, row=3, padx=10, pady=10, sticky=tk.W)
        self.save_filepath_input.insert(0, DEFAULT_SAVE_FILEPATH_TEXT)

        self.save_filepath_input.bind("<FocusIn>", self.fp_text_handle_focus_in)
        self.save_filepath_input.bind("<FocusOut>", self.fp_text_handle_focus_out)
        self.save_filepath_input.bind("<Return>", self.general_handle_enter)


        # Logo
        self.current_text_label = ttk.Label(self, text="Logo:")
        self.current_text_label.grid(column=0, row=4, padx=10, pady=10, sticky=tk.W)
        
        logo_img = Image.open("QuinceQr/placeholder_logo.png")
        self.logo_orig_image = logo_img
        logo_img = logo_img.resize((50, 50))
        logo_photo = ImageTk.PhotoImage(logo_img)
        self.logo_image_label = ttk.Label(self, image=logo_photo)

        self.logo_photo = logo_photo  # Keep a reference to the image to prevent it from being garbage collected
        self.logo_image_label.grid(column=2, row=4, padx=10, pady=10, sticky=tk.W)
        self.logo_filepath_input = ttk.Entry(self, width=40, foreground='grey')

        self.logo_filepath_input.grid(column=1, row=4, padx=10, pady=10, sticky=tk.W)
        self.logo_filepath_input.insert(0, DEFAULT_LOGO_FILEPATH_TEXT)

        self.logo_filepath_input.bind("<FocusIn>", self.logo_text_handle_focus_in)
        self.logo_filepath_input.bind("<FocusOut>", self.logo_text_handle_focus_out)
        self.logo_filepath_input.bind("<Return>", self.logo_handle_enter)

        self.apply_logo_button_state = tk.BooleanVar(value=False)
        self.apply_logo_button = ttk.Checkbutton(self, text="Apply Logo", variable=self.apply_logo_button_state)
        self.apply_logo_button.grid(column=2, row=4, padx=10, pady=10, sticky=tk.E)

        # Display the QR-Code
        image = Image.open("QuinceQr/BackgroundCode.png")
        photo = ImageTk.PhotoImage(image)
        self.image_label = ttk.Label(self, image=photo)
        self.image = image
        self.photo = photo  # Keep a reference to the image to prevent it from being garbage collected
        self.image_label.grid(column=3, row=0, padx=10, pady=10, columnspan=3, rowspan=7)


        # display the current Qr-Code text/info
        self.current_text_label = ttk.Label(self, text="Current Qr-Code:", font=font.Font(family="Helvetica", size=18), background="#e2e2e2")
        self.current_text_label.grid(column=0, row=5, padx=10, pady=10, columnspan=1, sticky=tk.NSEW)

        self.current_info_label = ttk.Label(self, text=f"Version: N/A\nMask: N/A", font=font.Font(family="Helvetica", size=10), background="#e2e2e2")
        self.current_info_label.grid(column=2, row=5, padx=10, pady=10, columnspan=1, sticky=tk.E)

        self.current_text = tk.Text(self, height=10, font=font.Font(family="Helvetica", size=12), background="#c8c8c8", borderwidth=1, foreground="#3d3d3d")
        self.current_text.insert("1.0", DEFAULT_QR_TEXT)
        self.current_text.configure(state="disabled")
        self.current_text.grid(column=0, row=6, padx=10, pady=10, columnspan=3)

    def get_qr_text(self):
        return self.text_input.get('1.0', tk.END).strip()

    def get_ecl(self):
        ecl = self.error_correction_box.get()
        return ecl_map[ecl]

    def get_mask(self):
        mask = self.mask_pattern_box.get()
        if mask == "Auto":
            return None
        return int(mask)
    
    def get_version(self):
        version = self.version_box.get()
        if version == "Auto":
            return None
        return int(version)

    def make_qr(self):
        text = self.get_qr_text()
        mask = self.get_mask()
        version = self.get_version()

        if mask is None and version is None:
            qr = QR.QrCode(text, self.get_ecl())
            mask = "N/A"
        elif mask is None and version is not None:
            qr = QR.QrCode(text, self.get_ecl(), version=version)
            mask = "N/A"
        elif mask is not None and version is None:
            qr = QR.QrCode(text, self.get_ecl(), force_mask=mask)
        else:
            qr = QR.QrCode(text, self.get_ecl(), version=version, force_mask=mask)

        img = qr.make_image(600)

        if self.apply_logo_button_state.get():
            print("apply LOGO here!") # TODO
            img.paste(self.logo_orig_image, (300, 300))

        version = qr.version # get the actually used version
        self.change_qr_image(img)
        self.update_current_text(text)
        self.update_current_info(version, mask)

    def change_qr_image(self, img: Image):
        photo = ImageTk.PhotoImage(img)
        self.image_label.configure(image=photo)
        self.image = img
        self.photo = photo  # Keep a reference to the image to prevent it from being garbage collected

    def update_current_text(self, text):
        self.current_text.configure(state="normal")
        self.current_text.delete("1.0", tk.END)
        self.current_text.insert("1.0", text)
        self.current_text.configure(state="disabled")

    def update_current_info(self, version, mask):
        self.current_info_label.config(text=f"Version: {version}\nMask: {mask}")

    def save(self):
        filepath = self.save_filepath_input.get()

        def is_just_dir(filepath):
            return os.path.basename(filepath) == ""
        
        def is_valid_parent_dir(filepath):
            parent_dir = os.path.dirname(filepath)
            return os.path.isdir(parent_dir)
        
        def does_file_already_exist(filepath):
            return os.path.isfile(filepath)

        if is_just_dir(filepath):
            print("Error: You only entered a directory!!") # TODO: display in GUI
        if is_valid_parent_dir(filepath):
            if does_file_already_exist(filepath):
                print("Warn: file already exists")
            
            print(f"saving to: {filepath=!r}")
            # file_extension = os.path.splitext(filepath)[1]

            self.image.save(filepath)


    def qr_text_handle_focus_in(self, event):
        widget = event.widget
        if widget.get('1.0', tk.END).strip() == DEFAULT_QR_TEXT:
            widget.delete('1.0', tk.END)
            widget.config(foreground="black")

    def qr_text_handle_focus_out(self, event):
        widget = event.widget
        if widget.get('1.0', tk.END).strip() == "":
            widget.config(foreground="grey")
            widget.insert('1.0', DEFAULT_QR_TEXT)

    def fp_text_handle_focus_in(self, event):
        widget = event.widget
        if widget.get().strip() == DEFAULT_SAVE_FILEPATH_TEXT:
            widget.delete(0, tk.END)
            widget.config(foreground="black")

    def fp_text_handle_focus_out(self, event):
        widget = event.widget
        if widget.get().strip() == "":
            widget.config(foreground="grey")
            widget.insert(0, DEFAULT_SAVE_FILEPATH_TEXT)

    def logo_text_handle_focus_in(self, event):
        widget = event.widget
        if widget.get().strip() == DEFAULT_LOGO_FILEPATH_TEXT:
            widget.delete(0, tk.END)
            widget.config(foreground="black")

    def logo_text_handle_focus_out(self, event):
        widget = event.widget
        if widget.get().strip() == "":
            widget.config(foreground="grey")
            widget.insert(0, DEFAULT_LOGO_FILEPATH_TEXT)

    def logo_handle_enter(self, event):
        filepath = event.widget.get()
        img = Image.open(filepath)
        self.logo_orig_image = img
        img = img.resize((50, 50))
        
        photo = ImageTk.PhotoImage(img)
        self.logo_image_label.configure(image=photo)
        self.logo_photo = photo # Keep a reference to the image to prevent it from being garbage collected


    def button_handle_enter(self, event):
        widget = event.widget
        widget.invoke()

    def focus_next_widget(self, widget):
        widget.tk_focusNext().focus()

    def general_handle_enter(self, event):
        self.focus_next_widget(event.widget)


def main():
    app = Window()
    app.mainloop()


if __name__ == "__main__":
    main()