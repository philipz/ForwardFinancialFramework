// ==============================================================
// File generated by Vivado(TM) HLS - High-Level Synthesis from C, C++ and SystemC
// Version: 2013.4
// Copyright (C) 2013 Xilinx Inc. All rights reserved.
// 
// ==============================================================

/***************************** Include Files *********************************/
#include "xvivado_activity_thread.h"

/************************** Function Implementation *************************/
#ifndef __linux__
int XVivado_activity_thread_CfgInitialize(XVivado_activity_thread *InstancePtr, XVivado_activity_thread_Config *ConfigPtr) {
    Xil_AssertNonvoid(InstancePtr != NULL);
    Xil_AssertNonvoid(ConfigPtr != NULL);

    InstancePtr->Core_io_BaseAddress = ConfigPtr->Core_io_BaseAddress;
    InstancePtr->IsReady = XIL_COMPONENT_IS_READY;

    return XST_SUCCESS;
}
#endif

void XVivado_activity_thread_SetKernel_arg_u_a_0_rfir(XVivado_activity_thread *InstancePtr, u32 Data) {
    Xil_AssertVoid(InstancePtr != NULL);
    Xil_AssertVoid(InstancePtr->IsReady == XIL_COMPONENT_IS_READY);

    XVivado_activity_thread_WriteReg(InstancePtr->Core_io_BaseAddress, XVIVADO_ACTIVITY_THREAD_CORE_IO_ADDR_KERNEL_ARG_U_A_0_RFIR_DATA, Data);
}

u32 XVivado_activity_thread_GetKernel_arg_u_a_0_rfir(XVivado_activity_thread *InstancePtr) {
    u32 Data;

    Xil_AssertNonvoid(InstancePtr != NULL);
    Xil_AssertNonvoid(InstancePtr->IsReady == XIL_COMPONENT_IS_READY);

    Data = XVivado_activity_thread_ReadReg(InstancePtr->Core_io_BaseAddress, XVIVADO_ACTIVITY_THREAD_CORE_IO_ADDR_KERNEL_ARG_U_A_0_RFIR_DATA);
    return Data;
}

void XVivado_activity_thread_SetKernel_arg_u_a_0_current_price(XVivado_activity_thread *InstancePtr, u32 Data) {
    Xil_AssertVoid(InstancePtr != NULL);
    Xil_AssertVoid(InstancePtr->IsReady == XIL_COMPONENT_IS_READY);

    XVivado_activity_thread_WriteReg(InstancePtr->Core_io_BaseAddress, XVIVADO_ACTIVITY_THREAD_CORE_IO_ADDR_KERNEL_ARG_U_A_0_CURRENT_PRICE_DATA, Data);
}

u32 XVivado_activity_thread_GetKernel_arg_u_a_0_current_price(XVivado_activity_thread *InstancePtr) {
    u32 Data;

    Xil_AssertNonvoid(InstancePtr != NULL);
    Xil_AssertNonvoid(InstancePtr->IsReady == XIL_COMPONENT_IS_READY);

    Data = XVivado_activity_thread_ReadReg(InstancePtr->Core_io_BaseAddress, XVIVADO_ACTIVITY_THREAD_CORE_IO_ADDR_KERNEL_ARG_U_A_0_CURRENT_PRICE_DATA);
    return Data;
}

u32 XVivado_activity_thread_GetKernel_arg_u_v_0_gamma(XVivado_activity_thread *InstancePtr) {
    u32 Data;

    Xil_AssertNonvoid(InstancePtr != NULL);
    Xil_AssertNonvoid(InstancePtr->IsReady == XIL_COMPONENT_IS_READY);

    Data = XVivado_activity_thread_ReadReg(InstancePtr->Core_io_BaseAddress, XVIVADO_ACTIVITY_THREAD_CORE_IO_ADDR_KERNEL_ARG_U_V_0_GAMMA_DATA);
    return Data;
}

