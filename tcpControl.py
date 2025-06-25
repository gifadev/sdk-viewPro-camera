#!/usr/bin/env python3
import socket
import time
import tkinter as tk
from tkinter import ttk, messagebox

# ====== KONFIGURASI TCP ======
CAM_IP, CAM_PORT = "192.168.2.119", 2000
TIMEOUT = 2

# ====== RAW FRAME 20-byte (persis dari manual) ======
RAW = {
    "motor_on":      bytes.fromhex("55 AA DC 11 30 00 01 00 00 00 00 00 00 00 00 00 00 00 20"),
    "motor_off":     bytes.fromhex("55 AA DC 11 30 00 00 01 00 00 00 00 00 00 00 00 00 00 00 20"),
    "follow_on":     bytes.fromhex("55 AA DC 11 30 03 00 00 00 00 00 00 00 00 00 00 00 00 00 22"),
    "follow_off":    bytes.fromhex("55 AA DC 11 30 0A 00 00 00 00 00 00 00 00 00 00 00 00 00 2B"),

    "left":          bytes.fromhex("55 AA DC 11 30 01 F8 30 00 00 00 00 00 00 00 00 00 00 00 E8"),
    "right":         bytes.fromhex("55 AA DC 11 30 01 07 D0 00 00 00 00 00 00 00 00 00 00 00 F7"),
    "up":            bytes.fromhex("55 AA DC 11 30 01 00 00 07 D0 00 00 00 00 00 00 00 00 00 F7"),
    "down":          bytes.fromhex("55 AA DC 11 30 01 00 00 F8 30 00 00 00 00 00 00 00 00 00 E8"),
    "stop":          bytes.fromhex("55 AA DC 11 30 01 00 00 00 00 00 00 00 00 00 00 00 00 00 20"),

    "angle90":       bytes.fromhex("55 AA DC 11 30 0B 3F FC 3F FC 00 00 00 00 00 00 00 00 00 2A"),
    "recenter":      bytes.fromhex("55 AA DC 11 30 04 00 00 00 00 00 00 00 00 00 00 00 00 00 25"),

    "zoom_in":       bytes.fromhex("55 AA DC 11 30 0F 00 00 00 00 00 00 00 00 02 78 00 00 00 54"),
    "zoom_out":      bytes.fromhex("55 AA DC 11 30 0F 00 00 00 00 00 00 00 00 02 38 00 00 00 14"),
    "stop_zoom":     bytes.fromhex("55 AA DC 11 30 0F 00 00 00 00 00 00 00 00 00 00 00 00 00 2E"),
    "zoom20x":       bytes.fromhex("55 AA DC 0D 31 00 00 53 00 C8 00 00 00 00 00 A7"),

    "picrec":        bytes.fromhex("55 AA DC 11 30 0F 00 00 00 00 00 00 00 00 06 10 00 00 00 38"),
    "take_pic":      bytes.fromhex("55 AA DC 11 30 0F 00 00 00 00 00 00 00 00 04 D0 00 00 00 FA"),
    "start_rec":     bytes.fromhex("55 AA DC 11 30 0F 00 00 00 00 00 00 00 00 05 10 00 00 00 3B"),
    "stop_rec":      bytes.fromhex("55 AA DC 11 30 0F 00 00 00 00 00 00 00 00 05 50 00 00 00 7B"),

    "ir_dzoom_plus":  bytes.fromhex("55 AA DC 11 30 0F 00 00 00 00 00 00 00 00 06 D0 00 00 00 F8"),
    "ir_dzoom_minus": bytes.fromhex("55 AA DC 11 30 0F 00 00 00 00 00 00 00 00 07 10 00 00 00 39"),
    "eo_dzoom_on":    bytes.fromhex("55 AA DC 0D 31 00 00 06 00 00 00 00 00 00 00 3A"),
    "eo_dzoom_off":   bytes.fromhex("55 AA DC 0D 31 00 00 07 00 00 00 00 00 00 00 3B"),
}

