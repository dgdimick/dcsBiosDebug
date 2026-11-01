"""Verify protocol word packing without importing the GUI or accessing hardware."""
import ast
from pathlib import Path
import unittest

source = ast.parse(Path(__file__).with_name('dcsBiosDebug.py').read_text())
window = next(n for n in source.body if isinstance(n, ast.ClassDef) and n.name == 'DCSDebugWindow')
method = next(n for n in window.body if isinstance(n, ast.FunctionDef) and n.name == 'packStringWords')
cls = ast.ClassDef(name='PackingOnly', bases=[], keywords=[], body=[method], decorator_list=[])
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

if __name__ == '__main__':
    unittest.main()
