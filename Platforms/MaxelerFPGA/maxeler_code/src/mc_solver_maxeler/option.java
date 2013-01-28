package mc_solver_maxeler;

import com.maxeler.maxcompiler.v1.kernelcompiler.Kernel;
import com.maxeler.maxcompiler.v1.kernelcompiler.KernelLib;
import com.maxeler.maxcompiler.v1.kernelcompiler.types.base.HWVar;

public class option extends KernelLib{
	//HWFloat doubleType = Kernel.hwFloat(11,53);
	String name = "option";

	protected option_parameters parameters;

	protected HWVar delta_time;
	protected HWVar carried_delta_time;
	protected HWVar new_delta_time;

	protected HWVar value;

	protected HWVar enable;
	protected HWVar carried_enable;
	protected HWVar new_enable;

	//protected HWVar temp_price;

	Kernel kernel;
	HWVar path;
	HWVar point;

	public option(MC_Solver_Maxeler_Base_Kernel kernel,HWVar pp,HWVar p,HWVar enable,option_parameters op) {
		super(kernel);
		this.kernel = kernel;
		this.point = pp;
		this.path = p;
		this.enable = enable;

		//this.temp_price = temp_price;

		this.parameters = op;
	}

	public void path_init(){
		carried_delta_time = ((MC_Solver_Maxeler_Base_Kernel)this.kernel).inputDoubleType.newInstance(((MC_Solver_Maxeler_Base_Kernel)this.kernel));

		this.delta_time = this.point.eq(0) ? ((this.parameters.time_period/(this.parameters.points))).cast(((MC_Solver_Maxeler_Base_Kernel)this.kernel).inputDoubleType) : this.carried_delta_time;
		}

	public void path(HWVar temp_price,HWVar time){
		this.new_delta_time = this.enable.eq(true)?this.parameters.time_period/(this.parameters.points):0.0;
		this.new_enable = this.enable;
		//this.value = (this.point.eq(this.kernel.path_points-1)) ? this.payoff(temp_price) : this.kernel.constant.var(this.kernel.doubleType,0.0);
	}

	public void connect_path(){
		this.carried_delta_time <== ((MC_Solver_Maxeler_Base_Kernel)this.kernel).stream.offset(this.new_delta_time,-((MC_Solver_Maxeler_Base_Kernel)this.kernel).instance_paths);
	}

	public HWVar payoff(HWVar end_price){
		return (this.parameters.call).eq(0) ? this.parameters.strike_price-end_price : end_price-this.parameters.strike_price;
	}

}
