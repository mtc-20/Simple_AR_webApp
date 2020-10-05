import cv2

faceCascade = cv2.CascadeClassifier('./models/haarcascade_frontalface_alt2.xml')
mask = cv2.imread('./models/goku_saiyan_hair.png')

class VideoCam(object):
    def __init__(self):
        self.video = cv2.VideoCapture(0)
        

    def __del__(self):
        self.video.release()

    def get_frame(self):
        ret, frame = self.video.read()
        
        # Do stuff here
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = faceCascade.detectMultiScale(gray, minNeighbors=5)
        for (fx, fy, fw, fh) in faces:
            if fh <=0 or fw <= 0:
                # print("[WARN] Skipping...")
                continue
            # cv2.rectangle(frame, (fx, fy), (fx+fw, fy+fh), (0, 200, 0), 2, 8)
            fw, fh = int(fw*1.6), int(fh*1.6)
            fy -= int(0.6*fh)
            fx -= int(0.2*fw)
            
            roi = frame[fy:fy+fh, fx:fx+fw]
            mask_resized = cv2.resize(mask, (fw, fh), interpolation=cv2.INTER_AREA)
            mask_gray = cv2.cvtColor(mask_resized, cv2.COLOR_BGR2GRAY)
            ret, mask_thresh = cv2.threshold(mask_gray, 150, 255, cv2.THRESH_BINARY_INV)
            # mask_inv = cv2.bitwise_not(mask_gray)
            # masked_face =  cv2.bitwise_and(mask_resized, mask_resized, mask=mask_thresh)
            # mask_reinv = cv2.bitwise_not(mask_thresh)
            masked_frame = cv2.bitwise_and(roi, roi, mask=mask_thresh)
            frame[fy:fy+fh, fx:fx+fw] = cv2.add(mask_resized, masked_frame)

        ret, jpeg = cv2.imencode('.jpg', frame)

        return jpeg.tobytes()
