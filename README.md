# 🎮 ViewPro Ground Control GUI

Python-based desktop GUI for controlling ViewPro camera gimbal via **TCP** or **Serial** using predefined hex commands based on the official protocol documentation.

## 📁 Contents

This repository includes two interfaces for controlling the gimbal:

- `tcpControl.py` — Communicates with the ViewPro camera using **TCP/IP socket**
- `serialControl.py` — Communicates with the ViewPro camera using **Serial COM port**

Both GUIs are built using Python's `tkinter` and offer control over:
- Gimbal movement (up, down, left, right, stop)
- Zoom in/out & stop
- Center/recenter view
- Motor & Follow mode
- Image capture and video recording
- Digital Zoom (EO/IR)

---

## 🚀 Getting Started

### 🔧 Requirements

- Python 3.10+
- Works on Windows/Linux
- `pyserial` (for serial version)

Install dependencies:

```bash
pip install pyserial
```
## 🧠 Usage

### 🖥 TCP Control

```bash
python tcpControl.py
```

* Make sure to update `CAM_IP` and `CAM_PORT` in the file to match your device IP.
* Connects automatically when the program starts.

### 🔌 Serial Control

```bash
python serialControl.py
```

* Ensure the correct COM port is selected (default is `COM4`).
* Change the port in the `serial.Serial(...)` section if needed.

---

## 🕹️ Features

* Simple GUI with arrow pad for gimbal movement
* Zoom, record, and snapshot support
* IR/EO digital zoom toggle
* Multiple command categories grouped in logical frames
* TCP and Serial command structure compatible with ViewPro protocols
* Automatic checksum and packet formatting for TCP

---

## ⚠️ Notes

* Make sure the ViewPro device is properly connected and powered on.
* TCP version requires network access to the camera IP.
* Serial version requires direct USB UART connection.

---

## ✍️ Author

Built by **\[Gisna Fauzian Dermawan]** — feel free to fork or contribute.
