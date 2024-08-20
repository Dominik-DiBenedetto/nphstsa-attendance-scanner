import cv2
from pyzbar.pyzbar import decode
from sheet_writer import Attendance
from playsound import playsound
import datetime

SHEET_ID = ""
attendance_manager = Attendance(SHEET_ID)
today = str(datetime.datetime.now()).split(" ")[0]

def BarcodeReader(img):
    detectedBarcodes = decode(img)
    if not detectedBarcodes: return

    for barcode in detectedBarcodes:
        if barcode.data == "": continue

        try:
            if barcode.data.decode("utf-8")[0] != "N": continue

            playsound("./beepsound.mp3")
            attendance_manager.update_attendance(barcode.data, today)
        except: pass

vid = cv2.VideoCapture(0)

while True:
    ret, frame = vid.read()
    cv2.imshow("Attendance", frame)

    BarcodeReader(frame)

    if cv2.waitKey(1) & 0xFF == ord('q'): break

vid.release()
cv2.destroyAllWindows()
