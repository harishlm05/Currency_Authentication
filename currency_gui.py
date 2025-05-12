import os
import tkinter as tk
from tkinter import messagebox, filedialog, ttk

import cv2
from PIL import Image, ImageTk
from currency_detector import CurrencyDetector


class CurrencyApp:
    def __init__(self, master):
        self.master = master
        master.title(" Currency Note Authentication")
        master.geometry("1000x700")
        master.configure(bg='#f0f0f0')

        self.center_window()
        self.configure_styles()
        self.create_widgets()
        self.detector = CurrencyDetector()
        self.current_image = None

    def center_window(self):
        self.master.update_idletasks()
        width = self.master.winfo_width()
        height = self.master.winfo_height()
        x = (self.master.winfo_screenwidth() // 2) - (width // 2)
        y = (self.master.winfo_screenheight() // 2) - (height // 2)
        self.master.geometry(f'{width}x{height}+{x}+{y}')

    def configure_styles(self):
        self.style = ttk.Style()
        self.style.configure('TFrame', background='#f0f0f0')
        self.style.configure('TLabel', background='#f0f0f0', font=('Helvetica', 12))
        self.style.configure('Title.TLabel', font=('Helvetica', 18, 'bold'))
        self.style.configure('TButton', font=('Helvetica', 12), padding=10)
        self.style.configure('Result.TLabel', font=('Helvetica', 14, 'bold'))

    def create_widgets(self):
        # Main container
        self.main_frame = ttk.Frame(self.master)
        self.main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

        # Title
        self.title_label = ttk.Label(
            self.main_frame,
            text=" Currency Note Authentication ",
            style='Title.TLabel'
        )
        self.title_label.pack(pady=(0, 20))

        # Image display frame
        self.image_frame = ttk.Frame(self.main_frame)
        self.image_frame.pack(fill=tk.BOTH, expand=True)

        # Input image panel
        self.create_input_panel()

        # Result image panel
        self.create_result_panel()

        # Control buttons
        self.create_control_buttons()

        # Result display
        self.create_result_display()

        # Status bar
        self.create_status_bar()

    def create_input_panel(self):
        self.input_frame = ttk.Frame(self.image_frame)
        self.input_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=10, pady=10)

        self.input_label = ttk.Label(self.input_frame, text="Input Currency Note", style='TLabel')
        self.input_label.pack()

        self.input_canvas = tk.Canvas(
            self.input_frame,
            width=400,
            height=400,
            bg='white',
            highlightthickness=2,
            highlightbackground="#cccccc"
        )
        self.input_canvas.pack(fill=tk.BOTH, expand=True)

    def create_result_panel(self):
        self.result_frame = ttk.Frame(self.image_frame)
        self.result_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=10, pady=10)

        self.result_label = ttk.Label(self.result_frame, text="Feature Matches", style='TLabel')
        self.result_label.pack()

        self.result_canvas = tk.Canvas(
            self.result_frame,
            width=400,
            height=400,
            bg='white',
            highlightthickness=2,
            highlightbackground="#cccccc"
        )
        self.result_canvas.pack(fill=tk.BOTH, expand=True)

    def create_control_buttons(self):
        self.control_frame = ttk.Frame(self.main_frame)
        self.control_frame.pack(fill=tk.X, pady=(20, 10))

        self.load_button = ttk.Button(
            self.control_frame,
            text="Load Currency Image",
            command=self.load_image,
            style='TButton'
        )
        self.load_button.pack(side=tk.LEFT, padx=10)

        self.verify_button = ttk.Button(
            self.control_frame,
            text="Verify Currency",
            command=self.verify_currency,
            style='TButton'
        )
        self.verify_button.pack(side=tk.LEFT, padx=10)

    def create_result_display(self):
        self.result_display_frame = ttk.Frame(self.main_frame)
        self.result_display_frame.pack(fill=tk.BOTH, expand=True)

        self.result_text = tk.Text(
            self.result_display_frame,
            height=6,
            width=60,
            font=('Helvetica', 12),
            wrap=tk.WORD,
            padx=10,
            pady=10,
            highlightthickness=2,
            highlightbackground="#cccccc"
        )
        self.result_text.pack(fill=tk.BOTH, expand=True)
        self.result_text.insert(tk.END, "Results will appear here...")
        self.result_text.config(state=tk.DISABLED)

    def create_status_bar(self):
        self.status_var = tk.StringVar()
        self.status_var.set("Ready")
        self.status_bar = ttk.Label(
            self.main_frame,
            textvariable=self.status_var,
            relief=tk.SUNKEN,
            anchor=tk.W,
            font=('Helvetica', 10)
        )
        self.status_bar.pack(fill=tk.X, pady=(10, 0))

    def load_image(self):
        file_path = filedialog.askopenfilename(
            title="Select Currency Note Image",
            filetypes=[("Image files", "*.jpg *.jpeg *.png")]
        )

        if file_path:
            try:
                self.status_var.set(f"Loading image: {os.path.basename(file_path)}...")
                self.master.update()

                img = cv2.imread(file_path)
                if img is None:
                    messagebox.showerror("Error", "Could not read the image file")
                    return

                self.current_image = img
                self.display_image(img, self.input_canvas)
                self.status_var.set(f"Loaded: {os.path.basename(file_path)}")

                self.result_canvas.delete("all")
                self.result_text.config(state=tk.NORMAL)
                self.result_text.delete(1.0, tk.END)
                self.result_text.insert(tk.END, "Click 'Verify Currency' to check authenticity")
                self.result_text.config(state=tk.DISABLED)

            except Exception as e:
                messagebox.showerror("Error", f"Failed to load image: {str(e)}")
                self.status_var.set("Error loading image")

    def display_image(self, img, canvas):
        img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        pil_img = Image.fromarray(img_rgb)

        canvas_width = canvas.winfo_width()
        canvas_height = canvas.winfo_height()
        img_ratio = pil_img.width / pil_img.height
        canvas_ratio = canvas_width / canvas_height

        if img_ratio > canvas_ratio:
            new_width = canvas_width
            new_height = int(canvas_width / img_ratio)
        else:
            new_height = canvas_height
            new_width = int(canvas_height * img_ratio)

        pil_img = pil_img.resize((new_width, new_height), Image.LANCZOS)
        tk_img = ImageTk.PhotoImage(pil_img)

        canvas.delete("all")
        canvas.create_image(canvas_width // 2, canvas_height // 2, anchor=tk.CENTER, image=tk_img)
        canvas.image = tk_img

    def verify_currency(self):
        if self.current_image is None:
            messagebox.showwarning("Warning", "Please load an image first")
            return

        try:
            self.status_var.set("Processing image...")
            self.master.update()

            temp_path = "temp_currency.jpg"
            cv2.imwrite(temp_path, self.current_image)

            result = self.detector.verify_currency(temp_path)

            if isinstance(result, str):
                messagebox.showerror("Error", result)
                self.status_var.set("Verification failed")
                return

            status = "GENUINE" if result['is_genuine'] else "POSSIBLY FAKE"
            color = "green" if result['is_genuine'] else "red"

            result_text = f"Denomination: {result['denomination']}\n"
            result_text += f"Match Score: {result['match_score']}\n"
            result_text += f"Status: {status}\n"
            result_text += f"Threshold: 30"

            self.result_text.config(state=tk.NORMAL)
            self.result_text.delete(1.0, tk.END)
            self.result_text.insert(tk.END, result_text)
            self.result_text.tag_add("status", "3.7", f"3.{7 + len(status)}")
            self.result_text.tag_config("status", foreground=color)
            self.result_text.config(state=tk.DISABLED)

            if result['match_data']:
                match_data = result['match_data']
                img_matches = cv2.drawMatches(
                    match_data['test_img'], match_data['test_kp'],
                    match_data['ref_img'], match_data['ref_kp'],
                    match_data['matches'][:50], None, flags=2
                )
                img_matches = cv2.cvtColor(img_matches, cv2.COLOR_BGR2RGB)
                self.display_result_image(img_matches)

            self.status_var.set(f"Verification complete: {result['denomination']}")

        except Exception as e:
            messagebox.showerror("Error", f"Verification failed: {str(e)}")
            self.status_var.set("Verification error")
        finally:
            if os.path.exists(temp_path):
                os.remove(temp_path)

    def display_result_image(self, img):
        pil_img = Image.fromarray(img)
        canvas_width = self.result_canvas.winfo_width()
        canvas_height = self.result_canvas.winfo_height()
        img_ratio = pil_img.width / pil_img.height
        canvas_ratio = canvas_width / canvas_height

        if img_ratio > canvas_ratio:
            new_width = canvas_width
            new_height = int(canvas_width / img_ratio)
        else:
            new_height = canvas_height
            new_width = int(canvas_height * img_ratio)

        pil_img = pil_img.resize((new_width, new_height), Image.LANCZOS)
        tk_img = ImageTk.PhotoImage(pil_img)

        self.result_canvas.delete("all")
        self.result_canvas.create_image(canvas_width // 2, canvas_height // 2, anchor=tk.CENTER, image=tk_img)
        self.result_canvas.image = tk_img


if __name__ == "__main__":
    root = tk.Tk()
    app = CurrencyApp(root)
    root.mainloop()