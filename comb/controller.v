//=========================================
// Version 1 : RGB2YCBCR, DCT
// Date : 2024/1/6
// Function : control rgb2ycbcr and dct & for testing
//=========================================

// Instruction: you use add more state of FSM to control quan. and huff. 

module controller (
    input clk,
    input rst_n,
    input enable,
    output reg enable_rgb2ycbcr,
    output reg enable_dct,
    output enable_quan,
    input valid_rgb2ycbcr,
    input valid_dct,
    input valid_quan,
    output valid
);

localparam IDLE = 4'd0, RGB2YCBCR = 4'd1, DCT = 4'd2, DONE = 4'd3, QUAN = 4'd4;

reg [3:0] state, nstate;
always @(posedge clk) begin
    if(!rst_n) state <= IDLE;
    else state <= nstate;
end
// for convenient testing, DCT stage -> DCT stage.
// add one more pin done_dct from dct block 
// Edit DCT : nstate = done_dct ? QUAN : DCT;
// add DONE stage to whole system when all blocks are done.
always @* begin
    case(state)
        IDLE : nstate = enable ? RGB2YCBCR : IDLE;
        RGB2YCBCR : nstate = valid_rgb2ycbcr ? DCT : RGB2YCBCR;
        DCT : nstate = valid_dct ? QUAN : DCT;
        // DCT : nstate = DCT;
        QUAN : nstate = QUAN;
        // DONE : nstate = IDLE;
        default : nstate = IDLE;
    endcase
end

// Uncomment valid and redesign it.
// for testing rgb2ycbcr and dct, valid connect to valid_dct. 



always @* begin
    case(state)
        IDLE : begin 
            enable_rgb2ycbcr = 0;
            enable_dct = 0;
            // valid = 0;
        end
        RGB2YCBCR : begin 
            enable_rgb2ycbcr = 1;
            enable_dct = 0;
            // valid = 0;
        end
        DCT : begin 
            enable_rgb2ycbcr = 0;
            enable_dct = 1;
            // valid = 0;
        end
        QUAN : begin
            enable_rgb2ycbcr = 0;
            enable_dct = 1;
            // valid = 0;
        end
        DONE : begin 
            enable_rgb2ycbcr = 0;
            enable_dct = 0;
            // valid = 1;
        end
        default : begin
            enable_rgb2ycbcr = 0;
            enable_dct = 0;
        end
    endcase
end
assign valid = valid_quan;
assign enable_quan = valid_dct;
endmodule