from __future__ import annotations

from math import log10, ceil
from typing import List, Tuple

from edg_core import *
from electronics_model import Common, Passive
from . import AnalogFilter, DiscreteApplication, Resistor, Filter
from .ESeriesUtil import ESeriesUtil, ESeriesRatioUtil, ESeriesRatioValue


class DividerValues(ESeriesRatioValue['DividerValues']):
  """Resistive divider calculator using the ESeriesRatioUtil infrastructure.

  R1 is the high-side resistor, and R2 is the low-side resistor, such that
  Vout = Vin * R2 / (R1 + R2)

  Example of decade adjustment:
  R1 : R2   maxR2/minR1  minR2/maxR1  (theoretical)
  1  : 10   100/101      10/20        /\ ratio towards 1
  1  : 1    10/11        1/11
  10 : 1    10/20        1/101
  100: 1    10/110       1/1001       \/ ratio towards 0
  """
  def __init__(self, ratio: Range, parallel_impedance: Range):
    self.ratio = ratio  # amplification factor from in to out
    self.parallel_impedance = parallel_impedance  # parallel impedance into the opamp negative pin

  @staticmethod
  def from_resistors(r1_range: Range, r2_range: Range) -> 'DividerValues':
    """This uses a slight rewriting of terms to avoid duplication of terms and not double-count tolerances:
    ratio = R2 / (R1 + R2) => divide  through by R2 / R2
    ratio = 1 / (R1 / R2 + 1)
    """
    return DividerValues(
      1 / (r1_range / r2_range + 1),
      1 / (1 / r1_range + 1 / r2_range)
    )

  def initial_test_decades(self) -> Tuple[int, int]:
    decade = ceil(log10(self.parallel_impedance.center()))
    return decade, decade

  def distance_to(self, spec: 'DividerValues') -> List[float]:
    if self.ratio in spec.ratio and self.parallel_impedance in spec.parallel_impedance:
      return []
    else:
      return [
        abs(self.ratio.center() - spec.ratio.center()),
        abs(self.parallel_impedance.center() - spec.parallel_impedance.center())
      ]

  def intersects(self, spec: 'DividerValues') -> bool:
    return self.ratio.intersects(spec.ratio) and \
           self.parallel_impedance.intersects(spec.parallel_impedance)


class ResistiveDivider(DiscreteApplication, GeneratorBlock):
  """Abstract, untyped (Passive) resistive divider, that takes in a ratio and parallel impedance spec."""

  @init_in_parent
  def __init__(self, ratio: RangeLike = RangeExpr(), impedance: RangeLike = RangeExpr()) -> None:
    super().__init__()

    self.ratio = self.Parameter(RangeExpr(ratio))
    self.impedance = self.Parameter(RangeExpr(impedance))

    self.series = self.Parameter(IntExpr(24))  # can be overridden by refinements
    self.tolerance = self.Parameter(FloatExpr(0.01))  # can be overridden by refinements

    self.selected_ratio = self.Parameter(RangeExpr())
    self.selected_impedance = self.Parameter(RangeExpr())
    self.selected_series_impedance = self.Parameter(RangeExpr())

    self.top = self.Port(Passive())
    self.center = self.Port(Passive())
    self.bottom = self.Port(Passive())

    self.generator(self.generate_divider, self.ratio, self.impedance, self.series, self.tolerance)

  def generate_divider(self, ratio: Range, impedance: Range, series: int, tolerance: float) -> None:
    """Generates a resistive divider meeting the required specifications, with the lowest E-series resistors possible.
    """

    # TODO: not fully optimal in that the ratio doesn't need to be recalculated if we're shifting both decades
    # (to achieve some impedance spec), but it uses shared infrastructure that doesn't assume this ratio optimization
    calculator = ESeriesRatioUtil(ESeriesUtil.SERIES[series], tolerance, DividerValues)
    top_resistance, bottom_resistance = calculator.find(DividerValues(ratio, impedance))

    self.top_res = self.Block(Resistor(
      resistance=Range.from_tolerance(top_resistance, tolerance)
    ))
    self.bottom_res = self.Block(Resistor(
      resistance=Range.from_tolerance(bottom_resistance, tolerance)
    ))

    self.connect(self.top_res.a, self.top)
    self.connect(self.top_res.b, self.center, self.bottom_res.a)
    self.connect(self.bottom_res.b, self.bottom)

    self.assign(self.selected_impedance,
                1 / (1/self.top_res.resistance + 1/self.bottom_res.resistance))
    self.assign(self.selected_series_impedance,
                self.top_res.resistance + self.bottom_res.resistance)
    self.assign(self.selected_ratio,
                1 / (self.top_res.resistance / self.bottom_res.resistance + 1))


