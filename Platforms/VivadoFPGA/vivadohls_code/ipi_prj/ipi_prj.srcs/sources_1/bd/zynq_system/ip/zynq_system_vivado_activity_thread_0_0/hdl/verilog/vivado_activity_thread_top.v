// ==============================================================
// File generated by Vivado(TM) HLS - High-Level Synthesis from C, C++ and SystemC
// Version: 2013.4
// Copyright (C) 2013 Xilinx Inc. All rights reserved.
// 
// ==============================================================

`timescale 1 ns / 1 ps
module vivado_activity_thread_top (
s_axi_CORE_IO_AWADDR,
s_axi_CORE_IO_AWVALID,
s_axi_CORE_IO_AWREADY,
s_axi_CORE_IO_WDATA,
s_axi_CORE_IO_WSTRB,
s_axi_CORE_IO_WVALID,
s_axi_CORE_IO_WREADY,
s_axi_CORE_IO_BRESP,
s_axi_CORE_IO_BVALID,
s_axi_CORE_IO_BREADY,
s_axi_CORE_IO_ARADDR,
s_axi_CORE_IO_ARVALID,
s_axi_CORE_IO_ARREADY,
s_axi_CORE_IO_RDATA,
s_axi_CORE_IO_RRESP,
s_axi_CORE_IO_RVALID,
s_axi_CORE_IO_RREADY,
aresetn,
aclk,
result_0_din,
result_0_full_n,
result_0_write,
ap_start,
ap_ready,
ap_done,
ap_idle
);

parameter C_S_AXI_CORE_IO_ADDR_WIDTH = 7;
parameter C_S_AXI_CORE_IO_DATA_WIDTH = 32;
parameter RESET_ACTIVE_LOW = 1;

input [C_S_AXI_CORE_IO_ADDR_WIDTH - 1:0] s_axi_CORE_IO_AWADDR ;
input s_axi_CORE_IO_AWVALID ;
output s_axi_CORE_IO_AWREADY ;
input [C_S_AXI_CORE_IO_DATA_WIDTH - 1:0] s_axi_CORE_IO_WDATA ;
input [C_S_AXI_CORE_IO_DATA_WIDTH/8 - 1:0] s_axi_CORE_IO_WSTRB ;
input s_axi_CORE_IO_WVALID ;
output s_axi_CORE_IO_WREADY ;
output [2 - 1:0] s_axi_CORE_IO_BRESP ;
output s_axi_CORE_IO_BVALID ;
input s_axi_CORE_IO_BREADY ;
input [C_S_AXI_CORE_IO_ADDR_WIDTH - 1:0] s_axi_CORE_IO_ARADDR ;
input s_axi_CORE_IO_ARVALID ;
output s_axi_CORE_IO_ARREADY ;
output [C_S_AXI_CORE_IO_DATA_WIDTH - 1:0] s_axi_CORE_IO_RDATA ;
output [2 - 1:0] s_axi_CORE_IO_RRESP ;
output s_axi_CORE_IO_RVALID ;
input s_axi_CORE_IO_RREADY ;

input aresetn ;

input aclk ;

output [32 - 1:0] result_0_din ;
input result_0_full_n ;
output result_0_write ;
input ap_start ;
output ap_ready ;
output ap_done ;
output ap_idle ;


wire [C_S_AXI_CORE_IO_ADDR_WIDTH - 1:0] s_axi_CORE_IO_AWADDR;
wire s_axi_CORE_IO_AWVALID;
wire s_axi_CORE_IO_AWREADY;
wire [C_S_AXI_CORE_IO_DATA_WIDTH - 1:0] s_axi_CORE_IO_WDATA;
wire [C_S_AXI_CORE_IO_DATA_WIDTH/8 - 1:0] s_axi_CORE_IO_WSTRB;
wire s_axi_CORE_IO_WVALID;
wire s_axi_CORE_IO_WREADY;
wire [2 - 1:0] s_axi_CORE_IO_BRESP;
wire s_axi_CORE_IO_BVALID;
wire s_axi_CORE_IO_BREADY;
wire [C_S_AXI_CORE_IO_ADDR_WIDTH - 1:0] s_axi_CORE_IO_ARADDR;
wire s_axi_CORE_IO_ARVALID;
wire s_axi_CORE_IO_ARREADY;
wire [C_S_AXI_CORE_IO_DATA_WIDTH - 1:0] s_axi_CORE_IO_RDATA;
wire [2 - 1:0] s_axi_CORE_IO_RRESP;
wire s_axi_CORE_IO_RVALID;
wire s_axi_CORE_IO_RREADY;

wire aresetn;


wire [32 - 1:0] sig_vivado_activity_thread_kernel_arg_u_a_0_rfir;
wire [32 - 1:0] sig_vivado_activity_thread_kernel_arg_u_a_0_current_price;
wire [32 - 1:0] sig_vivado_activity_thread_kernel_arg_u_v_0_gamma;
wire sig_vivado_activity_thread_kernel_arg_u_v_0_gamma_ap_vld;
wire [32 - 1:0] sig_vivado_activity_thread_kernel_arg_u_v_0_time;
wire sig_vivado_activity_thread_kernel_arg_u_v_0_time_ap_vld;
wire [32 - 1:0] sig_vivado_activity_thread_kernel_arg_o_a_0_strike_price;
wire [32 - 1:0] sig_vivado_activity_thread_kernel_arg_o_a_0_time_period;
wire [32 - 1:0] sig_vivado_activity_thread_kernel_arg_o_a_0_call;
wire [32 - 1:0] sig_vivado_activity_thread_kernel_arg_o_v_0_delta_time;
wire [32 - 1:0] sig_vivado_activity_thread_kernel_arg_o_v_0_value;
wire sig_vivado_activity_thread_kernel_arg_o_v_0_value_ap_vld;

wire sig_vivado_activity_thread_ap_rst;



vivado_activity_thread vivado_activity_thread_U(
    .kernel_arg_u_a_0_rfir(sig_vivado_activity_thread_kernel_arg_u_a_0_rfir),
    .kernel_arg_u_a_0_current_price(sig_vivado_activity_thread_kernel_arg_u_a_0_current_price),
    .kernel_arg_u_v_0_gamma(sig_vivado_activity_thread_kernel_arg_u_v_0_gamma),
    .kernel_arg_u_v_0_gamma_ap_vld(sig_vivado_activity_thread_kernel_arg_u_v_0_gamma_ap_vld),
    .kernel_arg_u_v_0_time(sig_vivado_activity_thread_kernel_arg_u_v_0_time),
    .kernel_arg_u_v_0_time_ap_vld(sig_vivado_activity_thread_kernel_arg_u_v_0_time_ap_vld),
    .kernel_arg_o_a_0_strike_price(sig_vivado_activity_thread_kernel_arg_o_a_0_strike_price),
    .kernel_arg_o_a_0_time_period(sig_vivado_activity_thread_kernel_arg_o_a_0_time_period),
    .kernel_arg_o_a_0_call(sig_vivado_activity_thread_kernel_arg_o_a_0_call),
    .kernel_arg_o_v_0_delta_time(sig_vivado_activity_thread_kernel_arg_o_v_0_delta_time),
    .kernel_arg_o_v_0_value(sig_vivado_activity_thread_kernel_arg_o_v_0_value),
    .kernel_arg_o_v_0_value_ap_vld(sig_vivado_activity_thread_kernel_arg_o_v_0_value_ap_vld),
    .ap_rst(sig_vivado_activity_thread_ap_rst),
    .ap_clk(aclk),
    .result_0_din(result_0_din),
    .result_0_full_n(result_0_full_n),
    .result_0_write(result_0_write),
    .ap_start(ap_start),
    .ap_ready(ap_ready),
    .ap_done(ap_done),
    .ap_idle(ap_idle)
);

vivado_activity_thread_CORE_IO_if #(
    .C_ADDR_WIDTH(C_S_AXI_CORE_IO_ADDR_WIDTH),
    .C_DATA_WIDTH(C_S_AXI_CORE_IO_DATA_WIDTH))
vivado_activity_thread_CORE_IO_if_U(
    .ACLK(aclk),
    .ARESETN(aresetn),
    .I_kernel_arg_u_a_0_rfir(sig_vivado_activity_thread_kernel_arg_u_a_0_rfir),
    .I_kernel_arg_u_a_0_current_price(sig_vivado_activity_thread_kernel_arg_u_a_0_current_price),
    .O_kernel_arg_u_v_0_gamma(sig_vivado_activity_thread_kernel_arg_u_v_0_gamma),
    .O_kernel_arg_u_v_0_gamma_ap_vld(sig_vivado_activity_thread_kernel_arg_u_v_0_gamma_ap_vld),
    .O_kernel_arg_u_v_0_time(sig_vivado_activity_thread_kernel_arg_u_v_0_time),
    .O_kernel_arg_u_v_0_time_ap_vld(sig_vivado_activity_thread_kernel_arg_u_v_0_time_ap_vld),
    .I_kernel_arg_o_a_0_strike_price(sig_vivado_activity_thread_kernel_arg_o_a_0_strike_price),
    .I_kernel_arg_o_a_0_time_period(sig_vivado_activity_thread_kernel_arg_o_a_0_time_period),
    .I_kernel_arg_o_a_0_call(sig_vivado_activity_thread_kernel_arg_o_a_0_call),
    .I_kernel_arg_o_v_0_delta_time(sig_vivado_activity_thread_kernel_arg_o_v_0_delta_time),
    .O_kernel_arg_o_v_0_value(sig_vivado_activity_thread_kernel_arg_o_v_0_value),
    .O_kernel_arg_o_v_0_value_ap_vld(sig_vivado_activity_thread_kernel_arg_o_v_0_value_ap_vld),
    .AWADDR(s_axi_CORE_IO_AWADDR),
    .AWVALID(s_axi_CORE_IO_AWVALID),
    .AWREADY(s_axi_CORE_IO_AWREADY),
    .WDATA(s_axi_CORE_IO_WDATA),
    .WSTRB(s_axi_CORE_IO_WSTRB),
    .WVALID(s_axi_CORE_IO_WVALID),
    .WREADY(s_axi_CORE_IO_WREADY),
    .BRESP(s_axi_CORE_IO_BRESP),
    .BVALID(s_axi_CORE_IO_BVALID),
    .BREADY(s_axi_CORE_IO_BREADY),
    .ARADDR(s_axi_CORE_IO_ARADDR),
    .ARVALID(s_axi_CORE_IO_ARVALID),
    .ARREADY(s_axi_CORE_IO_ARREADY),
    .RDATA(s_axi_CORE_IO_RDATA),
    .RRESP(s_axi_CORE_IO_RRESP),
    .RVALID(s_axi_CORE_IO_RVALID),
    .RREADY(s_axi_CORE_IO_RREADY));

vivado_activity_thread_ap_rst_if #(
    .RESET_ACTIVE_LOW(RESET_ACTIVE_LOW))
ap_rst_if_U(
    .dout(sig_vivado_activity_thread_ap_rst),
    .din(aresetn));

endmodule
