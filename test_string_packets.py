"""Verify protocol word packing without importing the GUI or accessing hardware."""
import ast
from pathlib import Path
import unittest

source = ast.parse(Path(__file__).with_name('dcsBiosDebug.py').read_text())
window = next(n for n in source.body if isinstance(n, ast.ClassDef) and n.name == 'DCSDebugWindow')
method = next(n for n in window.body if isinstance(n, ast.FunctionDef) and n.name == 'packStringWords')
cls = ast.ClassDef(name='PackingOnly', bases=[], keywords=[], body=[method, next(n for n in window.body if isinstance(n, ast.FunctionDef) and n.name == 'sendArc210Master')], decorator_list=[])
namespace = {}
exec(compile(ast.fix_missing_locations(ast.Module(body=[cls], type_ignores=[])), '<packet-packing>', 'exec'), namespace)

class StringPacketTests(unittest.TestCase):
    def setUp(self):
        self.packer = namespace['PackingOnly']()
        self.packer.dcsBiosValues = {0x1322: 0x6800}

    def test_rt_preserves_master_and_secondary(self):
        self.assertEqual(self.packer.packStringWords(0x1320, b'RT '), bytes.fromhex('2013040052542068'))
        self.assertEqual(self.packer.dcsBiosValues[0x1322], 0x6820)

    def test_frequency_seven_bytes_preserves_adjacent_byte(self):
        self.packer.dcsBiosValues[0x1388] = 0xab00
        packet = self.packer.packStringWords(0x1382, b'133.123')
        self.assertEqual(packet, bytes.fromhex('82130800') + b'133.123' + b'\xab')

    def test_single_byte_preserves_other_half(self):
        self.assertEqual(self.packer.packStringWords(0x1322, b'X'), bytes.fromhex('221302005868'))

    def test_odd_start_preserves_preceding_byte(self):
        self.packer.dcsBiosValues[0x1400] = 0x005a
        self.assertEqual(self.packer.packStringWords(0x1401, b'A'), bytes.fromhex('001402005a41'))


class MasterPowerTests(unittest.TestCase):
    def test_off_then_on_sends_display_power_and_preserves_secondary(self):
        from types import SimpleNamespace
        bridge = namespace['PackingOnly']()
        bridge.dcsBiosValues = {0x1322: 0x6820}
        bridge.arc210MasterModes = ['0 - OFF', '1 - TR-G', '2 - TR']
        bridge.statusBar = SimpleNamespace(set=lambda *args: None)
        selected = ['0 - OFF']
        bridge.arc210MasterMode = SimpleNamespace(get=lambda: selected[0])
        sent = []
        def send_string(address, value, length, label):
            sent.append(('RT', value))
            bridge.packStringWords(address, value.encode().ljust(length, b' '))
            return True
        def send_word(address, value, label):
            sent.append(('MASTER', value))
            bridge.dcsBiosValues[address] = value
            return True
        bridge._sendDirectString = send_string
        bridge._sendDirectWord = send_word
        bridge.sendArc210Master()
        selected[0] = '1 - TR-G'
        bridge.sendArc210Master()
        selected[0] = '2 - TR'
        bridge.sendArc210Master()
        self.assertEqual(sent, [('RT', ''), ('MASTER', 0x6020),
                               ('RT', 'RT'), ('MASTER', 0x6420),
                               ('RT', 'RT'), ('MASTER', 0x6820)])
        self.assertEqual(bridge.dcsBiosValues[0x1320], 0x5452)

    def test_failed_display_power_send_stops_master_send(self):
        from types import SimpleNamespace
        bridge = namespace['PackingOnly']()
        bridge.arc210MasterModes = ['0 - OFF', '2 - TR']
        bridge.arc210MasterMode = SimpleNamespace(get=lambda: '2 - TR')
        bridge._sendDirectString = lambda *args: False
        bridge._sendDirectWord = lambda *args: self.fail('MASTER sent after failed RT send')
        bridge.sendArc210Master()

if __name__ == '__main__':
    unittest.main()
