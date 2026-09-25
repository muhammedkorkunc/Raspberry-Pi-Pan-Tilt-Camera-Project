# 📷 Dual-Axis Pan-Tilt Camera System with Web-Based Remote Telemetry

An embedded Linux IoT project built on **Raspberry Pi**, featuring real-time low-latency video streaming and precision dual-axis servo positioning via hardware-timed Pulse Width Modulation (PWM) and an asynchronous Flask REST architecture.

---

## 🖥️ System Interface & Live Stream Preview

![Web Controller Interface]
(servodirectionalcontrolpage.png)
(pan-tilt camera.png)

---

## 🏗️ System Architecture & Engineering Principles

The system bridges low-level hardware control with a modern web dashboard across three decoupled layers:

```text
[ Web Browser Client ]
       │  ▲
       │  │ HTTP Asynchronous Fetch / MJPEG Stream
       ▼  │
[ Flask Application Server (WSGI / Python 3) ]
       │
  ┌────┴───────────────────────────┐
  ▼                                ▼
[ Camera Pipeline ]        [ GPIO / Actuator Controller ]
• picamera Thread Worker   • RPi.GPIO Broadcom (BCM) Map
• In-memory JPEG Buffer    • 50 Hz Hardware-Timed PWM
• Multipart HTTP Streaming • Dynamic Duty Cycle Mapping
```

### 1. Actuator Mechanics & PWM Mathematics

Servo motors (SG90/MG90S) are driven by a **50 Hz (20 ms period)** PWM signal generated via Raspberry Pi GPIO. Standard servos interpret pulse widths between **1.0 ms and 2.0 ms** to determine angular positioning:

- **0° position:** $\approx 1.0\text{ ms pulse} \rightarrow 5.0\% \text{ duty cycle}$
- **90° (neutral):** $\approx 1.5\text{ ms pulse} \rightarrow 7.5\% \text{ duty cycle}$
- **180° position:** $\approx 2.0\text{ ms pulse} \rightarrow 10.0\% \text{ duty cycle}$

The `angleServoCtrl.py` module computes the exact duty cycle dynamically:
$$\text{Duty Cycle} = 2.5 + \left(\frac{\text{Target Angle}}{180} \times 10.0\right)$$
Upon reaching the targeted coordinate, PWM signals are halted to prevent mechanical jitter, eliminate continuous stall current, and conserve power.

### 2. Multi-Threaded Video Pipeline

Instead of blocking the web server for each client, video acquisition runs on a dedicated background worker thread (`camera_pi.py`).

- Captured frames from the CSI camera ribbon interface are encoded directly to JPEG in an in-memory byte buffer (`io.BytesIO`).
- Frames are broadcast via an HTTP multipart stream (`multipart/x-mixed-replace; boundary=frame`), maintaining low latency (< 180 ms over LAN) without the overhead of heavy external media streaming servers.

### 3. Asynchronous Non-Blocking Web Communication

The user interface uses the JavaScript `Fetch API` to dispatch asynchronous HTTP requests to endpoint routes (e.g., `/left`, `/right`, `/up`, `/down`). The dashboard remains fully interactive without full page refreshes during rapid directional adjustments.

---

## 📁 Repository Structure

```text
├── app.py                  # Main Flask entrypoint & HTTP route dispatchers
├── templates/
│   ├── controller.html     # Responsive Pan/Tilt UI dashboard
│   └── index.html          # Camera feed view template
└── server/
    ├── appCam.py           # Video streaming endpoint handlers
    ├── camera_pi.py        # Frame capturing logic & thread synchronization
    └── angleServoCtrl.py   # GPIO hardware setup & PWM duty cycle engine
```

---

## ⚙️ Pin Configuration & Wiring

| Component                  | Pin Function     | Raspberry Pi Physical Pin | BCM GPIO Pin       |
| :------------------------- | :--------------- | :------------------------ | :----------------- |
| **Pan Servo (Horizontal)** | PWM Signal       | Pin 12                    | GPIO 18 (PWM0)     |
| **Tilt Servo (Vertical)**  | PWM Signal       | Pin 33                    | GPIO 13 (PWM1)     |
| **Power Bus**              | +5V External VCC | Shared Ground             | 5V External Supply |
| **Ground**                 | Common GND       | Pin 6 / Pin 14            | GND                |
| **Pi Camera Module**       | CSI Ribbon Cable | Dedicated Camera Port     | CSI-2              |

> **Note:** Servos must share a common ground with the Raspberry Pi while drawing motor current from an external 5V power supply to avoid brownouts and voltage drops.

---

## 🚀 Deployment Guide

### Prerequisites

- Raspberry Pi (3B+ / 4B / Zero 2W) running Raspberry Pi OS
- Raspberry Pi Camera Module (v1/v2/v3) enabled via `raspi-config`
- Python 3.8+

### Setup & Execution

```bash
# 1. Clone repository
git clone [https://github.com/muhammedkorkunc/Raspberry-Pi-Pan-Tilt-Camera-Project.git](https://github.com/muhammedkorkunc/Raspberry-Pi-Pan-Tilt-Camera-Project.git)
cd Raspberry-Pi-Pan-Tilt-Camera-Project

# 2. Install dependencies
pip install Flask

# 3. Launch server on Raspberry Pi
python3 app.py
```

Open a browser on any device in the same local network:  
`http://<RASPBERRY_PI_IP>:5000`

---

## 🇹🇷 Türkçe Proje Özeti (Turkish Summary)

Bu çalışma, **Raspberry Pi** donanımı üzerinde gömülü Linux mimarisi kullanılarak geliştirilmiş iki eksenli (Pan-Tilt) uzaktan kamera yönlendirme ve canlı video akış sistemidir:

- **Gömülü Kontrol & PWM:** SG90 servo motorlar, Raspberry Pi'nin BCM GPIO pinleri üzerinden 50 Hz periyotlu donanımsal darbe genişlik modülasyonu (PWM) ile sürülmektedir. İstenen açılar dinamik formül ile Duty Cycle değerine dönüştürülür ve titreşimi önlemek için hedef açıda sinyal durdurulur.
- **Düşük Gecikmeli Canlı Yayın:** CSI arayüzünden alınan kamera kareleri bellek içi tamponlanarak (in-memory buffer) `multipart/x-mixed-replace` MJPEG formatında çoklu iş parçacığı (multi-threading) üzerinden gecikmesiz olarak tarayıcıya aktarılır.
- **Asenkron İstemci-Sunucu İletişimi:** Kontrol panelindeki yönlendirme komutları modern JavaScript `Fetch` API ile Flask REST uç noktalarına iletilir; sayfa yenilenmesine gerek kalmadan akıcı ve kesintisiz kontrol sağlanır.

---

## 👥 Contributors / Geliştirici Ekip

- **Muhammed Emin Korkunç**
- **Nurettin Süleymanoğlu**
- **Faruk Kerem Bedir**
