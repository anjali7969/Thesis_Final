# usb_medical_classifier_zoom_save.py
# Run:  python usb_medical_classifier_zoom_save.py --cam 2 --port COM5

import time
import tempfile
import argparse
import cv2
import os
from datetime import datetime
from inference_sdk import InferenceHTTPClient

# ----- optional Arduino (pyserial) -----
try:
    import serial  # pip install pyserial
except Exception:
    serial = None

# ---- Roboflow config ----
API_URL  = "https://serverless.roboflow.com"
API_KEY  = "hgHsDbvaij3qIfFjE7mE"
MODEL_ID = "medical-waste/1"
CONF_THRESH = 0.35

# Define medical classes (everything else -> non-medical)
MEDICAL_CLASSES = {"gloves", "masks", "medicine", "syringe"}

# Signals
SIGNAL_MEDICAL = "1"
SIGNAL_NONMED  = "3"
SIGNAL_IDLE    = "2"

# Init client once
CLIENT = InferenceHTTPClient(api_url=API_URL, api_key=API_KEY)

# ---- CONFIG ----
SAVE_DIR = "E:/"
ZOOM_FACTOR = 2  # >1.0 means zoom-in

def zoom_frame(frame, zoom_factor=1.0):
    """Crop center and resize to original size."""
    if zoom_factor <= 1.0:
        return frame
    h, w = frame.shape[:2]
    nh, nw = int(h / zoom_factor), int(w / zoom_factor)
    y1, x1 = (h - nh) // 2, (w - nw) // 2
    y2, x2 = y1 + nh, x1 + nw
    cropped = frame[y1:y2, x1:x2]
    return cv2.resize(cropped, (w, h))

def open_serial(port: str | None, baud=9600, timeout=0.1):
    if not port or serial is None:
        if serial is None:
            print("[INFO] pyserial not installed; will only print signals.")
        else:
            print("[INFO] No serial port given; will only print signals.")
        return None
    try:
        ser = serial.Serial(port=port, baudrate=baud, timeout=timeout)
        time.sleep(1.8)  # Arduino reset
        return ser
    except Exception as e:
        print(f"[WARN] Could not open {port}: {e}. Will only print signals.")
        return None

def send_signal(ser, msg: str):
    print(f"Sending signal: {msg}")
    if ser:
        try:
            ser.write(msg.encode("utf-8"))
        except Exception as e:
            print(f"[WARN] Serial write failed: {e}")

def infer_from_frame(frame_bgr) -> dict:
    temp_path = tempfile.NamedTemporaryFile(suffix=".jpg", delete=False).name
    cv2.imwrite(temp_path, frame_bgr, [cv2.IMWRITE_JPEG_QUALITY, 85])
    return CLIENT.infer(temp_path, model_id=MODEL_ID)

def decide(preds: list[dict]) -> tuple[str, list[tuple[str, float]]]:
    hits = []
    medical_hit = False
    for p in preds or []:
        cls = str(p.get("class", "unknown")).lower()
        conf = float(p.get("confidence", 0.0))
        if conf < CONF_THRESH:
            continue
        hits.append((cls, conf))
        if cls in MEDICAL_CLASSES:
            medical_hit = True
    return ("MEDICAL" if medical_hit else "NON_MEDICAL"), hits

def save_captured_frame(frame):
    os.makedirs(SAVE_DIR, exist_ok=True)
    filename = f"captured_{datetime.now().strftime('%Y%m%d_%H%M%S')}.jpg"
    save_path = os.path.join(SAVE_DIR, filename)
    cv2.imwrite(save_path, frame)
    print(f"[INFO] Saved captured image to: {save_path}")

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--cam", type=int, default=1, help="Webcam index (0/1/2...)")
    ap.add_argument("--port", type=str, default="COM5", help="Arduino serial port")
    args = ap.parse_args()

    ser = open_serial(args.port)

    cap = cv2.VideoCapture(args.cam, cv2.CAP_DSHOW) if hasattr(cv2, "CAP_DSHOW") else cv2.VideoCapture(args.cam)
    if not cap.isOpened():
        print(f"[ERR] Could not open camera index {args.cam}")
        if ser: ser.close()
        return

    # Optional: set resolution
    cap.set(cv2.CAP_PROP_FRAME_WIDTH,  1280)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
    cap.set(cv2.CAP_PROP_FPS, 30)

    # Warmup
    for _ in range(5):
        cap.read()
        time.sleep(0.05)

    ok, frame = cap.read()
    cap.release()

    if not ok or frame is None:
        print("[ERR] Failed to capture frame.")
        if ser: ser.close()
        return

    # Zoom
    frame = zoom_frame(frame, ZOOM_FACTOR)

    # Save to E:/
    save_captured_frame(frame)

    # Inference
    try:
        result = infer_from_frame(frame)
    except Exception as e:
        print(f"[ERR] Inference failed: {e}")
        if ser: ser.close()
        return

    preds = result.get("predictions", [])
    decision, hits = decide(preds)

    if hits:
        for cls, conf in hits:
            print(f"Detected: {cls} ({conf*100:.1f}%)")
    else:
        print("No detections >= threshold.")

    print("Decision:", decision)

    # Send decision and idle
    send_signal(ser, SIGNAL_MEDICAL if decision == "MEDICAL" else SIGNAL_NONMED)
    time.sleep(1.5)
    send_signal(ser, SIGNAL_IDLE)

    if ser: ser.close()

if __name__ == "__main__":
    main()