@abstract_block
class BaseVoltageDivider(Filter, Block):
  """Base class that defines a resistive divider that takes in a voltage source and ground, and outputs
  an analog constant-voltage signal.
  The actual output voltage is defined as a ratio of the input voltage, and the divider is specified by
  ratio and impedance.
  Subclasses should define the ratio and impedance spec."""
  @init_in_parent
  def __init__(self) -> None:
    super().__init__()

    self.ratio = self.Parameter(RangeExpr())
    self.impedance = self.Parameter(RangeExpr())
    self.div = self.Block(ResistiveDivider(ratio=self.ratio, impedance=self.impedance))

    self.input = self.Export(self.div.top.as_voltage_sink(
      current_draw=RangeExpr(),
      voltage_limits=RangeExpr.ALL
    ), [Input])
    self.output = self.Export(self.div.center.as_analog_source(
      voltage_out=(self.input.link().voltage.lower() * self.div.selected_ratio.lower(),
                   self.input.link().voltage.upper() * self.div.selected_ratio.upper()),
      current_limits=RangeExpr.ALL,
      impedance=self.div.selected_impedance
    ), [Output])
    self.gnd = self.Export(self.div.bottom.as_ground(), [Common])

    self.selected_ratio = self.Parameter(RangeExpr(self.div.selected_ratio))
    self.selected_impedance = self.Parameter(RangeExpr(self.div.selected_impedance))
    self.selected_series_impedance = self.Parameter(RangeExpr(self.div.selected_series_impedance))

    self.assign(self.input.current_draw, self.output.link().current_drawn)
    # TODO also model static current draw into gnd


class VoltageDivider(BaseVoltageDivider):
  """Voltage divider that takes in a ratio and parallel impedance spec, and produces an output analog signal
  of the appropriate magnitude (as a fraction of the input voltage)"""
  @init_in_parent
  def __init__(self, *, output_voltage: RangeLike = RangeExpr(),
               impedance: RangeLike = RangeExpr()) -> None:
    super().__init__()

    self.output_voltage = self.Parameter(RangeExpr(output_voltage))  # TODO eliminate this casting?
    self.assign(self.impedance, impedance)

    ratio_lower = self.output_voltage.lower() / self.input.link().voltage.lower()
    ratio_upper = self.output_voltage.upper() / self.input.link().voltage.upper()
    self.require(ratio_lower <= ratio_upper,
                   "can't generate divider to create output voltage of tighter tolerance than input voltage")
    self.assign(self.ratio, (ratio_lower, ratio_upper))


class FeedbackVoltageDivider(BaseVoltageDivider):
  """Voltage divider that takes in a ratio and parallel impedance spec, and produces an output analog signal
  of the appropriate magnitude (as a fraction of the input voltage)"""
  @init_in_parent
  def __init__(self, *, output_voltage: RangeLike = RangeExpr(),
               impedance: RangeLike = RangeExpr(),
               assumed_input_voltage: RangeLike = RangeExpr()) -> None:
    super().__init__()

    self.output_voltage = self.Parameter(RangeExpr(output_voltage))  # TODO eliminate this casting?
    self.assumed_input_voltage = self.Parameter(RangeExpr(assumed_input_voltage))  # TODO eliminate this casting?
    self.assign(self.impedance, impedance)

    ratio_lower = self.output_voltage.upper() / self.assumed_input_voltage.upper()
    ratio_upper = self.output_voltage.lower() / self.assumed_input_voltage.lower()
    self.require(ratio_lower <= ratio_upper,
                   "can't generate feedback divider with input voltage of tighter tolerance than output voltage")
    self.assign(self.ratio, (ratio_lower, ratio_upper))


class SignalDivider(AnalogFilter, Block):
  """Specialization of ResistiveDivider for Analog signals"""
  @init_in_parent
  def __init__(self, ratio: RangeLike = RangeExpr(),
               impedance: RangeLike = RangeExpr()) -> None:
    super().__init__()

    self.div = self.Block(ResistiveDivider(ratio=ratio, impedance=impedance))
    self.input = self.Export(self.div.top.as_analog_sink(
      impedance=self.div.selected_series_impedance,
      current_draw=RangeExpr(),
      voltage_limits=RangeExpr.ALL
    ), [Input])
    self.output = self.Export(self.div.center.as_analog_source(
      voltage_out=(self.input.link().voltage.lower() * self.div.selected_ratio.lower(),
                   self.input.link().voltage.upper() * self.div.selected_ratio.upper()),
      current_limits=RangeExpr.ALL,
      impedance=self.div.selected_impedance
    ), [Output])
    self.gnd = self.Export(self.div.bottom.as_ground(), [Common])
    self.assign(self.input.current_draw, self.output.link().current_drawn)
