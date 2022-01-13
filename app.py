from functions import *
import pyvirtualcam
from hand_detector import full_detect_hands
from webcam import Webcam

CAP_PROPS = {
    "CAP_ID": 0, #Capture device id, usually 0 is correct
    "GAMMA": 1.0,
    "CONTRAST": 1.0,
    "BRIGHTNESS": 0.0,
    "HUE": 0.0,
    "WIDTH": 960,
    "HEIGHT": 640,
    "GAUSSIAN_KERNEL_SIZE": 0,
    "GAUSSIAN_KERNEL_SIGMA": 0,
    "HAND_DETECTION": False,
    "ROTATE_DEGREES": 0,
    "MIRROR": False
}

CAM_PROPS = {
    "TARGET_FPS": 30, #Usually real fps is smaller than this.
    "WIDTH": CAP_PROPS["WIDTH"],
    "HEIGHT": CAP_PROPS["HEIGHT"]
}

GUI_PROPS = {
    "SHOW_VIDEO": True #Setting this to 'False' might stabilize the program in some cases.
}

if __name__ == "__main__":
    webcam = Webcam(cap_id=CAP_PROPS["CAP_ID"], cap_width=CAP_PROPS["WIDTH"], cap_height=CAP_PROPS["HEIGHT"], 
        cam_width=CAM_PROPS["WIDTH"], cam_height=CAM_PROPS["HEIGHT"], show_video=GUI_PROPS["SHOW_VIDEO"],
        target_fps=CAM_PROPS["TARGET_FPS"])
        
    webcam.create_parameter_slider(1, CAP_PROPS, "GAMMA", "Gamma", values=(0,5,(5-0)/100))
    webcam.create_parameter_slider(2, CAP_PROPS, "CONTRAST", "Contrast", values=(0,2,(2-0)/100))
    webcam.create_parameter_slider(3, CAP_PROPS, "BRIGHTNESS", "Brightness", values=(-128,128,(128+128)/100))
    webcam.create_parameter_slider(4, CAP_PROPS, "HUE", "Hue", values=(-60,60,(60+60)/100))
    webcam.create_parameter_slider(5, CAP_PROPS, "GAUSSIAN_KERNEL_SIZE", "Gaussian kernel size", values=(0,20,1))
    webcam.create_parameter_slider(6, CAP_PROPS, "GAUSSIAN_KERNEL_SIGMA", "Gaussian kernel sigma", values=(0,5,0.1))
    webcam.create_parameter_slider(7, CAP_PROPS, "ROTATE_DEGREES", "Rotate angle (slow)", values=(0,360,45))
    webcam.create_parameter_checkbox(8, CAP_PROPS, "HAND_DETECTION", "Hand detection")
    webcam.create_parameter_checkbox(9, CAP_PROPS, "MIRROR", "Mirror")
        
    webcam.add_image_transformer(lambda img: hue_correction(img, hue=CAP_PROPS["HUE"]))
    webcam.add_image_transformer(lambda img: gamma_correction(img, CAP_PROPS["GAMMA"]))
    webcam.add_image_transformer(lambda img: contrast_correction(img, alpha=CAP_PROPS["CONTRAST"], beta=CAP_PROPS["BRIGHTNESS"]))
    webcam.add_image_transformer(lambda img: gaussian_filter(img, size=CAP_PROPS["GAUSSIAN_KERNEL_SIZE"], sigma=CAP_PROPS["GAUSSIAN_KERNEL_SIGMA"]))
    webcam.add_image_transformer(lambda img: rotate_image(img, CAP_PROPS["ROTATE_DEGREES"]))
    webcam.add_image_transformer(lambda img: mirror_image(img, flip=CAP_PROPS["MIRROR"]))
    webcam.add_image_transformer(lambda img: full_detect_hands(img, draw=True, skip=(not CAP_PROPS["HAND_DETECTION"])))

    webcam.start()