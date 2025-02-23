import cv2
import requests
import time
import json
from typing import Optional, Tuple
import logging
import numpy as np

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class QRScanner:
    def __init__(self, api_url: str):
        self.api_url = api_url
        self.detector = cv2.QRCodeDetector()
        self.last_scan_data = None
        self.last_scan_time = 0
        self.scan_cooldown = 2  # seconds between scans

    def initialize_camera(self) -> Optional[cv2.VideoCapture]:
        """Initialize camera with fallback options."""
        camera_apis = [
            (0, cv2.CAP_AVFOUNDATION),  # MacOS
            (0, cv2.CAP_ANY),           # Any available API
            (0, cv2.CAP_DSHOW),         # DirectShow (Windows)
            (1, cv2.CAP_ANY),           # Try second camera if available
        ]

        for camera_id, api in camera_apis:
            cap = cv2.VideoCapture(camera_id, api)
            if cap.isOpened():
                logger.info(f"Successfully opened camera with ID {camera_id} using API {api}")
                return cap
            cap.release()

        logger.error("Failed to initialize camera with any available API")
        return None

    def process_frame(self, frame: np.ndarray) -> Tuple[np.ndarray, Optional[str]]:
        """Process a single frame and return the modified frame and QR data if found."""
        frame = cv2.flip(frame, 1)  # Mirror view
        qr_data, points, _ = self.detector.detectAndDecode(frame)

        if points is not None and qr_data:
            # Draw bounding box
            points = points[0].astype(int)
            cv2.polylines(frame, [points], True, (0, 255, 0), 2)

            # Check cooldown
            current_time = time.time()
            if (current_time - self.last_scan_time >= self.scan_cooldown and 
                qr_data != self.last_scan_data):
                self.last_scan_data = qr_data
                self.last_scan_time = current_time
                return frame, qr_data

        return frame, None

    def send_to_server(self, qr_data: str) -> bool:
        """Send QR data to server with proper error handling."""
        headers = {
            'Content-Type': 'application/json'
        }

        try:
            response = requests.post(
                self.api_url,
                json={'qr_data': qr_data},
                headers=headers,
                timeout=5
            )
            response.raise_for_status()
            response_data = response.json()
            
            if response_data.get('status') == 'success':
                logger.info(f"Successfully processed QR code: Medicine ID {response_data.get('med_id')}, Quantity {response_data.get('quantity')}")
                return True
            else:
                logger.error(f"Server error: {response_data.get('message', 'Unknown error')}")
                return False

        except requests.exceptions.RequestException as e:
            logger.error(f"Error sending to server: {str(e)}")
            return False

    def run(self):
        """Main scanning loop."""
        cap = self.initialize_camera()
        if not cap:
            return

        logger.info("QR Scanner started. Press 'q' to quit.")

        try:
            while True:
                ret, frame = cap.read()
                if not ret:
                    logger.error("Failed to read frame")
                    break

                frame, qr_data = self.process_frame(frame)

                if qr_data:
                    logger.info(f"QR Code detected: {qr_data}")
                    success = self.send_to_server(qr_data)
                    
                    # Display status on frame
                    status_text = "Success!" if success else "Error!"
                    color = (0, 255, 0) if success else (0, 0, 255)
                    cv2.putText(frame, status_text, (50, 50),
                              cv2.FONT_HERSHEY_SIMPLEX, 1, color, 2)

                cv2.imshow('QR Code Scanner (Press q to quit)', frame)
                
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break

        finally:
            cap.release()
            cv2.destroyAllWindows()

if __name__ == "__main__":
    # Configuration - update port to match Flask server
    API_URL = "http://localhost:5001/scan"   # Updated port to 5001
    
    scanner = QRScanner(API_URL)
    scanner.run()