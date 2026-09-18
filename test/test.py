import cocotb
from cocotb.clock import Clock
from cocotb.triggers import ClockCycles, FallingEdge, RisingEdge

@cocotb.test()
async def test_project(dut):
    dut._log.info("Start counter test")

    # Set up a 10 us clock (100 kHz)
    clock = Clock(dut.clk, 10, units="us")
    cocotb.start_soon(clock.start())

    # Reset state
    dut._log.info("Applying reset")
    dut.ena.value = 1
    dut.ui_in.value = 0
    dut.uio_in.value = 0  # load=0, oe=0
    dut.rst_n.value = 0
    await ClockCycles(dut.clk, 2)
    dut.rst_n.value = 1
    await ClockCycles(dut.clk, 1)

    # 1. Enable Output Drive (uio_in[1] = 1 -> oe=1)
    dut.uio_in.value = 0b00000010  # oe = 1, load = 0
    await ClockCycles(dut.clk, 1)

    # Verify output resets to 0
    assert int(dut.uo_out.value) == 0, f"Expected 0 after reset, got {dut.uo_out.value}"

    # 2. Test Counting (increment for 5 clock cycles)
    await ClockCycles(dut.clk, 5)
    assert int(dut.uo_out.value) == 5, f"Expected count 5, got {dut.uo_out.value}"

    # 3. Test Synchronous Load (uio_in[0] = 1 -> load=1, ui_in = 0xA5)
    dut.ui_in.value = 0xA5
    dut.uio_in.value = 0b00000011  # oe = 1, load = 1
    await ClockCycles(dut.clk, 1)
    
    # Disable load and let it count from 0xA5
    dut.uio_in.value = 0b00000010  # load = 0, oe = 1
    assert int(dut.uo_out.value) == 0xA5, f"Expected 0xA5 (165), got {dut.uo_out.value}"

    # 4. Count up from loaded value
    await ClockCycles(dut.clk, 1)
    assert int(dut.uo_out.value) == 0xA6, f"Expected 0xA6 (166), got {dut.uo_out.value}"

    dut._log.info("All counter tests passed!")