u32 XVivado_activity_thread_GetKernel_arg_u_v_0_gammaVld(XVivado_activity_thread *InstancePtr) {
    u32 Data;

    Xil_AssertNonvoid(InstancePtr != NULL);
    Xil_AssertNonvoid(InstancePtr->IsReady == XIL_COMPONENT_IS_READY);

    Data = XVivado_activity_thread_ReadReg(InstancePtr->Core_io_BaseAddress, XVIVADO_ACTIVITY_THREAD_CORE_IO_ADDR_KERNEL_ARG_U_V_0_GAMMA_CTRL);
    return Data & 0x1;
}

u32 XVivado_activity_thread_GetKernel_arg_u_v_0_time(XVivado_activity_thread *InstancePtr) {
    u32 Data;

    Xil_AssertNonvoid(InstancePtr != NULL);
    Xil_AssertNonvoid(InstancePtr->IsReady == XIL_COMPONENT_IS_READY);

    Data = XVivado_activity_thread_ReadReg(InstancePtr->Core_io_BaseAddress, XVIVADO_ACTIVITY_THREAD_CORE_IO_ADDR_KERNEL_ARG_U_V_0_TIME_DATA);
    return Data;
}

u32 XVivado_activity_thread_GetKernel_arg_u_v_0_timeVld(XVivado_activity_thread *InstancePtr) {
    u32 Data;

    Xil_AssertNonvoid(InstancePtr != NULL);
    Xil_AssertNonvoid(InstancePtr->IsReady == XIL_COMPONENT_IS_READY);

    Data = XVivado_activity_thread_ReadReg(InstancePtr->Core_io_BaseAddress, XVIVADO_ACTIVITY_THREAD_CORE_IO_ADDR_KERNEL_ARG_U_V_0_TIME_CTRL);
    return Data & 0x1;
}

void XVivado_activity_thread_SetKernel_arg_o_a_0_strike_price(XVivado_activity_thread *InstancePtr, u32 Data) {
    Xil_AssertVoid(InstancePtr != NULL);
    Xil_AssertVoid(InstancePtr->IsReady == XIL_COMPONENT_IS_READY);

    XVivado_activity_thread_WriteReg(InstancePtr->Core_io_BaseAddress, XVIVADO_ACTIVITY_THREAD_CORE_IO_ADDR_KERNEL_ARG_O_A_0_STRIKE_PRICE_DATA, Data);
}

u32 XVivado_activity_thread_GetKernel_arg_o_a_0_strike_price(XVivado_activity_thread *InstancePtr) {
    u32 Data;

    Xil_AssertNonvoid(InstancePtr != NULL);
    Xil_AssertNonvoid(InstancePtr->IsReady == XIL_COMPONENT_IS_READY);

    Data = XVivado_activity_thread_ReadReg(InstancePtr->Core_io_BaseAddress, XVIVADO_ACTIVITY_THREAD_CORE_IO_ADDR_KERNEL_ARG_O_A_0_STRIKE_PRICE_DATA);
    return Data;
}

void XVivado_activity_thread_SetKernel_arg_o_a_0_time_period(XVivado_activity_thread *InstancePtr, u32 Data) {
    Xil_AssertVoid(InstancePtr != NULL);
    Xil_AssertVoid(InstancePtr->IsReady == XIL_COMPONENT_IS_READY);

    XVivado_activity_thread_WriteReg(InstancePtr->Core_io_BaseAddress, XVIVADO_ACTIVITY_THREAD_CORE_IO_ADDR_KERNEL_ARG_O_A_0_TIME_PERIOD_DATA, Data);
}

