import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk, UnidentifiedImageError, ImageFont, ImageDraw


class Watermarker(tk.Tk):
    def __init__(self):
        super().__init__()
        self.minsize(620, 540)
        self.img = None
        self.desired_text = None
        self.popup = None
        self.red = None
        self.blue = None
        self.green = None
        self.opacity = None
        self.colour_label = None
        self.watermark_img = None
        self.filename = None
        self.initial_width = 0
        self.initial_height = 0
        self.title('Water-Marker')
        self.upload_button = tk.Button(text='Upload Image', command=self.upload_image, width=20)
        self.upload_button.grid(column=0, row=2)
        self.chosen_option = tk.StringVar(self)
        self.chosen_option.set('Choose an Option')
        options = ['Text Watermark', 'Picture Watermark', 'Corner Text']
        self.watermark_option = tk.OptionMenu(
            self,
            self.chosen_option,
            *options,
            command=self.open_popup
        )
        self.watermark_option.grid(column=1, row=2)
        self.canvas = tk.Canvas(self, width=612, height=473)
        self.canvas.grid(column=0, row=1, columnspan=3)
        self.image = ImageTk.PhotoImage(image=Image.open('placeholder.jpeg'))
        self.image_container = self.canvas.create_image(0, 0, anchor='nw', image=self.image)
        self.reset_button = tk.Button(text='Reset', comman=self.reset, width=20)
        self.reset_button.grid(column=0, row=3)
        self.save_button = tk.Button(text='Save', command=self.save, width=20)
        self.save_button.grid(column=1, row=3)

        self.mainloop()

    def upload_image(self):
        self.filename = filedialog.askopenfilename()
        try:
            self.img = Image.open(self.filename)
        except UnidentifiedImageError:
            messagebox.showerror('Unsupported File', 'This File type is not supported, please select an image.')
        else:
            self.initial_width = self.img.width
            self.initial_height = self.img.height
            self.img = self.img.resize((612, 473))
            self.image = ImageTk.PhotoImage(self.img)

        self.canvas.itemconfig(self.image_container, image=self.image)

    def add_text_watermark(self):
        input_text = self.desired_text.get()
        font_size = 36
        self.img = self.img.convert('RGBA')
        self.img = self.img.resize((self.initial_width, self.initial_height))
        txt = Image.new('RGBA', self.img.size, (255, 255, 255, 0))
        draw = ImageDraw.Draw(txt)
        font = ImageFont.truetype("Arial Bold.ttf", font_size)
        font_rows = round(self.initial_height / font_size) + 1
        font_columns = round(self.initial_width / (font_size * len(input_text))) + 1
        red = int(self.red.get())
        green = int(self.green.get())
        blue = int(self.blue.get())
        opacity = int(self.opacity.get())
        for y_cor in range(font_rows):
            for x_cor in range(font_columns):
                draw.text((x_cor * len(input_text) * font_size,
                           y_cor * (font_size * (4/3))),
                          input_text,
                          fill=(red, green, blue, opacity),
                          font=font)
        self.img = Image.alpha_composite(self.img, txt)
        self.popup.destroy()

        self.img = self.img.resize((612, 473))
        self.image = ImageTk.PhotoImage(self.img)
        self.canvas.itemconfig(self.image_container, image=self.image)

    def add_corner_watermark(self):
        input_text = self.desired_text.get()
        font_size = 36
        self.img = self.img.convert('RGBA')
        self.img = self.img.resize((self.initial_width, self.initial_height))
        txt = Image.new('RGBA', self.img.size, (255, 255, 255, 0))
        draw = ImageDraw.Draw(txt)
        font = ImageFont.truetype("Arial Bold.ttf", font_size)
        red = int(self.red.get())
        green = int(self.green.get())
        blue = int(self.blue.get())
        opacity = int(self.opacity.get())
        draw.text((20, self.initial_height - font_size),
                  input_text,
                  fill=(red, green, blue, opacity),
                  font=font)
        self.img = Image.alpha_composite(self.img, txt)
        self.popup.destroy()

        self.img = self.img.resize((612, 473))
        self.image = ImageTk.PhotoImage(self.img)
        self.canvas.itemconfig(self.image_container, image=self.image)

    def get_colour(self, var):
        red = int(self.red.get())
        green = int(self.green.get())
        blue = int(self.blue.get())
        colour = f'#{red:02x}{green:02x}{blue:02x}'
        self.colour_label.config(bg=colour)

    def upload_watermark(self):
        watermark_filename = filedialog.askopenfilename()
        try:
            self.watermark_img = Image.open(watermark_filename)
        except UnidentifiedImageError:
            messagebox.showerror('Unsupported File', 'This File type is not supported, please select an image.')

    def add_image_watermark(self):
        opacity = int(self.opacity.get())
        self.watermark_img.putalpha(opacity)
        self.watermark_img = self.watermark_img.resize((self.initial_width, self.initial_height))
        self.img = self.img.resize((self.initial_width, self.initial_height))

        self.img.paste(self.watermark_img, (0, 0), self.watermark_img)

        self.img = self.img.resize((612, 473))
        self.image = ImageTk.PhotoImage(self.img)
        self.canvas.itemconfig(self.image_container, image=self.image)
        self.popup.destroy()

    def open_popup(self, chosen_option):
        if chosen_option == 'Text Watermark':
            if self.img is None:
                messagebox.showerror('Select an Image', 'You need to select an Image before choosing a watermark.')
                self.chosen_option.set('Choose an Option')
            else:
                self.popup = tk.Toplevel(self)
                self.popup.title('Add Text Watermark')
                self.popup.minsize(300, 200)
                text_label = tk.Label(self.popup, text='Text')
                text_label.grid(column=0, row=0)
                self.desired_text = tk.Entry(self.popup)
                self.desired_text.grid(column=1, row=0)

                self.red = tk.Scale(self.popup, label='Red:', from_=0, to=255,
                                    command=self.get_colour, orient=tk.HORIZONTAL)
                self.red.grid(column=0, row=1)

                self.green = tk.Scale(self.popup, label='Green:', from_=0, to=255,
                                      command=self.get_colour, orient=tk.HORIZONTAL)
                self.green.grid(column=1, row=1)

                self.blue = tk.Scale(self.popup, label='Blue:', from_=0, to=255,
                                     command=self.get_colour, orient=tk.HORIZONTAL)
                self.blue.grid(column=0, row=2)

                self.opacity = tk.Scale(self.popup, label='Opacity:', from_=0, to=255,
                                        command=self.get_colour, orient=tk.HORIZONTAL)
                self.opacity.grid(column=1, row=2)

                tk.Label(self.popup, text='Colour').grid(column=0, row=5)
                self.colour_label = tk.Label(self.popup, width=20, bg=f'#{0:02x}{0:02x}{0:02x}')
                self.colour_label.grid(column=1, row=5)

                add_watermark = tk.Button(self.popup, text='Add Watermark', command=self.add_text_watermark)
                add_watermark.grid(column=0, row=6, columnspan=2)

        elif chosen_option == 'Corner Text':
            if self.img is None:
                messagebox.showerror('Select an Image', 'You need to select an Image before choosing a watermark.')
                self.chosen_option.set('Choose an Option')
            else:
                self.popup = tk.Toplevel(self)
                self.popup.minsize(300, 200)
                text_label = tk.Label(self.popup, text='Text:')
                text_label.grid(column=0, row=0)
                self.desired_text = tk.Entry(self.popup)
                self.desired_text.grid(column=1, row=0)

                self.red = tk.Scale(self.popup, label='Red:', from_=0, to=255,
                                    command=self.get_colour, orient=tk.HORIZONTAL)
                self.red.grid(column=0, row=1)

                self.green = tk.Scale(self.popup, label='Green:', from_=0, to=255,
                                      command=self.get_colour, orient=tk.HORIZONTAL)
                self.green.grid(column=1, row=1)

                self.blue = tk.Scale(self.popup, label='Blue:', from_=0, to=255,
                                     command=self.get_colour, orient=tk.HORIZONTAL)
                self.blue.grid(column=0, row=2)

                self.opacity = tk.Scale(self.popup, label='Opacity:', from_=0, to=255,
                                        command=self.get_colour, orient=tk.HORIZONTAL)
                self.opacity.grid(column=1, row=2)

                tk.Label(self.popup, text='Colour').grid(column=0, row=5)
                self.colour_label = tk.Label(self.popup, width=20, bg=f'#{0:02x}{0:02x}{0:02x}')
                self.colour_label.grid(column=1, row=5)

                add_watermark = tk.Button(self.popup, text='Add Watermark', command=self.add_corner_watermark)
                add_watermark.grid(column=0, row=6, columnspan=2)

        elif chosen_option == 'Picture Watermark':
            if self.img is None:
                messagebox.showerror('Select an Image', 'You need to select an Image before choosing a watermark.')
                self.chosen_option.set('Choose an Option')
            else:
                self.popup = tk.Toplevel(self)
                self.popup.minsize(300, 200)
                tk.Button(self.popup, text='Upload Watermark Image',
                          command=self.upload_watermark).grid(column=0, row=0, columnspan=2)
                self.opacity = tk.Scale(self.popup, label='Opacity:', from_=0, to=255,
                                        command='', orient=tk.HORIZONTAL)
                self.opacity.grid(column=0, row=1, columnspan=2)

                add_watermark = tk.Button(self.popup, text='Add Watermark', command=self.add_image_watermark)
                add_watermark.grid(column=0, row=2, columnspan=2)

    def reset(self):
        self.image = ImageTk.PhotoImage(image=Image.open('placeholder.jpeg'))
        self.img = None
        self.initial_width = 0
        self.initial_height = 0
        self.canvas.itemconfig(self.image_container, image=self.image)

    def save(self):
        self.img = self.img.resize((self.initial_width, self.initial_height))
        file = self.filename.split('/')
        new_file = 'Watermarked-' + file[-1]
        file[-1] = new_file
        file = '/'.join(file)
        self.img = self.img.save(file)
        messagebox.showinfo(title='Image Saved', message=f'Image saved to:\n{file}')
        self.reset()