def wrap_tcp(raw: bytes) -> bytes:
    length = len(raw)
    header = bytes([0xEB, 0x90, length])
    cs = sum(raw) & 0xFF
    return header + raw + bytes([cs])

def send_cmd(name: str):
    try:
        pkt = wrap_tcp(RAW[name])
        sock.sendall(pkt)
        status.set(f"Sent: {name}")
    except Exception as e:
        status.set(f"Error: {e}")

# ====== GUI ======
root = tk.Tk()
root.title("ViewPro ( ͡❛ ͜ʖ ͡❛)")
root.resizable(False, False)

status = tk.StringVar(value="Ready")
ttk.Label(root, textvariable=status).grid(row=0, column=0, columnspan=3, pady=5)

# Arrow pad
pad = ttk.Frame(root)
pad.grid(row=1, column=0, columnspan=3)
ttk.Button(pad, text="🢁", width=5, command=lambda: send_cmd("up")).grid(row=0, column=1)
ttk.Button(pad, text="🢀", width=5, command=lambda: send_cmd("left")).grid(row=1, column=0)
ttk.Button(pad, text="■", width=5, command=lambda: send_cmd("stop")).grid(row=1, column=1)
ttk.Button(pad, text="'🢂", width=5, command=lambda: send_cmd("right")).grid(row=1, column=2)
ttk.Button(pad, text="🢃", width=5, command=lambda: send_cmd("down")).grid(row=2, column=1)

# Gimbal Controls
gimb = ttk.LabelFrame(root, text="Gimbal Controls")
gimb.grid(row=2, column=0, padx=5, pady=5, sticky="ew")
buttons = [
    ("Recenter", "recenter"), ("Angle90°", "angle90"),
    ("Follow On", "follow_on"), ("Follow Off", "follow_off"),
    ("Motor On", "motor_on"), ("Motor Off", "motor_off"),
]
for i, (label, cmd) in enumerate(buttons):
    ttk.Button(gimb, text=label, width=12, command=lambda c=cmd: send_cmd(c))\
        .grid(row=i//2, column=i%2, padx=3, pady=3)

# Sensor & Zoom
sens = ttk.LabelFrame(root, text="Sensor & Zoom")
sens.grid(row=2, column=1, padx=5, pady=5, sticky="ew")
buttons = [
    ("Zoom In", "zoom_in"), ("Zoom Out", "zoom_out"),
    ("Stop Zoom", "stop_zoom"), ("20× Zoom", "zoom20x"),
    ("Pic/Rec", "picrec"),   ("Take Pic", "take_pic"),
    ("Start Rec", "start_rec"), ("Stop Rec", "stop_rec"),
]
for i, (label, cmd) in enumerate(buttons):
    ttk.Button(sens, text=label, width=12, command=lambda c=cmd: send_cmd(c))\
        .grid(row=i//2, column=i%2, padx=3, pady=3)

# Digital Zoom
dzoom = ttk.LabelFrame(root, text="Digital Zoom (Dzoom)")
dzoom.grid(row=2, column=2, padx=5, pady=5, sticky="ew")
buttons = [
    ("IR Dzoom+", "ir_dzoom_plus"), ("IR Dzoom-", "ir_dzoom_minus"),
    ("EO Dzoom On", "eo_dzoom_on"), ("EO Dzoom Off", "eo_dzoom_off"),
]
for i, (label, cmd) in enumerate(buttons):
    ttk.Button(dzoom, text=label, width=12, command=lambda c=cmd: send_cmd(c))\
        .grid(row=i//2, column=i%2, padx=3, pady=3)

# ====== Connect TCP ======
try:
    sock = socket.create_connection((CAM_IP, CAM_PORT), timeout=TIMEOUT)
    status.set(f"Connected to {CAM_IP}")
except Exception as e:
    messagebox.showerror("Connection Error", e)
    root.destroy()

# Cleanup on close
def on_close():
    try:
        sock.close()
    except:
        pass
    root.destroy()

root.protocol("WM_DELETE_WINDOW", on_close)
root.mainloop()
