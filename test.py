# pylint: disable=protected-access

import unittest
from unittest.mock import MagicMock, patch
from GP8XXX_IIC import GP8503, GP8211S, GP8512, GP8413, GP8403, GP8302


class TestGP8XXX(unittest.TestCase):
    """
    Test cases for GP8XXX classes.
    """

    def setUp(self):
        self.mock_i2c = MagicMock()
        self.mock_i2c.read_byte.return_value = 0
        self.mock_i2c.read_byte_data.return_value = 0
        self.mock_i2c.read_word_data.return_value = 0
        self.mock_i2c.write_byte_data.return_value = None
        self.mock_i2c.write_word_data.return_value = None

    @patch('GP8XXX_IIC.SMBus')
    def test_gp8503(self, mock_smbus):
        """
        Test GP8503 functionality.

        This test verifies the functionality of the GP8503 class,
        including initialization and setting DAC output voltage.
        """
        mock_smbus.return_value = self.mock_i2c
        gp8503 = GP8503()
        gp8503._i2c = self.mock_i2c

        gp8503.begin()
        self.mock_i2c.read_byte.assert_called_once_with(gp8503._device_addr)

        gp8503.set_dac_out_voltage(2.0, 0)
        self.assertEqual(gp8503.channel0['value'], 2000)
        self.assertEqual(gp8503.channel0['dac_voltage'], 2500)

        gp8503.set_dac_out_voltage(0.167, 0)
        self.assertEqual(gp8503.channel0['value'], 167)
        self.assertEqual(gp8503.channel0['dac_voltage'], 2500)

        gp8503.set_dac_out_voltage(9.8, 0)
        self.assertEqual(gp8503.channel0['value'], 2500)
        self.assertEqual(gp8503.channel0['dac_voltage'], 2500)

        self.assertEqual(gp8503.channel1['value'], 0)
        self.assertEqual(gp8503.channel1['dac_voltage'], 2500)

        gp8503.set_dac_out_voltage(1.8, 1)
        self.assertEqual(gp8503.channel1['value'], 1800)
        self.assertEqual(gp8503.channel1['dac_voltage'], 2500)

        with self.assertRaises(ValueError) as context:
            gp8503.set_dac_outrange(gp8503.OUTPUT_RANGE_10V)
            self.assertEqual(str(context.exception),
                             "DAC does't support another output range.")

    @patch('GP8XXX_IIC.SMBus')
    def test_gp8211s(self, mock_smbus):
        """
        Test GP8211S functionality.

        This test verifies the functionality of the GP8211S class,
        including initialization and setting DAC output voltage.
        """
        mock_smbus.return_value = self.mock_i2c
        gp8211s = GP8211S()
        gp8211s._i2c = self.mock_i2c

        gp8211s.begin()
        self.mock_i2c.read_byte.assert_called_once_with(gp8211s._device_addr)

        gp8211s.set_dac_outrange(gp8211s.OUTPUT_RANGE_10V)
        self.assertEqual(gp8211s._dac_voltage, 10000)

        gp8211s.set_dac_outrange(gp8211s.OUTPUT_RANGE_5V)
        self.assertEqual(gp8211s._dac_voltage, 5000)

        gp8211s.set_dac_out_voltage(3.5, 0)
        self.assertEqual(gp8211s.channel0['value'], 3500)
        self.assertTrue(gp8211s.channel0['dac_voltage'], 5000)

        gp8211s.set_dac_out_voltage(9.5, 0)
        self.assertEqual(gp8211s.channel0['value'], 9500)
        self.assertTrue(gp8211s.channel0['dac_voltage'], 10000)

        with self.assertRaises(ValueError) as context:
            gp8211s.set_dac_out_voltage(3.5, 1)
            self.assertEqual(str(context.exception),
                             "Unsupported channel. The DAC only supports channel 0.")

    @patch('GP8XXX_IIC.SMBus')
    def test_gp8512(self, mock_smbus):
        """
        Test GP8512 functionality.

        This test verifies the functionality of the GP8512 class,
        including initialization and setting DAC output voltage.
        """
        mock_smbus.return_value = self.mock_i2c
        gp8512 = GP8512()
        gp8512._i2c = self.mock_i2c

        gp8512.begin()
        self.mock_i2c.read_byte.assert_called_once_with(gp8512._device_addr)

        gp8512.set_dac_out_voltage(2.0, 0)
        self.assertEqual(gp8512.channel0['value'], 2000)
        self.assertEqual(gp8512.channel0['dac_voltage'], 2500)

        gp8512.set_dac_out_voltage(0.167, 0)
        self.assertEqual(gp8512.channel0['value'], 167)
        self.assertEqual(gp8512.channel0['dac_voltage'], 2500)

        gp8512.set_dac_out_voltage(9.8, 0)
        self.assertEqual(gp8512.channel0['value'], 2500)
        self.assertEqual(gp8512.channel0['dac_voltage'], 2500)

        self.assertEqual(gp8512.channel1['value'], 0)
        self.assertEqual(gp8512.channel1['dac_voltage'], 2500)

        with self.assertRaises(ValueError) as context:
            gp8512.set_dac_out_voltage(1.8, 1)
        self.assertEqual(str(context.exception),
                         "Unsupported channel. The DAC only supports channel 0.")

        with self.assertRaises(ValueError) as context:
            gp8512.set_dac_outrange(gp8512.OUTPUT_RANGE_5V)
            self.assertEqual(str(context.exception),
                             "DAC does't support another output range.")
    
    @patch('GP8XXX_IIC.SMBus')
    def test_gp8413(self, mock_smbus):
        """
        Test GP8413 functionality.

        This test verifies the functionality of the GP8413 class,
        including initialization and setting DAC output voltage.
        """
        mock_smbus.return_value = self.mock_i2c
        gp8413 = GP8413(bus=1, i2c_addr=0)
        gp8413._i2c = self.mock_i2c

        self.mock_i2c.read_byte.return_value = 0

        gp8413.begin()
        self.mock_i2c.read_byte.assert_called_once_with(gp8413._device_addr)

        # Test setting output voltage on channel 0
        gp8413.set_dac_out_voltage(3.5, 0)
        self.assertEqual(gp8413.channel0['value'], 3500)
        self.assertEqual(gp8413.channel0['dac_voltage'], 10000)

        with self.assertRaises(ValueError) as context:
            gp8413.set_dac_outrange(gp8413.OUTPUT_RANGE_5V)
            self.assertEqual(str(context.exception),
                             "DAC does't support another output range.")


    @patch('GP8XXX_IIC.SMBus')
    def test_gp8403(self, mock_smbus):
        """
        Test GP8403 functionality.

        This test verifies the functionality of the GP8403 class,
        including initialization and setting DAC output voltage.
        """
        mock_smbus.return_value = self.mock_i2c
        gp8403 = GP8403()
        gp8403._i2c = self.mock_i2c

        gp8403.begin()
        self.mock_i2c.read_byte.assert_called_once_with(gp8403._device_addr)

        gp8403.set_dac_outrange(gp8403.OUTPUT_RANGE_10V)
        self.assertEqual(gp8403._dac_voltage, 10000)

        gp8403.set_dac_outrange(gp8403.OUTPUT_RANGE_5V)
        self.assertEqual(gp8403._dac_voltage, 5000)

        gp8403.set_dac_out_voltage(2.0, 0)
        self.assertEqual(gp8403.channel0['value'], 2000)
        self.assertEqual(gp8403.channel0['dac_voltage'], 5000)

        gp8403.set_dac_out_voltage(0.167, 0)
        self.assertEqual(gp8403.channel0['value'], 167)
        self.assertEqual(gp8403.channel0['dac_voltage'], 5000)

        gp8403.set_dac_out_voltage(5.01, 0)
        self.assertEqual(gp8403.channel0['value'], 5010)
        self.assertEqual(gp8403.channel0['dac_voltage'], 10000)

        self.assertEqual(gp8403.channel1['value'], 0)
        self.assertEqual(gp8403.channel1['dac_voltage'], 10000)

    @patch('GP8XXX_IIC.SMBus')
    def test_gp8302(self, mock_smbus):
        """
        Test GP8302 functionality.

        This test verifies the functionality of the GP8302 class,
        including initialization and setting DAC output voltage.
        """
        mock_smbus.return_value = self.mock_i2c
        gp8302 = GP8302()
        gp8302._i2c = self.mock_i2c

        gp8302.begin()
        self.mock_i2c.read_byte.assert_called_once_with(gp8302._device_addr)

        gp8302.set_dac_outrange(gp8302.OUTPUT_RANGE_10V)
        self.assertEqual(gp8302._dac_voltage, 10000)

        gp8302.set_dac_outrange(gp8302.OUTPUT_RANGE_5V)
        self.assertEqual(gp8302._dac_voltage, 5000)

        gp8302.set_dac_out_voltage(2.0, 0)
        self.assertEqual(gp8302.channel0['value'], 2000)
        self.assertEqual(gp8302.channel0['dac_voltage'], 5000)

        gp8302.set_dac_out_voltage(0.167, 0)
        self.assertEqual(gp8302.channel0['value'], 167)
        self.assertEqual(gp8302.channel0['dac_voltage'], 5000)

        value = 7.8321
        expected_channel_value = float(value * 1000)
        gp8302.set_dac_out_voltage(value, 1)
        self.assertEqual(gp8302.channel1['value'], expected_channel_value)
        self.assertEqual(gp8302.channel1['dac_voltage'], 10000)

        gp8302.set_dac_out_voltage(0, 1)
        self.assertEqual(gp8302.channel1['value'], 0)
        self.assertEqual(gp8302.channel1['dac_voltage'], 5000)


if __name__ == '__main__':
    unittest.main()
