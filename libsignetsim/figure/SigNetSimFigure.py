#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright 2014-2017 Vincent Noel (vincent.noel@butantan.gov.br)
#
# This file is part of libSigNetSim.
#
# libSigNetSim is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# libSigNetSim is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with libSigNetSim.  If not, see <http://www.gnu.org/licenses/>.

"""

    This file ...

"""

import matplotlib.pyplot as plt

class SigNetSimFigure(object):

    # color_scheme = ['#009ece', '#ff9e00', '#9ccf31', '#f7d708', '#ce0000']
    color_scheme = (["#FFB300", "#803E75", "#FF6800", "#A6BDD7"]
                    + ["#C10020", "#CEA262", "#817066", "#007D34"]
                    + ["#F6768E", "#00538A", "#FF7A5C", "#53377A"]
                    + ["#FF8E00", "#B32851", "#F4C800", "#7F180D"]
                    + ["#93AA00", "#593315", "#F13A13", "#232C16"])
    color_scheme_light = ['#67b6ce']
    default_width = 1000
    default_dpi = 600

    def __init__(self):

        self.__figure = plt.figure(figsize=(10, 5))


    def add_subplot(self, nb_cols=1, nb_rows=None, id_cell=None):

        t_subplot = None
        if nb_rows == None and id_cell == None:
            t_subplot = self.__figure.add_subplot(nb_cols,1,1)
        else:
            t_subplot = self.__figure.add_subplot(nb_cols, nb_rows, id_cell)

        # t_subplot.spines["top"].set_visible(False)
        # t_subplot.spines["right"].set_visible(False)
        # t_subplot.spines["bottom"].set_linewidth(0.3 * self.w)
        # t_subplot.spines["left"].set_linewidth(0.3 * self.w)

        t_subplot.tick_params(
            axis='x',          # changes apply to the x-axis
            which='both',      # both major and minor ticks are affected
            bottom='off',      # ticks along the bottom edge are off
            top='off',         # ticks along the top edge are off
            labelbottom='on',  # labels along the bottom edge are off
        )

        t_subplot.tick_params(
            axis='y',          # changes apply to the x-axis
            which='both',      # both major and minor ticks are affected
            left='off',        # ticks along the bottom edge are off
            right='off',       # ticks along the top edge are off
            labelbottom='on',  # labels along the bottom edge are off
        )

        return t_subplot



    def plot(self, subplot, curve_id, x, y, x_name="", y_name=None):

        if y_name is None:
            subplot.plot(x, y, '-',
                color=self.color_scheme[curve_id % len(self.color_scheme)],
                # linewidth=int(5 * self.w),
                # label=y_name
            )
        else:
            subplot.plot(x, y, '-',
                 color=self.color_scheme[curve_id % len(self.color_scheme)],
                 # linewidth=int(5 * self.w),
                 label=y_name
            )
