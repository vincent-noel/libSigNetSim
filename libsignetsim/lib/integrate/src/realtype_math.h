/******************************************************************************
 *                                                                            *
 *   realtype_math.h                                                          *
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

#include <sundials/sundials_types.h> /* definition of type realtype */
#include <math.h>

#define RT_PI RCONST(M_PI)
#define RT_E RCONST(M_E)
#define RT_NA RCONST(6.02214179E+23)
#define RT_NAN RCONST(NAN)
#define RT_INF RCONST(INFINITY)

void rt_set_precision(realtype abs_tol, realtype rel_tol);

int rt_eq(realtype x, realtype y);
int rt_neq(realtype x, realtype y);
int rt_lt(realtype x, realtype y);
int rt_gt(realtype x, realtype y);
int rt_leq(realtype x, realtype y);
int rt_geq(realtype x, realtype y);

realtype rt_factorial(realtype n);
realtype rt_ceil(realtype n);
realtype rt_floor(realtype n);

realtype rt_pow(realtype x, realtype n);
realtype rt_exp(realtype x);
realtype rt_abs(realtype x);
realtype rt_log(realtype x);
realtype rt_cos(realtype x);
realtype rt_cosh(realtype x);
realtype rt_sin(realtype x);
realtype rt_sinh(realtype x);
realtype rt_tan(realtype x);
realtype rt_tanh(realtype x);
realtype rt_acos(realtype x);
realtype rt_acosh(realtype x);
realtype rt_asin(realtype x);
realtype rt_asinh(realtype x);
realtype rt_atan(realtype x);
realtype rt_atanh(realtype x);
realtype rt_cot(realtype x);
realtype rt_coth(realtype x);
realtype rt_sec(realtype x);
realtype rt_sech(realtype x);
realtype rt_csc(realtype x);
realtype rt_csch(realtype x);
realtype rt_acot(realtype x);
realtype rt_acoth(realtype x);
realtype rt_asec(realtype x);
realtype rt_asech(realtype x);
realtype rt_acsc(realtype x);
realtype rt_acsch(realtype x);

// realtype RT_PI = RCONST(M_PI);
// realtype RT_E = RCONST(M_E);
// realtype RT_NA = RCONST(6.02214179E+23);
// realtype RT_NAN = RCONST(NAN);
// realtype RT_INF = RCONST(INFINITY);
