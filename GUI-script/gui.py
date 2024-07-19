import tkinter as tk
from tkinter import ttk
import serial
import time
import threading
import math

class AngleMonitorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("角度モニター")
        
        self.serial_port = serial.Serial('COM7', 9600, timeout=1)
        self.data = []

        self.create_widgets()
        self.update_data()

    def create_widgets(self):
        self.frame = ttk.Frame(self.root)
        self.frame.pack(expand=True, fill=tk.BOTH)

        self.lean_angle_label = tk.Label(self.frame, text="傾き角度", font=("Helvetica", 24))
        self.lean_angle_label.grid(row=0, column=0, padx=20, pady=20)

        self.steering_angle_label = tk.Label(self.frame, text="ステアリング角度", font=("Helvetica", 24))
        self.steering_angle_label.grid(row=0, column=1, padx=20, pady=20)

        self.lean_angle_value = tk.Label(self.frame, text="0°", font=("Helvetica", 48))
        self.lean_angle_value.grid(row=1, column=0, padx=20, pady=20)

        self.steering_angle_value = tk.Label(self.frame, text="0°", font=("Helvetica", 48))
        self.steering_angle_value.grid(row=1, column=1, padx=20, pady=20)

        self.lean_angle_canvas = tk.Canvas(self.frame, width=200, height=200)
        self.lean_angle_canvas.grid(row=2, column=0, padx=20, pady=20)
        self.lean_angle_arrow = self.lean_angle_canvas.create_line(100, 100, 100, 20, arrow=tk.LAST, fill="blue", width=5)

        self.steering_angle_canvas = tk.Canvas(self.frame, width=200, height=200)
        self.steering_angle_canvas.grid(row=2, column=1, padx=20, pady=20)
        self.steering_angle_arrow = self.steering_angle_canvas.create_line(100, 100, 100, 20, arrow=tk.LAST, fill="red", width=5)

        self.time_label = tk.Label(self.frame, text="時間", font=("Helvetica", 24))
        self.time_label.grid(row=3, column=0, padx=20, pady=20, columnspan=2)

        self.time_value = tk.Label(self.frame, text="00:00:00.00", font=("Helvetica", 48))
        self.time_value.grid(row=4, column=0, padx=20, pady=20, columnspan=2)

    def update_data(self):
        if self.serial_port.in_waiting > 0:
            line = self.serial_port.readline().decode('utf-8').strip()
            print(f"Received line: {line}")  # デバッグ用にシリアルデータを出力
            try:
                time_str, angle1, angle2 = line.split(',')
                hours, minutes = map(int, time_str.split(':')[:2])
                seconds, centiseconds = map(float, time_str.split(':')[2].split('.'))
                time_stamp = (hours * 3600 + minutes * 60 + int(seconds)) * 1000 + int(centiseconds * 10)
                angle1 = int(angle1)
                angle2 = int(angle2)
                self.update_gui(time_stamp, angle1, angle2)
            except ValueError:
                print("Error parsing line:", line)  # デバッグ用
                pass
        
        self.root.after(10, self.update_data)

    def update_gui(self, time_stamp, angle1, angle2):
        self.lean_angle_value.config(text=f"{angle1}°")
        self.steering_angle_value.config(text=f"{angle2}°")

        self.update_arrow(self.lean_angle_canvas, self.lean_angle_arrow, angle1)
        self.update_arrow(self.steering_angle_canvas, self.steering_angle_arrow, angle2)

        time_str = time.strftime('%H:%M:%S', time.gmtime(time_stamp / 1000)) + f".{int(time_stamp % 1000 / 10):02d}"
        self.time_value.config(text=time_str)

    def update_arrow(self, canvas, arrow, angle):
        angle_rad = angle * 3.14159265359 / 180
        x_end = 100 + 80 * -math.sin(angle_rad)
        y_end = 100 - 80 * math.cos(angle_rad)
        canvas.coords(arrow, 100, 100, x_end, y_end)

if __name__ == "__main__":
    root = tk.Tk()
    app = AngleMonitorApp(root)
    root.mainloop()
