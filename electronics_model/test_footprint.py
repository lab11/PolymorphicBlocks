import unittest

import edgir
from edg_core import *
from . import *


class TestBlock(FootprintBlock):
  def __init__(self) -> None:
    super().__init__()

    self.port_1 = self.Port(VoltageSink())
    self.port_2 = self.Port(VoltageSink())

  def contents(self) -> None:
    super().contents()
    self.footprint(
      'R', 'Resistor_SMD:R_0603_1608Metric',
      {
        '1': self.port_1,
        '2': self.port_2
      },
      value='1k'
    )


class FootprintTestCase(unittest.TestCase):
  def setUp(self):
    self.pb = TestBlock()._elaborated_def_to_proto()

  def test_footprint(self):
    self.assertIn(edgir.AssignLit(['footprint_name'], 'Resistor_SMD:R_0603_1608Metric'),
                  self.pb.constraints.values())
    self.assertIn(edgir.AssignLit(['value'], '1k'),
                  self.pb.constraints.values())
    self.assertIn(edgir.AssignLit(['refdes_prefix'], 'R'),
                  self.pb.constraints.values())

    expected_pinning = edgir.Metadata()
    path = edgir.ValueExpr()
    path.ref.steps.add().name = 'port_1'
    expected_pinning.members.node['1'].bin_leaf = path.SerializeToString()
    path = edgir.ValueExpr()
    path.ref.steps.add().name = 'port_2'
    expected_pinning.members.node['2'].bin_leaf = path.SerializeToString()
    self.assertEqual(self.pb.meta.members.node['pinning'], expected_pinning)
