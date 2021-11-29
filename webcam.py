from functions import *
import pyvirtualcam
from hand_detector import full_detect_hands
from webcam_gui import WebcamGUI

CAP_PROPS = {
    "GAMMA": 1.0,
    "CONTRAST": 1.0,
    "BRIGHTNESS": 0.0,
    "HUE": 0.0,
    "WIDTH": 960,
    "HEIGHT": 540,
    "GAUSSIAN_KERNEL_SIZE": 0,
    "GAUSSIAN_KERNEL_SIGMA": 0,
    "HAND_DETECTION": False,
    "ROTATE_DEGREES": 0,
    "MIRROR": False
}

CAM_PROPS = {
    "FPS": 30,
    "WIDTH": CAP_PROPS["WIDTH"],
    "HEIGHT": CAP_PROPS["HEIGHT"]
}

if __name__ == "__main__":
    with pyvirtualcam.Camera(width=CAM_PROPS["WIDTH"], height=CAM_PROPS["HEIGHT"], fps=CAM_PROPS["FPS"]) as cam:
        gui = WebcamGUI(cap_id=0, cap_width=CAP_PROPS["WIDTH"], cap_height=CAP_PROPS["HEIGHT"], cam_width=CAM_PROPS["WIDTH"], cam_height=CAM_PROPS["HEIGHT"], cam=cam)
        
        gui.create_parameter_slider(1, CAP_PROPS, "GAMMA", "Gamma", values=(0,5,(5-0)/100))
        gui.create_parameter_slider(2, CAP_PROPS, "CONTRAST", "Contrast", values=(0,2,(2-0)/100))
        gui.create_parameter_slider(3, CAP_PROPS, "BRIGHTNESS", "Brightness", values=(-128,128,(128+128)/100))
        gui.create_parameter_slider(4, CAP_PROPS, "HUE", "Hue", values=(-60,60,(60+60)/100))
        gui.create_parameter_slider(5, CAP_PROPS, "GAUSSIAN_KERNEL_SIZE", "Gaussian kernel size", values=(0,20,1))
        gui.create_parameter_slider(6, CAP_PROPS, "GAUSSIAN_KERNEL_SIGMA", "Gaussian kernel sigma", values=(0,5,0.1))
        gui.create_parameter_slider(7, CAP_PROPS, "ROTATE_DEGREES", "Rotate angle (slow)", values=(0,360,45))
        gui.create_parameter_checkbox(8, CAP_PROPS, "HAND_DETECTION", "Hand detection")
        gui.create_parameter_checkbox(9, CAP_PROPS, "MIRROR", "Mirror")
        
        gui.add_image_transformer(lambda img: hue_correction(img, hue=CAP_PROPS["HUE"]))
        gui.add_image_transformer(lambda img: gamma_correction(img, CAP_PROPS["GAMMA"]))
        gui.add_image_transformer(lambda img: contrast_correction(img, alpha=CAP_PROPS["CONTRAST"], beta=CAP_PROPS["BRIGHTNESS"]))
        gui.add_image_transformer(lambda img: gaussian_filter(img, size=CAP_PROPS["GAUSSIAN_KERNEL_SIZE"], sigma=CAP_PROPS["GAUSSIAN_KERNEL_SIGMA"]))
        gui.add_image_transformer(lambda img: rotate_image(img, CAP_PROPS["ROTATE_DEGREES"]))
        gui.add_image_transformer(lambda img: mirror_image(img, flip=CAP_PROPS["MIRROR"]))
        gui.add_image_transformer(lambda img: full_detect_hands(img, draw=True, skip=(not CAP_PROPS["HAND_DETECTION"])))

        gui.init_cap()
        gui.start_mainloop()