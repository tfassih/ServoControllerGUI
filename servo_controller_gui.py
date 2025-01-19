import tkinter as tk
from tkinter import ttk, messagebox
import serial
import serial.tools.list_ports
from typing import Optional

class ServoControllerGUI:
    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.title("SERVO CONTROLLER TEST")
        self.root.geometry("400x300")
        self.serial_connection: Optional[serial.Serial] = None

        self.main_frame = ttk.Frame(root, padding="10")
        self.main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        ttk.Label(self.main_frame, text="Serial Port: ").grid(row=0, column=0, sticky=tk.W)
        self.port_var = tk.StringVar()
        self.port_combo = ttk.Combobox(self.main_frame, textvariable=self.port_var)
        self.port_combo.grid(row=0, column=1, sticky=(tk.W, tk.E))

        self.connect_btn = ttk.Button(self.main_frame, text="Connect", command=self.toggle_connection)
        self.connect_btn.grid(row=0, column=2, padx=5)

        ttk.Button(self.main_frame, text="↻", command=self.refresh_ports, width=3).grid(row=0, column=3)

        ttk.Label(self.main_frame, text="Servo A", font=('Arial', 12, 'bold')).grid(row=1, column=0, columnspac=2, pady=10)
        self.servo_a_scale = ttk.Scale(self.main_frame, from_=0, to=180, orient=tk.HORIZONTAL,
                                       command= lambda v: self.update_angle_label('A', v))
        self.servo_a_scale.grid(row=2, column=0, columnspan=3, sticky=(tk.W, tk.E))
        self.servo_a_label = ttk.Label(self.main_frame, text="0°")
        self.servo_a_label.grid(row=2, column=3)
        ttk.Button(self.main_frame, text="Set Servo A",
                   command=lambda: self.send_servo_command('A')).grid(row=3, column=0, columnspan=2, pady=5)

        ttk.Label(self.main_frame, text="Servo B",
                  font=('Arial', 12, 'bold')).grid(row=4, column=0, columnspan=2, pady=10)
        self.servo_b_scale = ttk.Scale(self.main_frame, from_=0, to=180, orient=tk.HORIZONTAL,
                                       command=lambda v: self.update_angle_label('B', v))
        self.servo_b_scale.grid(row=5, column=0, columnspan=3, sticky=(tk.W, tk.E))
        self.servo_b_label = ttk.Label(self.main_frame, text="0°")
        self.servo_b_label.grid(row=5, column=3)
        ttk.Button(self.main_frame, text="Set Servo B",
                   command=lambda: self.send_servo_command('B')).grid(row=6, column=0, columnspan=2, pady=5)

        self.refresh_ports()

    def refresh_ports(self):
        ports = [port.device for port in serial.tools.list_ports.comports()]
        self.port_combo['values'] = ports
        if ports:
            self.port_combo.set(ports[0])

    def toggle_connection(self):
        if self.serial_connection is None:
            try:
                port = self.port_var.get()
                self.serial_connection = serial.Serial(port, 9600, timeout=1)
                self.connect_btn.config(text="Disconnect")
                messagebox.showinfo("SUCCESS", f"Connected to {port}")
            except serial.SerialException as e:
                messagebox.showerror("Error", f"Failed to connect: {str(e)}")
        else:
            self.serial_connection.close()
            self.serial_connection = None
            self.connect_btn.config(text="Connect")

    def update_angle_label(self, servo: str, value: float):
        angle = int(float(value))
        if servo == 'A':
            self.servo_a_label.config(text=f"{angle}°")
        else:
            self.servo_b_label.config(text=f"{angle}°")

    def send_servo_command(self, servo: str):
        if self.serial_connection is None:
            messagebox.showerror("Error", "NO CONNECTION")
            return

        angle = int(self.servo_a_scale.get() if servo == 'A' else self.servo_b_scale.get())
        command = f"S{servo}:{angle}\n"

        try:
            self.serial_connection.write(command.encode())
            response = self.serial_connection.readline().decode().strip()
            print(f"Arduino response: {response}")
        except serial.SerialException as e:
            messagebox.showerror("Error", f"Failed to send command: {str(e)}")
            self.serial_connection = None
            self.connect_btn.config(text="Connect")

def main():
    root = tk.Tk()
    app = ServoControllerGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()

