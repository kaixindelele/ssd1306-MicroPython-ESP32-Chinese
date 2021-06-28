import machine
import time
import utime
"""
滑动平均并校准：https://www.mfitzp.com/tutorials/3-axis-gyro-micropython/
3D透视：https://www.mfitzp.com/invent/gyroscopic-wireframe-cube/
"""


class Accel():
    def __init__(self, i2c, addr=0x68):
        self.iic = i2c
        self.addr = addr
        self.iic.start()
        self.iic.writeto(self.addr, bytearray([107, 0]))
        self.iic.stop()
        self.file_path = 'mpu6050.txt'

    def get_raw_values(self):
        self.iic.start()
        a = self.iic.readfrom_mem(self.addr, 0x3B, 14)
        self.iic.stop()
        return a

    def get_ints(self):
        b = self.get_raw_values()
        c = []
        for i in b:
            c.append(i)
        return c

    def bytes_toint(self, firstbyte, secondbyte):
        if not firstbyte & 0x80:
            return firstbyte << 8 | secondbyte
        return - (((firstbyte ^ 255) << 8) | (secondbyte ^ 255) + 1)

    def get_values(self):
        raw_ints = self.get_raw_values()
        vals = {}
#         vals["AcX"] = self.bytes_toint(raw_ints[0], raw_ints[1])
        vals["AcY"] = self.bytes_toint(raw_ints[2], raw_ints[3])
        vals["AcZ"] = self.bytes_toint(raw_ints[4], raw_ints[5])
#         vals["Tmp"] = self.bytes_toint(raw_ints[6], raw_ints[7]) / 340.00 + 36.53
#         vals["GyX"] = self.bytes_toint(raw_ints[8], raw_ints[9])
#         vals["GyY"] = self.bytes_toint(raw_ints[10], raw_ints[11])
#         vals["GyZ"] = self.bytes_toint(raw_ints[12], raw_ints[13])
        return vals  # returned in range of Int16
        # -32768 to 32767
        
    def get_smoothed_values(self, n_samples=2):
        """
        Get smoothed values from the sensor by sampling
        the sensor `n_samples` times and returning the mean.
        """
        result = {}
        for _ in range(n_samples):
            data = self.get_values()
            for k in data.keys():
                # Add on value / n_samples (to generate an average)
                # with default of 0 for first loop.
                result[k] = result.get(k, 0) + (data[k] / n_samples)

        return result
    
    def get_average(self, data_list):
        pass
    
    def get_accel(self, n_samples=10, calibration=None):
        # Setup a dict of measure at 0
        result = {}
        for _ in range(n_samples):
            v = self.get_values()

            for m in v.keys():
                # Add on value / n_samples (to generate an average)
                result[m] = result.get(m, 0) + v[m] / n_samples

        if calibration:
            # Remove calibration adjustment
            for m in calibration.keys():
                result[m] -= calibration[m]

        return result
    
    def calibrate(self, threshold=50):
        print('Calibrating...', end='')
        while True:
            v1 = self.get_accel(100)
            v2 = self.get_accel(100)
            if all(abs(v1[m] - v2[m]) < threshold for m in v1.keys()):
                print('Done.')
                return v1

    def val_test(self):  # ONLY FOR TESTING! Also, fast reading sometimes crashes IIC
        from time import sleep
        value = self.calibrate()
        self.cal_z = value['AcZ']
        self.cal_y = value['AcY']
        print("calibrate_value:", value)
        data_list = []        
        for i in range(1000):
            
            data = self.get_smoothed_values()
            
            data_list.append(data)
#             sleep(0.05)
            if i % 1 == 0 and i > 0:
                for data in data_list:
                    st = utime.ticks_ms()
                    self.save2local(data['AcZ'])
                    print(i,
                          "time:", (utime.ticks_ms()-st)/1000.0,                  
                          data['AcZ']-self.cal_z,
                          data['AcY']-self.cal_y)                        
                del data_list
                data_list = []
            
    def save2local(self, data):
#         if type(string) is not str:
#             string = str(string)
        with open(self.file_path, 'a+') as file:
            file.write('%s\n'%(data))


def main():
    from machine import I2C,Pin
    i2c = I2C(scl=Pin(17), sda=Pin(16))
    accel = Accel(i2c)
    accel.val_test()
    
    
if __name__=="__main__":
    main()

