class DataPoint:
    """class representing a point of data acquired by the air. This includes both
    raw and scaled data as well as unscaled accelerometer values.
    """
    raw:int
    scaled:float
    x:int
    y:int
    z:int

    def __init__(self, raw_data : bytearray) -> None:
        """Create a new point from raw data received by the Sniff Controller Air

        Args:
            raw_data (bytearray): byte array received from the air via BLE
        """
        self.raw = int.from_bytes(raw_data[0:2],"little",signed=True)
        self.scaled = self.raw/60 # this is the scale factor of the Air
        self.x = int.from_bytes(raw_data[2:4],"little",signed=True)
        self.y = int.from_bytes(raw_data[4:6],"little",signed=True)
        self.z = int.from_bytes(raw_data[6:8],"little",signed=True)
    

    def __str__(self):
        """String representation of a point. Does not print the raw data only the scaled.

        Returns:
            str: String representation
        """
        return f"pressure: {self.scaled}, acceleration: {self.x},{self.y},{self.z}"
