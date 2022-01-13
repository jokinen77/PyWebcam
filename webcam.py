from tkinter import *
from PIL import ImageTk, Image
import cv2
import time
import threading
import pyvirtualcam

class Webcam:
    def __init__(self, cap_id=0, cap_width=1280, cap_height=720, cam=None, cam_width=1280, cam_height=720,
        target_fps=30, show_video=True):
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
        self.show_video = show_video
        self.target_fps = target_fps

        #FPS calculation
        self.capture_start_time_ns = 0
        self.prev_capture_start_time_ns = 0
        self.fps_count = 0
        self.fps_sum = 0
        self.fps = 0

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
        self.update_fps()
        window_w = max(self.root.winfo_width() - 6, 240)
        success, img = self.cap.read()
        if success:
            img_processed = img
            for tranformer in self.image_transformers:
                img_processed = tranformer(img_processed)
            self.send_img_to_cam(img_processed)
            if self.show_video:
                img_rgb = cv2.cvtColor(cv2.resize(img_processed, (window_w, int(img_processed.shape[0]*window_w/img_processed.shape[1]))), cv2.COLOR_BGR2RGBA)
                cv2.putText(img_rgb,'FPS: {}'.format(int(self.fps)), (20, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,0,0))
                img_pil = Image.fromarray(img_rgb)
                img_tk = ImageTk.PhotoImage(image=img_pil)
                self.image_label.img_tk = img_tk
                self.image_label.configure(image=img_tk)
                self.image_label.after(self.calc_target_fps_wait_ms(), self.capture_video)
            else:
                time.sleep(self.calc_target_fps_wait_ms()/1000)
                threading.Thread(target=self.capture_video).start()
        else:
            print("Capture didn't success! Trying again soon...")
            time.sleep(3)
            self.init_cap()
            self.capture_video()

        
    def update_fps(self):
        self.prev_capture_start_time_ns = self.capture_start_time_ns
        self.capture_start_time_ns = time.time_ns()
        if self.fps_count > 5:
            self.fps = int(self.fps_sum / self.fps_count)
            self.fps_sum = 0
            self.fps_count = 0
        self.fps_sum += 1e9 // max(1, self.capture_start_time_ns - self.prev_capture_start_time_ns)
        self.fps_count += 1
    
    def calc_target_fps_wait_ms(self):
        current_fps = 1e9 / (self.capture_start_time_ns - self.prev_capture_start_time_ns)
        target_fps_wait_time_ms = 1000 / self.target_fps
        processing_time_ms = (time.time_ns() - self.capture_start_time_ns) / 1e6
        wait_time_ms = max(1, target_fps_wait_time_ms - processing_time_ms + current_fps - self.target_fps)
        return int(wait_time_ms)

    def init_cap(self):
        self.cap = cv2.VideoCapture(self.cap_id)
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, self.cap_width)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, self.cap_height)
    
    def send_img_to_cam(self, img):
        if self.cam:
            self.cam.send(cv2.resize(cv2.cvtColor(img, cv2.COLOR_BGR2RGB), (self.cam_width, self.cam_height)))

    def start(self):
        with pyvirtualcam.Camera(width=self.cam_width, height=self.cam_height, fps=self.target_fps) as cam:
            self.cam = cam
            print("Virtual camera initialized!")
            self.init_cap()
            print("Capture device initialized!")
            self.capture_video()
            self.root.mainloop()
            self.cap.release()