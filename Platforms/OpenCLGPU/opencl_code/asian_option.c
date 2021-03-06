/*
 * asian_option.c
 *
 *  Created on: 17 June 2012
 *      Author: gordon
 */
#include "asian_option.h"

void asian_option_derivative_init(FP_t t,char c,FP_t k,FP_t p,asian_option_attributes* o_a){
    european_option_derivative_init(t,c,k,&(o_a->european_option));
    o_a->strike_price = (o_a->european_option).strike_price;
    o_a->call = (o_a->european_option).call;
    o_a->time_period = (o_a->european_option).time_period;
    
    //Asian Specific Behaviour
    o_a->points = p;
    
}

void asian_option_derivative_path_init(asian_option_variables* o_v,asian_option_attributes* o_a){
    european_option_derivative_path_init(&(o_v->european_option),&(o_a->european_option));
    o_v->value = (o_v->european_option).value;
    o_v->delta_time = (o_v->european_option).delta_time/o_a->points;
    
    o_v->average_value = 0;
}

void asian_option_derivative_path(FP_t price,FP_t time,asian_option_variables* o_v,asian_option_attributes* o_a){
    //shouldn't really bother calling european path function, it doesn't do anything...
    european_option_derivative_path(price,time,&(o_v->european_option),&(o_a->european_option));
    
    o_v->average_value += price;
}

void asian_option_derivative_payoff(FP_t end_price,asian_option_variables* o_v,asian_option_attributes* o_a){
    o_v->average_value = o_v->average_value/o_a->points;
    
    european_option_derivative_payoff(o_v->average_value,&(o_v->european_option),&(o_a->european_option));
    o_v->value = (o_v->european_option).value;
}