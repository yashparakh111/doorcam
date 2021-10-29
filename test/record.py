import picamera

with picamera.PiCamera(framerate=10) as camera:
    camera.resolution = (640, 480)
    camera.start_recording('test_video.h264')
    camera.wait_recording(2)
    camera.stop_recording()
