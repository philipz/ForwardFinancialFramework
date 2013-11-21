package mc_solver_maxeler;

import com.maxeler.maxcompiler.v2.kernelcompiler.types.base.DFEVar;

public class barrier_option_parameters extends european_option_parameters {
	protected final DFEVar points,barrier,down,out;

	public barrier_option_parameters(MC_Solver_Maxeler_Base_Kernel k,DFEVar time_period,DFEVar call,DFEVar strike_price,DFEVar observation_points,DFEVar barrier,DFEVar out,DFEVar down){
		super(k,time_period,call,strike_price);
		this.points = observation_points;
		this.barrier = barrier;
		this.down = down;
		this.out = out;
	}

}
