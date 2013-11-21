package mc_solver_maxeler;

import com.maxeler.maxcompiler.v2.kernelcompiler.Kernel;
import com.maxeler.maxcompiler.v2.kernelcompiler.KernelLib;
import com.maxeler.maxcompiler.v2.kernelcompiler.types.base.DFEVar;

public class option_parameters extends KernelLib {
	protected final DFEVar time_period;
	protected final DFEVar call;
	protected final DFEVar strike_price;

	public option_parameters(MC_Solver_Maxeler_Base_Kernel k,DFEVar time_period,DFEVar call,DFEVar strike_price){
		super(k);
		this.time_period = time_period;
		this.call = call;
		this.strike_price = strike_price;
	}

}
