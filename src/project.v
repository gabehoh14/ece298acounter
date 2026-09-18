`default_nettype none

module tt_um_example (
    input  wire [7:0] ui_in,    // Dedicated inputs
    output wire [7:0] uo_out,   // Dedicated outputs
    input  wire [7:0] uio_in,   // Bidirectional pins: Input path
    output wire [7:0] uio_out,  // Bidirectional pins: Output path
    output wire [7:0] uio_oe,   // Bidirectional pins: Enable path
    input  wire       ena,      // Will be driven high when project is active
    input  wire       clk,      // Clock signal
    input  wire       rst_n     // Active-low reset
);

  // Set unused bidirectional output/enable channels to 0
  assign uio_out = 8'b0000_0000;
  assign uio_oe  = 8'b0000_0000;

  // Instantiate your 8-bit counter module
  counter my_counter (
      .clk       (clk),         // Connect system clock
      .rst_n     (rst_n),       // Connect active-low reset
      .load      (uio_in[0]),   // Map uio_in[0] to synchronous load
      .oe        (uio_in[1]),   // Map uio_in[1] to tri-state output enable
      .d_in      (ui_in),       // Map ui_in[7:0] to 8-bit parallel load input
      .count_out (uo_out)       // Map uo_out[7:0] to 8-bit count output
  );

  // Tie off unused inputs to suppress OpenLane linter warnings
  wire _unused = &{ena, uio_in[7:2], 1'b0};

endmodule