u32 XVivado_activity_thread_GetKernel_arg_o_a_0_time_period(XVivado_activity_thread *InstancePtr) {
    u32 Data;

    Xil_AssertNonvoid(InstancePtr != NULL);
    Xil_AssertNonvoid(InstancePtr->IsReady == XIL_COMPONENT_IS_READY);

    Data = XVivado_activity_thread_ReadReg(InstancePtr->Core_io_BaseAddress, XVIVADO_ACTIVITY_THREAD_CORE_IO_ADDR_KERNEL_ARG_O_A_0_TIME_PERIOD_DATA);
    return Data;
}

void XVivado_activity_thread_SetKernel_arg_o_a_0_call(XVivado_activity_thread *InstancePtr, u32 Data) {
    Xil_AssertVoid(InstancePtr != NULL);
    Xil_AssertVoid(InstancePtr->IsReady == XIL_COMPONENT_IS_READY);

    XVivado_activity_thread_WriteReg(InstancePtr->Core_io_BaseAddress, XVIVADO_ACTIVITY_THREAD_CORE_IO_ADDR_KERNEL_ARG_O_A_0_CALL_DATA, Data);
}

u32 XVivado_activity_thread_GetKernel_arg_o_a_0_call(XVivado_activity_thread *InstancePtr) {
    u32 Data;

    Xil_AssertNonvoid(InstancePtr != NULL);
    Xil_AssertNonvoid(InstancePtr->IsReady == XIL_COMPONENT_IS_READY);

    Data = XVivado_activity_thread_ReadReg(InstancePtr->Core_io_BaseAddress, XVIVADO_ACTIVITY_THREAD_CORE_IO_ADDR_KERNEL_ARG_O_A_0_CALL_DATA);
    return Data;
}

void XVivado_activity_thread_SetKernel_arg_o_v_0_delta_time(XVivado_activity_thread *InstancePtr, u32 Data) {
    Xil_AssertVoid(InstancePtr != NULL);
    Xil_AssertVoid(InstancePtr->IsReady == XIL_COMPONENT_IS_READY);

    XVivado_activity_thread_WriteReg(InstancePtr->Core_io_BaseAddress, XVIVADO_ACTIVITY_THREAD_CORE_IO_ADDR_KERNEL_ARG_O_V_0_DELTA_TIME_DATA, Data);
}

u32 XVivado_activity_thread_GetKernel_arg_o_v_0_delta_time(XVivado_activity_thread *InstancePtr) {
    u32 Data;

    Xil_AssertNonvoid(InstancePtr != NULL);
    Xil_AssertNonvoid(InstancePtr->IsReady == XIL_COMPONENT_IS_READY);

    Data = XVivado_activity_thread_ReadReg(InstancePtr->Core_io_BaseAddress, XVIVADO_ACTIVITY_THREAD_CORE_IO_ADDR_KERNEL_ARG_O_V_0_DELTA_TIME_DATA);
    return Data;
}

u32 XVivado_activity_thread_GetKernel_arg_o_v_0_value(XVivado_activity_thread *InstancePtr) {
    u32 Data;

    Xil_AssertNonvoid(InstancePtr != NULL);
    Xil_AssertNonvoid(InstancePtr->IsReady == XIL_COMPONENT_IS_READY);

    Data = XVivado_activity_thread_ReadReg(InstancePtr->Core_io_BaseAddress, XVIVADO_ACTIVITY_THREAD_CORE_IO_ADDR_KERNEL_ARG_O_V_0_VALUE_DATA);
    return Data;
}

u32 XVivado_activity_thread_GetKernel_arg_o_v_0_valueVld(XVivado_activity_thread *InstancePtr) {
    u32 Data;

    Xil_AssertNonvoid(InstancePtr != NULL);
    Xil_AssertNonvoid(InstancePtr->IsReady == XIL_COMPONENT_IS_READY);

    Data = XVivado_activity_thread_ReadReg(InstancePtr->Core_io_BaseAddress, XVIVADO_ACTIVITY_THREAD_CORE_IO_ADDR_KERNEL_ARG_O_V_0_VALUE_CTRL);
    return Data & 0x1;
}

