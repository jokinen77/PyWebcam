from tkinter import *
from PIL import ImageTk, Image
import cv2
import time

class WebcamGUI:
    def __init__(self, cap_id=0, cap_width=1280, cap_height=720, cam=None, cam_width=1280, cam_height=720):
        #Param window
        self.root = Tk()
        self.root.minsize(240,240)
        self.root.title("Webcam")

        #Image frame
        self.image_frame = Frame(self.root, bg="white")
        self.image_frame.grid(columnspan=3)
        #Image label
        self.image_label = Label(self.image_frame)
        self.image_label.pack()

        #Misc params
        self.image_transformers = []
        self.slider_width = 200
        self.font=("Arial", 12)
        self.padx=10
        self.pady=10
        self.cap_id = cap_id
        self.cap_width = cap_width
        self.cap_height = cap_height
        self.cam = cam
        self.cam_width = cam_width
        self.cam_height = cam_height

    def create_parameter_slider(self, row, params, param_name, label, values=(0,100,1)):
        #Param label
        param_label = Label(self.root, text=label, padx=self.padx, pady=self.pady, font=self.font)
        param_label.grid(column=0, row=row)

        #Value label
        def update_value_label():
            if param_name in params:
                value_label = Label(self.root, text=f'{params[param_name]}', anchor=W, padx=self.padx, pady=self.pady, font=self.font)
                value_label.grid(column=2, row=row)
        update_value_label()

        #On slider change
        def change_param_value(x):
            params[param_name] = float(x)
            update_value_label()

        #Slider
        slider = Scale(self.root, from_=values[0], to=values[1], resolution=values[2], showvalue=0, orient=HORIZONTAL, length=self.slider_width, command=change_param_value)
        if param_name in params:
            slider.set(params[param_name])
        slider.grid(column=1, row=row)

    def create_parameter_checkbox(self, row, params, param_name, label):
        #Param label
        param_label = Label(self.root, text=label, padx=self.padx, pady=self.pady, font=self.font)
        param_label.grid(column=0, row=row)

        #On slider change
        var = BooleanVar()
        if param_name in params:
            var.set(value=params[param_name])
        var.set(value=params[param_name])
        def change_param_value():
            params[param_name] = var.get()
        
        #Slider
        button = Checkbutton(self.root, variable=var, onvalue=True, offvalue=False, command=change_param_value)
        button.grid(column=1, row=row)

    def add_image_transformer(self, function):
        self.image_transformers.append(function)

    def capture_video(self):
        window_w = max(self.root.winfo_width() - 6, 240)
        success, img = self.cap.read()
        if success:
            img_processed = img.copy()
            for tranformer in self.image_transformers:
                img_processed = tranformer(img_processed)
            img_rgb = cv2.cvtColor(cv2.resize(img_processed, (window_w, int(img.shape[0]*window_w/img.shape[1]))), cv2.COLOR_BGR2RGBA)
            img_pil = Image.fromarray(img_rgb)
            img_tk = ImageTk.PhotoImage(image=img_pil)
            self.image_label.img_tk = img_tk
            self.image_label.configure(image=img_tk)
            self.image_label.after(int(1000/20), self.capture_video)
            self.send_img_to_cam(img_processed)
        else:
            print("Capture didn't success! Trying again soon...")
            time.sleep(3)
            self.init_cap()
            self.capture_video()
    
    def init_cap(self):
        self.cap = cv2.VideoCapture(self.cap_id)
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, self.cap_width)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, self.cap_height)

    def start_mainloop(self):
        self.capture_video()
        self.root.mainloop()
        self.cap.release()
    
    def send_img_to_cam(self, img):
        if self.cam:
            self.cam.send(cv2.resize(cv2.cvtColor(img, cv2.COLOR_BGR2RGB), (self.cam_width, self.cam_height)))