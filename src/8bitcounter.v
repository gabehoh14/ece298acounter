`default_nettype none

module counter (
    input  wire       clk,        // Clock signal
    input  wire       rst_n,      // Asynchronous active-low reset
    input  wire       load,       // Synchronous load enable
    input  wire       oe,         // Output enable for tri-state control
    input  wire [7:0] d_in,       // 8-bit parallel load data input
    output wire [7:0] count_out   // 8-bit tri-state count output
);

    reg [7:0] count_reg;

    // Asynchronous Reset & Synchronous Counter/Load
    always @(posedge clk or negedge rst_n) begin
        if (!rst_n) begin
            count_reg <= 8'h00;
        end else if (load) begin
            count_reg <= d_in;
        end else begin
            count_reg <= count_reg + 1'b1;
        end
    end

    // Tri-State Output Driver
    assign count_out = oe ? count_reg : 8'bzzzz_zzzz;

endmodule