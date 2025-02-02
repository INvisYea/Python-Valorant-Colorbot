import pyautogui
import keyboard
import time
import cv2
import numpy as np
from PIL import ImageGrab

def is_yellow(color):
    r, g, b = color
    return 200 <= r <= 255 and 200 <= g <= 255 and 0 <= b <= 100

screen_width, screen_height = pyautogui.size()
center_x, center_y = screen_width // 2, screen_height // 2
fov_radius = 10

def check_center_pixel():
    global fov_radius
    yellow_time = 0
    response_type = 'o'
    thresholds = {
        'i': 0.3,
        'o': 0.2,
        'p': 0.1
    }

    print("Press 'I' for slow response, 'O' for mid response, 'P' for fast response.")
    print("Press UP/DOWN arrows to increase/decrease FOV size.")
    print("Press 'Insert' to quit.")

    while True:
        start_time = time.time()

        if keyboard.is_pressed('i'):
            response_type = 'i'
        elif keyboard.is_pressed('o'):
            response_type = 'o'
        elif keyboard.is_pressed('p'):
            response_type = 'p'
        elif keyboard.is_pressed('insert'):
            print("Exiting...")
            break

        if keyboard.is_pressed('up'):
            fov_radius = min(fov_radius + 1, 100)
            print(f"FOV Radius Increased: {fov_radius}")
            time.sleep(0.1)

        if keyboard.is_pressed('down'):
            fov_radius = max(fov_radius - 1, 1)
            print(f"FOV Radius Decreased: {fov_radius}")
            time.sleep(0.1)

        yellow_time_threshold = thresholds.get(response_type, 0.2)
        screenshot = ImageGrab.grab()
        frame = np.array(screenshot)
        frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)

        yellow_detected = False
        for dx in range(-fov_radius, fov_radius + 1):
            for dy in range(-fov_radius, fov_radius + 1):
                if dx**2 + dy**2 <= fov_radius**2:
                    pixel_color = screenshot.getpixel((center_x + dx, center_y + dy))
                    if is_yellow(pixel_color[:3]):
                        yellow_detected = True
                        break
            if yellow_detected:
                break

        if yellow_detected:
            yellow_time += time.time() - start_time
            if yellow_time >= yellow_time_threshold:
                keyboard.press_and_release('k')
                print(f"Detected yellow for {yellow_time:.2f} seconds (Response: {response_type.upper()})")
        else:
            yellow_time = 0

        frame[:] = 0
        cv2.circle(frame, (center_x, center_y), fov_radius, (0, 255, 0), 2)

        if yellow_detected:
            cv2.circle(frame, (center_x, center_y), 10, (0, 255, 255), -1)

        cv2.imshow("Overlay", frame)

        elapsed_time = time.time() - start_time
        sleep_time = max(1/60 - elapsed_time, 0)
        time.sleep(sleep_time)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            print("Exiting...")
            break

    cv2.destroyAllWindows()

if __name__ == "__main__":
    check_center_pixel()
