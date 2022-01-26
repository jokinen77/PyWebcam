from functions import *
from hand_detector import full_detect_hands
from webcam import Webcam
import sys
import ast

PROPS = {
    "CAP_ID": 0, #Capture device id, usually 0 is correct
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
    "MIRROR": False,
    "SHOW_VIDEO": True, #Setting this to 'False' might stabilize the program in some cases.
    "TARGET_FPS": 30 #Usually real fps is smaller than this.
}

if __name__ == "__main__":
    for argv in sys.argv[1:]:
        if "=" not in argv:
            continue
        key = argv.split("=")[0].upper()
        value = ast.literal_eval(argv.split("=")[1])
        if key in PROPS.keys():
            PROPS[key] = value


    webcam = Webcam(cap_id=PROPS["CAP_ID"], cap_width=PROPS["WIDTH"], cap_height=PROPS["HEIGHT"], 
        cam_width=PROPS["WIDTH"], cam_height=PROPS["HEIGHT"], show_video=PROPS["SHOW_VIDEO"],
        target_fps=PROPS["TARGET_FPS"])
        
    webcam.create_parameter_slider(1, PROPS, "GAMMA", "Gamma", values=(0,5,(5-0)/100))
    webcam.create_parameter_slider(2, PROPS, "CONTRAST", "Contrast", values=(0,2,(2-0)/100))
    webcam.create_parameter_slider(3, PROPS, "BRIGHTNESS", "Brightness", values=(-128,128,(128+128)/100))
    webcam.create_parameter_slider(4, PROPS, "HUE", "Hue", values=(-60,60,(60+60)/100))
    webcam.create_parameter_slider(5, PROPS, "GAUSSIAN_KERNEL_SIZE", "Gaussian kernel size", values=(0,20,1))
    webcam.create_parameter_slider(6, PROPS, "GAUSSIAN_KERNEL_SIGMA", "Gaussian kernel sigma", values=(0,5,0.1))
    webcam.create_parameter_slider(7, PROPS, "ROTATE_DEGREES", "Rotate angle (slow)", values=(0,360,45))
    webcam.create_parameter_checkbox(8, PROPS, "HAND_DETECTION", "Hand detection")
    webcam.create_parameter_checkbox(9, PROPS, "MIRROR", "Mirror")
        
    webcam.add_image_transformer(lambda img: hue_correction(img, hue=PROPS["HUE"]))
    webcam.add_image_transformer(lambda img: gamma_correction(img, PROPS["GAMMA"]))
    webcam.add_image_transformer(lambda img: contrast_correction(img, alpha=PROPS["CONTRAST"], beta=PROPS["BRIGHTNESS"]))
    webcam.add_image_transformer(lambda img: gaussian_filter(img, size=PROPS["GAUSSIAN_KERNEL_SIZE"], sigma=PROPS["GAUSSIAN_KERNEL_SIGMA"]))
    webcam.add_image_transformer(lambda img: rotate_image(img, PROPS["ROTATE_DEGREES"]))
    webcam.add_image_transformer(lambda img: mirror_image(img, flip=PROPS["MIRROR"]))
    webcam.add_image_transformer(lambda img: full_detect_hands(img, draw=True, skip=(not PROPS["HAND_DETECTION"])))

    webcam.start()