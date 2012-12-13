/*
 * option.c
 *
 *  Created on: 10 November 2012
 *      Author: gordon
 */
#include "option.h"

void option_derivative_init(double t,double c,double k,double p,option_opt_attr* o_a){
	o_a->strike_price = k;
	o_a->call=c;
	o_a->time_period=t;
	o_a->points = p;
}

void option_derivative_path_init(option_opt_var* o_v,option_opt_attr* o_a){
	o_v->value=0;
	o_v->delta_time=o_a->time_period/o_a->points;
}

void option_derivative_path(double price,double time,option_opt_var* o_v,option_opt_attr* o_a){
}

void option_derivative_payoff(double end_price,option_opt_var* o_v,option_opt_attr* o_a){
	if((o_a->call)){
		o_v->value = (end_price-o_a->strike_price);
	}
	else{
		o_v->value = (o_a->strike_price-end_price);
	}
}