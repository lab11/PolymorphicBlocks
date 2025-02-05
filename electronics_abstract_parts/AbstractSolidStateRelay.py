from electronics_model import *
from .DummyDevices import MergedAnalogSource
from .AbstractPassives import Resistor


@abstract_block
class SolidStateRelay(Block):
  """Base class for solid state relays.
  LED pins are passive (like the abstract LED) and the enclosing class should provide
  the circuitry to make it a DigitalSink port.
  """
  def __init__(self) -> None:
    super().__init__()

    self.leda = self.Port(Passive())
    self.ledk = self.Port(Passive())

    self.feta = self.Port(Passive())
    self.fetb = self.Port(Passive())

    # TODO: this is a different way of modeling parts - parameters in the part itself
    # instead of on the ports (because this doesn't have typed ports)
    self.led_forward_voltage = self.Parameter(RangeExpr())
    self.led_current_limit = self.Parameter(RangeExpr())
    self.led_current_recommendation = self.Parameter(RangeExpr())
    self.load_voltage_limit = self.Parameter(RangeExpr())
    self.load_current_limit = self.Parameter(RangeExpr())
    self.load_resistance = self.Parameter(RangeExpr())


class DigitalAnalogIsolatedSwitch(Block):
  """Digitally controlled solid state relay that switches an analog signal.
  Includes a ballasting resistor.

  The ports are not tagged with Input/Output/InOut, because of potential for confusion between
  the digital side and the analog side
  """
  def __init__(self) -> None:
    super().__init__()

    self.signal = self.Port(DigitalSink())
    self.gnd = self.Port(Ground(), [Common])

    self.apull = self.Port(AnalogSink())
    self.ain = self.Port(AnalogSink())
    self.aout = self.Port(AnalogSource())

    self.ic = self.Block(SolidStateRelay())
    self.res = self.Block(Resistor(
      resistance=(self.signal.link().voltage.upper() / self.ic.led_current_recommendation.upper(),
                  self.signal.link().output_thresholds.upper() / self.ic.led_current_recommendation.lower())
    ))
    self.connect(self.signal, self.ic.leda.as_digital_sink(
      current_draw=self.signal.link().voltage / self.res.resistance
    ))
    self.connect(self.res.a, self.ic.ledk)
    self.connect(self.res.b.as_ground(), self.gnd)

    self.connect(self.ain, self.ic.feta.as_analog_sink(
      voltage_limits=self.apull.link().voltage + self.ic.load_voltage_limit,
      impedance=self.aout.link().sink_impedance + self.ic.load_resistance
    ))
    self.pull_merge = MergedAnalogSource.merge(
      self, self.apull,
      self.ic.fetb.as_analog_source(
        voltage_out=self.ain.link().voltage,
        current_limits=self.ic.load_current_limit,
        impedance=self.ain.link().source_impedance + self.ic.load_resistance
    ))
    self.connect(self.pull_merge.source, self.aout)
