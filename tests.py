import unittest
from unittest.mock import patch

import network
from infoports import InfoPorts

class TestNetwork(unittest.TestCase):
    
    def test_subnet_for_ip(self):
        self.assertEqual(network.subnet_from_ip('192.168.1.22/24'), '192.168.1.0')
        self.assertEqual(network.subnet_from_ip('10.8.12.123/20'), '10.8.0.0')
        
    def test_ip_list_from_subnet(self):
        ip_list = network.ip_list_from_subnet('192.168.1.0/24')
        self.assertEqual(len(ip_list), 254)
        
    def test_port_is_open(self):
        # Mock la classe InfoPorts
        with patch('infoports.InfoPorts', autospec=True) as MockInfoPorts:
            iports_instance = MockInfoPorts.return_value

            # Simule l'appel à description_for
            iports_instance.description_for.return_value = "Service Test"
            
            # Exécute la fonction avec un port ouvert
            with patch('socket.socket') as mock_socket:
                mock_socket.return_value.connect.return_value = None
                mock_socket.return_value.settimeout.return_value = None
                mock_socket.return_value.close.return_value = None
                
                result = network.port_is_open("127.0.0.1", 80, display_result=True)
                
                self.assertTrue(result)  # Vérifiez que le résultat est True

                # Vérifiez si description_for a été appelée
                iports_instance.description_for.assert_called_with(80)

                # Vérifiez si l'impression a eu lieu
                self.assertEqual(
                    mock_socket.return_value.connect.call_args[0][0], 
                    ("127.0.0.1", 80)
                )
        
class TestInfoPorts(unittest.TestCase):
        
        def test_load(self):
            iports = InfoPorts()
            self.assertEqual(len(iports._ports), 1096)
            
        def test_description_for(self):
            iports = InfoPorts()
            self.assertEqual(iports.description_for(80), "Hypertext Transfer Protocol (HTTP)")
            self.assertEqual(iports.description_for(443), "Hypertext Transfer Protocol over TLS/SSL (HTTPS)")
            self.assertEqual(iports.description_for(1), "TCP Port Service Multiplexer (TCPMUX)")
            self.assertEqual(iports.description_for(8000), "iRDMI (Intel Remote Desktop Management Interface)[92]\u00e2\u20ac\u201dsometimes erroneously used instead of port 8080")
            self.assertEqual(iports.description_for(65535), "Unknown")