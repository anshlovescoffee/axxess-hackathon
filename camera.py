import cv2
import requests
import time

def scan_and_send():
    # Initialize OpenCV's built-in QRCodeDetector
    detector = cv2.QRCodeDetector()

    # For MacBook cameras, try different video capture APIs
    cap = cv2.VideoCapture(0, cv2.CAP_AVFOUNDATION)
    
    if not cap.isOpened():
        print("Error: Could not open camera")
        return
    
    print("Camera initialized. Looking for QR code...")
    print("Press 'q' to quit")
    
    while True:
        # Get frame from camera
        ret, frame = cap.read()
        
        if not ret:
            print("Error: Could not read frame")
            break
        
        # Flip the frame horizontally for a more intuitive mirror view
        frame = cv2.flip(frame, 1)
        
        # Detect and decode the QR code
        qr_data, points, _ = detector.detectAndDecode(frame)
        
        if points is not None and qr_data:
            # Draw a bounding box around the QR code
            points = points[0].astype(int)
            for i in range(len(points)):
                cv2.line(frame, tuple(points[i]), tuple(points[(i + 1) % len(points)]), (0, 255, 0), 2)
            
            print(f"QR Code detected! Data: {qr_data}")
            
            # Send to your API endpoint
            try:
                response = requests.post(
                    'http://localhost:5000/scan',  # Update this URL to match your server
                    json={'qr_data': qr_data},
                    headers={'Content-Type': 'application/json'}
                )
                
                if response.status_code == 200:
                    print("Successfully sent to server!")
                    print("Response:", response.json())
                    # Draw success message on frame
                    cv2.putText(frame, "Success!", (50, 50), 
                                cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
                else:
                    print(f"Error from server: {response.status_code}")
                    print("Response:", response.text)
                    # Draw error message on frame
                    cv2.putText(frame, "Error!", (50, 50), 
                                cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
                
                # Wait a bit to avoid multiple scans of the same QR code
                time.sleep(2)
                
            except requests.exceptions.RequestException as e:
                print(f"Error sending to server: {e}")
        
        # Show the camera feed
        cv2.imshow('QR Code Scanner (Press q to quit)', frame)
        
        # Break the loop if 'q' is pressed
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
            
    # Clean up
    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    scan_and_send()
