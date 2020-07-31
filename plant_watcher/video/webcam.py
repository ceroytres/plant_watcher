import abc
import io


from picamera.array import PiRGBArray
from picamera import PiCamera



class BaseWebCam(abc.ABC):

    @abc.abstractmethod
    def isOpen(self) -> bool:
        pass

    @abc.abstractmethod
    def get_frame(self):
        pass

    @abc.abstractmethod
    def get_stream(self):
        pass

    @abc.abstractmethod
    def close(self):
        pass

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, exc_tb):
        self.close()


class PiWebCam(BaseWebCam):

    def __init__(self, num=0):
        super(PiWebCam, self).__init__()
        self.cam = PiCamera(num)

    def isOpen(self) -> bool:
        return True

    def get_frame(self):

        with PiRGBArray(self.cam) as stream:
            camera.capture(stream, format='rgb')
            image = stream.array

        return image

    def get_stream(self, format: str = 'rgb') -> io.BytesIO:
        stream = io.BytesIO()
        self.cam.capture(stream, format=format)
        return stream

    def close(self):
        self.cam.close()
