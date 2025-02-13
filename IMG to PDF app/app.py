import tkinter as tk
from tkinter import filedialog, messagebox
from fpdf import FPDF
import os

class ImageToPDFConverter:
    def __init__(self, root):
        self.root = root
        self.image_paths = []
        self.output_pdf_name = tk.StringVar()
        self.selected_images_listbox = tk.Listbox(root, selectmode=tk.MULTIPLE)

        self.initialize_ui()

    def initialize_ui(self):
        title_label = tk.Label(self.root, text="Convertor", font=("Helvetica", 16, "bold"))
        title_label.pack(pady=10)

        select_images_bottom = tk.Button(self.root, text="Select Images", command=self.select_images)
        select_images_bottom.pack(pady=(0, 10))

        self.selected_images_listbox.pack(pady=(0, 10), fill=tk.BOTH, expand=True)

        label = tk.Label(self.root, text="Enter the converted PDF name:")
        label.pack()

        pdf_name_entry = tk.Entry(self.root, textvariable=self.output_pdf_name, width=40, justify='center')
        pdf_name_entry.pack()

        convert_button = tk.Button(self.root, text="Convert to PDF", command=self.convert_images_to_pdf)
        convert_button.pack(pady=(20, 40))

    def select_images(self):
        self.image_paths = filedialog.askopenfilenames(
            title="Select Images",
            filetypes=[("Image files", "*.png;*.jpg;*.jpeg")]
        )
        self.update_selected_images_listbox()

    def update_selected_images_listbox(self):
        self.selected_images_listbox.delete(0, tk.END)
        for image_path in self.image_paths:
            _, image_name = os.path.split(image_path)
            self.selected_images_listbox.insert(tk.END, image_name)

    def convert_images_to_pdf(self):
        if not self.image_paths:
            messagebox.showwarning("No Images", "Please select at least one image.")
            return

        output_pdf_path = self.output_pdf_name.get() + ".pdf" if self.output_pdf_name.get() else "output.pdf"

        try:
            # Create a PDF using fpdf
            pdf = FPDF()
            for image_path in self.image_paths:
                pdf.add_page()
                pdf.image(image_path, x=10, y=10, w=190)  # Adjust dimensions as needed
            pdf.output(output_pdf_path)
            messagebox.showinfo("Success", f"PDF saved as {output_pdf_path}")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to convert images to PDF: {e}")


def main():
    root = tk.Tk()
    root.title("Convert any IMG to PDF")
    converter = ImageToPDFConverter(root)
    root.geometry("400x600")
    root.mainloop()


if __name__ == "__main__":
    main()