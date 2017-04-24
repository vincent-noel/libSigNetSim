/******************************************************************************
 *                                                                            *
 *   realtype_math.c                                                          *
 *                                                                            *
 ******************************************************************************
 *                                                                            *
 *   written by Vincent Noel                                                  *
 *                                                                            *
 ******************************************************************************
 *                                                                            *
 *   Math functions for CVODE type realtype                                   *
 *                                                                            *
 ******************************************************************************
 *                                                                            *
 *   Copyright (C) 2016 Vincent Noel (vincent.noel@butantan.gov.br)           *
 *                                                                            *
 *   This file is part of libSigNetSim.                                       *
 *                                                                            *
 *   libSigNetSim is free software: you can redistribute it and/or modify     *
 *   it under the terms of the GNU General Public License as published by     *
 *   the Free Software Foundation, either version 3 of the License, or        *
 *   (at your option) any later version.                                      *
 *                                                                            *
 *   libSigNetSim is distributed in the hope that it will be useful,          *
 *   but WITHOUT ANY WARRANTY; without even the implied warranty of           *
 *   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the            *
 *   GNU General Public License for more details.                             *
 *                                                                            *
 *   You should have received a copy of the GNU General Public License        *
 *   along with SigNetSim.  If not, see <http://www.gnu.org/licenses/>.       *
 *                                                                            *
 ******************************************************************************/

#define MAX(a,b) (((a)>(b))?(a):(b))
#define MIN(a,b) (((a)<(b))?(a):(b))

#include <stdio.h>
#include "realtype_math.h"

realtype abs_tol = RCONST(DBL_EPSILON);
realtype rel_tol = RCONST(DBL_EPSILON);


void rt_set_precision(realtype abs_tol, realtype rel_tol)
{
	abs_tol = abs_tol;
	rel_tol = rel_tol;
}

int rt_eq(realtype x, realtype y)
{
	return (rt_abs(x-y) <= MAX(abs_tol, rel_tol*MAX(rt_abs(x), rt_abs(y))));
//	return (rt_abs(x-y) <= rt_get_precision(x));
//	return (rt_abs(x-y) <= DBL_EPSILON);
}

int rt_neq(realtype x, realtype y)
{
	return (rt_abs(x-y) > MAX(abs_tol, rel_tol*MAX(rt_abs(x), rt_abs(y))));
//	return (rt_abs(x-y) > rt_get_precision(x));
//	return (rt_abs(x-y) > DBL_EPSILON);
}

int rt_lt(realtype x, realtype y)
{
	return ((x < y) && rt_neq(x,y));
}

int rt_gt(realtype x, realtype y)
{
	return ((x > y) && rt_neq(x,y));
}

int rt_leq(realtype x, realtype y)
{
	return (rt_eq(x,y) || (x < y));
}

int rt_geq(realtype x, realtype y)
{
	return (rt_eq(x,y) || (x > y));
}

int rt_rec_factorial(int n)
{
    if (n <= 1) return 1;
    else return n*rt_rec_factorial(n-1);
}

realtype rt_factorial(realtype n)
{
  return RCONST((double) rt_rec_factorial((int) n));
}

realtype rt_ceil(realtype n)
{
	return RCONST(ceil((double) n));
}

realtype rt_floor(realtype n)
{
	return RCONST(floor((double) n));
}

realtype rt_pow(realtype x, realtype n)
{
	return RCONST(pow((double) x, (double) n));
}

realtype rt_exp(realtype x)
{
	return RCONST(exp((double) x));
}

realtype rt_abs(realtype x)
{
	return RCONST(fabs((double) x));
}

realtype rt_log(realtype x)
{
	return RCONST(log((double) x));
}

realtype rt_cos(realtype x)
{
	return RCONST(cos((double) x));
}

realtype rt_cosh(realtype x)
{
	return RCONST(cosh((double) x));
}

realtype rt_sin(realtype x)
{
	return RCONST(sin((double) x));
}

realtype rt_sinh(realtype x)
{
	return RCONST(sinh((double) x));
}

realtype rt_tan(realtype x)
{
	return RCONST(tan((double) x));
}

realtype rt_tanh(realtype x)
{
	return RCONST(tanh((double) x));
}
realtype rt_acos(realtype x)
{
	return RCONST(acos((double) x));
}

realtype rt_acosh(realtype x)
{
	return RCONST(acosh((double) x));
}

realtype rt_asin(realtype x)
{
	return RCONST(asin((double) x));
}

realtype rt_asinh(realtype x)
{
	return RCONST(asinh((double) x));
}

realtype rt_atan(realtype x)
{
	return (realtype) atan((double) x);
}

realtype rt_atanh(realtype x)
{
	return (realtype) atanh((double) x);
}

realtype rt_cot(realtype x)
{
	return RCONST(1.0)/rt_tan(x);
}

realtype rt_coth(realtype x)
{
	return RCONST(1.0)/rt_tanh(x);
}

realtype rt_sec(realtype x)
{
	return RCONST(1.0)/rt_cos(x);
}

realtype rt_sech(realtype x)
{
	return RCONST(1.0)/rt_cosh(x);
}

realtype rt_csc(realtype x)
{
	return RCONST(1.0)/rt_sin(x);
}

realtype rt_csch(realtype x)
{
	return RCONST(1.0)/rt_sinh(x);
}


realtype rt_acot(realtype x)
{
	return rt_atan(RCONST(1.0)/x);
}

realtype rt_acoth(realtype x)
{
	return rt_atanh(RCONST(1.0)/x);
}

realtype rt_asec(realtype x)
{
	return rt_acos(RCONST(1.0)/x);
}

realtype rt_asech(realtype x)
{
	return rt_acosh(RCONST(1.0)/x);
}

realtype rt_acsc(realtype x)
{
	return rt_asin(RCONST(1.0)/x);
}

realtype rt_acsch(realtype x)
{
	return rt_asinh(RCONST(1.0)/x);
}
