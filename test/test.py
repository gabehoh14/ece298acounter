import cocotb
from cocotb.clock import Clock
from cocotb.triggers import ClockCycles, FallingEdge, RisingEdge

@cocotb.test()
async def test_project(dut):
    dut._log.info("Start counter test")

    # 100 kHz clock (10 us period)
    clock = Clock(dut.clk, 10, unit="us")
    cocotb.start_soon(clock.start())

    # Initial signal values
    dut.ena.value = 1
    dut.ui_in.value = 0
    dut.uio_in.value = 0b00000010  # oe = 1, load = 0

    # 1. Apply active-low reset
    dut._log.info("Applying reset")
    dut.rst_n.value = 0
    await ClockCycles(dut.clk, 2)
    
    # Release reset on falling edge (prevents rising-edge race condition)
    await FallingEdge(dut.clk)
    dut.rst_n.value = 1

    # Verify reset value (0) during low clock phase before next rising edge
    assert int(dut.uo_out.value) == 0, f"Expected 0 after reset, got {dut.uo_out.value}"

    # 2. Test Counting (5 clock cycles)
    await ClockCycles(dut.clk, 5)
    await FallingEdge(dut.clk)
    assert int(dut.uo_out.value) == 5, f"Expected count 5, got {dut.uo_out.value}"

    # 3. Test Synchronous Load (set load=1 and input=0xA5 on falling edge)
    dut.ui_in.value = 0xA5
    dut.uio_in.value = 0b00000011  # oe = 1, load = 1

    # Clock in the loaded value
    await RisingEdge(dut.clk)
    await FallingEdge(dut.clk)
    
    # Disable load
    dut.uio_in.value = 0b00000010  # oe = 1, load = 0
    assert int(dut.uo_out.value) == 0xA5, f"Expected 0xA5 (165), got {dut.uo_out.value}"

    # 4. Verify incrementing from loaded value (0xA5 -> 0xA6)
    await RisingEdge(dut.clk)
    await FallingEdge(dut.clk)
    assert int(dut.uo_out.value) == 0xA6, f"Expected 0xA6 (166), got {dut.uo_out.value}"

    dut._log.info("All counter tests passed!")