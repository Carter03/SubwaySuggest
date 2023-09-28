ready, frame = self.cam.read()
        if not ready:
            self.cam.release()
            cv2.destroyAllWindows()