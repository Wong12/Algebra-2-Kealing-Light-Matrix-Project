import os
import numpy as np
import picamera
from picamera.array import PiMotionAnalysis
import time

class GestureDetector(PiMotionAnalysis):
    QUEUE_SIZE = 10 # the number of consecutive frames to analyze
    THRESHOLD = 1.0 # the minimum average motion required in either axis

    def __init__(self, camera):
        super(GestureDetector, self).__init__(camera)
        self.x_queue = np.zeros(self.QUEUE_SIZE, dtype=np.float)
        self.y_queue = np.zeros(self.QUEUE_SIZE, dtype=np.float)
        self.last_move = ''

    def analyze(self, a):
        # Roll the queues and overwrite the first element with a new
        # mean (equivalent to pop and append, but faster)
        self.x_queue[1:] = self.x_queue[:-1]
        self.y_queue[1:] = self.y_queue[:-1]
        self.x_queue[0] = a['x'].mean()
        self.y_queue[0] = a['y'].mean()
        # Calculate the mean of both queues
        x_mean = self.x_queue.mean()
        y_mean = self.y_queue.mean()
        # Convert left/up to -1, right/down to 1, and movement below
        # the threshold to 0
        if abs(x_mean) < self.THRESHOLD:
            x_move = ''
        elif x_mean < 0.0:
            
        x_move = (
            '' if abs(x_mean) > self.THRESHOLD else
            'left' if x_mean > 0.0 else
            'right')
        y_move = (
            '' if abs(y_mean) > self.THRESHOLD else
            'down' if y_mean > 0.0 else
            'up')
        # Update the display
        movement = ('%s %s' % (x_move, y_move)).strip()
        if movement != self.last_move:
            self.last_move = movement
            if movement:
                print(movement)
            else:
                print("nobody home")
with picamera.PiCamera(resolution='VGA', framerate=24) as camera:
    with GestureDetector(camera) as detector:
        camera.rotation = 180
        
        time.sleep(2)
    
        camera.start_recording(
            os.devnull, format='h264', motion_output=detector)
        #camera.start_preview()
        
        try:
            while True:
                camera.wait_recording(1)
        except KeyboardInterrupt:
            pass
        finally:
            camera.stop_recording()
