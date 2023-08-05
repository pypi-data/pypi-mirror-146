import abc
import numpy as np
class BaseProcessor():
    """ Parent Processor class.   

    Attributes:
        _enable (bool): boolean that allows the processor to perform

    """

    def __init__(self,enable_boolean: bool = True): 
        
        """__Init__ method for the BaseProcessor.

            Args:
            enable_boolean (bool): Boolean that can be set as True or False and allows the processor to perform

        """
        __metaclass__ = abc.ABCMeta
        if  type (enable_boolean):
            self._enable = enable_boolean
        else:
            raise TypeError("enable must be a boolean value")
        

    
    @property      
    def enable(self):
        """ bool: allows the processor to perform."""        
        return self._enable
      
    @enable.setter
    def enable(self, val):
        """ bool: process enabled 
        
        Raises:
            TypeError: enable must be a boolean value
        """
        if  type (val) == bool:
            self._enable = val
        else:
            raise TypeError("enable must be a boolean value")
        

    @abc.abstractmethod
    def process(image):
        
        """ process the input 2D numpy data .
       
        Args:
            image: 2D numpy data.

        Returns:
            image if enabled 

        Raises:
           ValueError: process is not enabled.

        """
        if  (self._enable == True):
            return image
        else:
             raise ValueError("Process is not enabled")


class Lens(BaseProcessor):
    """ Lens class childer of BaseProcessor
        Simple Lens emulator 

        Attributes:
            height (int): height of the emulated camera Lens
            height (int): width of the emulated camera Lens
        
    """
    def __init__(self,height: int = 0,width: int = 0):
        """__Init__ method for the lens class.
                inherits BaseProcessor properties.

        Args:
            height (int): initial value for the emulated camera Lens height
            width (int): initial value for the emulated camera Lens width
        """
        super().__init__()
        if  type (height) == int and type (width) == int:
            self._height = height
            self._width = width
        else:
            raise TypeError("width and height must be integer values")
        
        
    @property      
    def height(self):
        """ int: changes the height of the Lens property """
        return self._height
      
    @height.setter
    def height(self, value):
        """ int: changes height of the lens  
        
        Raises:
            TypeError: height must be an integer value
        """
        if  type (value) == int:
            self._height = value
        else:
            raise TypeError("height must be an integer value")
        


    @property      
    def width(self):
        """ int: width of the sensor property"""
        return self._width
      
    @width.setter    
    def width(self, value):
        """ int: changes width of the lens  
        
        Raises:
            TypeError: width must be an integer value
        """
        if  type (value) == int:
            self._width = value
        else:
            raise TypeError("width must be an integer value")
        

    def process(self,image):
        """ Validates that the shape of the input numpy data matches the Lens
           height and width properties.
       
        Args:
            image: 2D numpy data.

        Returns:
            image if height and width matches the Lens and if the process method is enabled 

        Raises:
            ValueError: Shape of the image does not match the Lens
            ValueError: Process is not enabled
        """
        if (self._enable == True):
            if (np.shape(image) == (self._height,self._width)) :
                return image
            else:
                raise ValueError("Shape of the image does not match the Lens")
        else:
            raise ValueError("Process is not enabled")
            

class Sensor(BaseProcessor):
    """ Sensor class childer of BaseProcessor
        Simple sensor emulator 

    Attributes:
        gain (int): digital camera setting that controls the amplification of the signal from the emulated camera sensor
        
    """
    def __init__(self,gain= 1):
        """__Init__ method for the Sensor class.
                inherits BaseProcessor properties.
            Args:
            gain (int): initial value for the emulated camera sensor gain
        """
        super().__init__()
        if  type (gain) == int:
            self._gain = gain
        else:
            raise TypeError("Gain must be an integer value")
        
    @property      
    def gain(self):
        """ int: gain of the sensor property """
        return self._gain
      
    @gain.setter
    def gain(self, value):
        """ int: changes gain of the sensor 
        
        Raises:
            TypeError: Gain must be an integer value
        """
        if  type (value) == int:
            self._gain = value
        else:
            raise TypeError("Gain must be an integer value")

    def process(self,image):
        """ apply the gain to the image
       
        Args:
            image: 2D numpy data.

        Returns:
            image*gain if the process method is enabled 

        Raises:
            ValueError: Process is not enabled
        """

        if (self._enable == True):            
            return np.multiply(image, self._gain)

        else:
            raise ValueError("Process is not enabled")






# x = np.array([[1, 2, 3], [4, 5, 6]], np.int32)


# processor = BaseProcessor()
# processor.enable = False
# print("processor",processor.enable)

# lens = Lens(2,4)
# lens.enable = False
# lens.enable = True
# print(lens.process(x))

# sensor = Sensor(2)
# print(sensor.process(x))
