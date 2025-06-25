import serial
import time
import tkinter as tk
from tkinter import ttk

# Initialize serial connection (update port if needed)
ser = serial.Serial(port='COM4', baudrate=115200,
                    bytesize=serial.EIGHTBITS, parity=serial.PARITY_NONE,
                    stopbits=serial.STOPBITS_ONE, timeout=1)

def send_cmd(hex_str: str) -> bytes:
    """Send hex command string over serial and return raw response."""
    cmd_bytes = bytes.fromhex(hex_str.replace(' ', ''))
    ser.write(cmd_bytes)
    time.sleep(0.05)
    resp = ser.read(ser.in_waiting or 1)
    return resp

# Command dictionary
CMDS = {
    # Gimbal movement
    'left':      '55 AA DC 11 30 01 F8 30 00 00 00 00 00 00 00 00 00 00 00 E8',
    'right':     '55 AA DC 11 30 01 07 D0 00 00 00 00 00 00 00 00 00 00 00 F7',
    'up':        '55 AA DC 11 30 01 00 00 07 D0 00 00 00 00 00 00 00 00 00 F7',
    'down':      '55 AA DC 11 30 01 00 00 F8 30 00 00 00 00 00 00 00 00 00 E8',
    'stop':      '55 AA DC 11 30 01 00 00 00 00 00 00 00 00 00 00 00 00 00 20',
    'angle90':   '55 AA DC 11 30 0B 3F FC 3F FC 00 00 00 00 00 00 00 00 00 2A',
    'recenter':  '55 AA DC 11 30 04 00 00 00 00 00 00 00 00 00 00 00 00 00 25',
    'follow_on': '55 AA DC 11 30 03 00 00 00 00 00 00 00 00 00 00 00 00 00 22',
    'follow_off':'55 AA DC 11 30 0A 00 00 00 00 00 00 00 00 00 00 00 00 00 2B',
    'motor_on':  '55 AA DC 11 30 00 01 00 00 00 00 00 00 00 00 00 00 00 00 20',
    'motor_off': '55 AA DC 11 30 00 00 01 00 00 00 00 00 00 00 00 00 00 00 20',
    # Sensor control
    'zoom_in':    '55 AA DC 11 30 0F 00 00 00 00 00 00 00 00 02 78 00 00 00 54',
    'zoom_out':   '55 AA DC 11 30 0F 00 00 00 00 00 00 00 00 02 38 00 00 00 14',
    'stop_zoom':  '55 AA DC 11 30 0F 00 00 00 00 00 00 00 00 00 00 00 00 00 2E',
    'zoom20x':    '55 AA DC 0D 31 00 00 53 00 C8 00 00 00 00 00 A7',
    'picrec':     '55 AA DC 11 30 0F 00 00 00 00 00 00 00 00 06 10 00 00 00 38',
    'take_pic':   '55 AA DC 11 30 0F 00 00 00 00 00 00 00 00 04 D0 00 00 00 FA',
    'start_rec':  '55 AA DC 11 30 0F 00 00 00 00 00 00 00 00 05 10 00 00 00 3B',
    'stop_rec':   '55 AA DC 11 30 0F 00 00 00 00 00 00 00 00 05 50 00 00 00 7B',
    # Digital Zoom
    'ir_dzoom_plus':  '55 AA DC 11 30 0F 00 00 00 00 00 00 00 00 06 D0 00 00 00 F8',
    'ir_dzoom_minus': '55 AA DC 11 30 0F 00 00 00 00 00 00 00 00 07 10 00 00 00 39',
    'eo_dzoom_on':    '55 AA DC 0D 31 00 00 06 00 00 00 00 00 00 00 3A',
    'eo_dzoom_off':   '55 AA DC 0D 31 00 00 07 00 00 00 00 00 00 00 3B'
}

# GUI Setup
window = tk.Tk()
window.title('Viw Pro (͡❛ ͜ʖ͡❛)')
window.geometry('450x550')

# Response display
resp_var = tk.StringVar(value='Ready')
resp_label = ttk.Label(window, textvariable=resp_var, anchor='center')
resp_label.pack(pady=5)

# Command executor
def do_cmd(key):
    resp = send_cmd(CMDS[key])
    resp_var.set(f"Sent {key.replace('_',' ')}, received: {resp.hex()}")

# Movement buttons frame
gframe = ttk.Frame(window)
gframe.pack(pady=10)
ttk.Button(gframe, text='🢁', width=5, command=lambda: do_cmd('up')).grid(row=0, column=1)
ttk.Button(gframe, text='🢀', width=5, command=lambda: do_cmd('left')).grid(row=1, column=0)
ttk.Button(gframe, text='■', width=5, command=lambda: do_cmd('stop')).grid(row=1, column=1)
ttk.Button(gframe, text='🢂', width=5, command=lambda: do_cmd('right')).grid(row=1, column=2)
ttk.Button(gframe, text='🢃', width=5, command=lambda: do_cmd('down')).grid(row=2, column=1)

# Additional controls frame
aframe = ttk.LabelFrame(window, text='Gimbal Controls')
aframe.pack(pady=10)
controls = [
    ('Recenter', 'recenter'), ('Angle90°', 'angle90'),
    ('Follow On', 'follow_on'), ('Follow Off', 'follow_off'),
    ('Motor On', 'motor_on'), ('Motor Off', 'motor_off')
]
for i, (label, key) in enumerate(controls):
    ttk.Button(aframe, text=label, width=12,
               command=lambda k=key: do_cmd(k)).grid(row=i//2, column=i%2, padx=5, pady=3)

# Sensor controls frame
sframe = ttk.LabelFrame(window, text='Sensor & Zoom')
sframe.pack(pady=10)
sensors = [
    ('Zoom In', 'zoom_in'), ('Zoom Out', 'zoom_out'), ('Stop Zoom', 'stop_zoom'),
    ('20x Zoom', 'zoom20x'), ('Pic/Rec', 'picrec'), ('Take Pic', 'take_pic'),
    ('Start Rec', 'start_rec'), ('Stop Rec', 'stop_rec')
]
for i, (label, key) in enumerate(sensors):
    ttk.Button(sframe, text=label, width=10,
               command=lambda k=key: do_cmd(k)).grid(row=i//4, column=i%4, padx=3, pady=3)

# Digital Zoom controls frame
dframe = ttk.LabelFrame(window, text='Digital Zoom (Dzoom)')
dframe.pack(pady=10)
dz = [
    ('IR Dzoom+', 'ir_dzoom_plus'), ('IR Dzoom-', 'ir_dzoom_minus'),
    ('EO Dzoom ON', 'eo_dzoom_on'), ('EO Dzoom OFF', 'eo_dzoom_off')
]
for i, (label, key) in enumerate(dz):
    ttk.Button(dframe, text=label, width=12,
               command=lambda k=key: do_cmd(k)).grid(row=i//2, column=i%2, padx=5, pady=3)

window.mainloop()
