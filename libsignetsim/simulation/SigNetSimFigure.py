#!/usr/bin/env python
""" SigNetSimFigure.py


    This file ...


    Copyright (C) 2016 Vincent Noel (vincent.noel@butantan.gov.br)

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program. If not, see <http://www.gnu.org/licenses/>.

"""

import matplotlib.pyplot as plt
# from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure
from matplotlib.dates import DateFormatter
import matplotlib
matplotlib.rcParams['figure.figsize'] = (20.0, 10.0)
color_scheme = ['#009ece', '#ff9e00', '#9ccf31', '#f7d708', '#ce0000']
color_scheme_light = ['#67b6ce']
default_width = 1000
default_dpi = 600

class SigNetSimFigure(Figure):


    def __init__(self,
                 width=default_width,
                 x_unit="",
                 y_unit="",
                 nb_rows=1,
                 nb_cols=1,
                 dpi=default_dpi):


        if dpi is None:
            self.__dpi = default_dpi
        else:
            self.__dpi = dpi
        if width is None:
            self.w = default_width / float(self.__dpi)
            self.h = (default_width * 0.667) / float(self.__dpi)
        else:
            self.w = width / float(self.__dpi)
            self.h = (width * 0.667) / float(self.__dpi)

        self.x_unit = x_unit
        self.y_unit = y_unit
        #
        # print self.h
        # print self.w
        Figure.__init__(self,
                        figsize=(10,6),#self.w, self.h * float(nb_rows)),
                        dpi=self.__dpi,
                        tight_layout=False,
                        facecolor='white')


    def add_subplot(self, nb_cols=1, nb_rows=None, id_cell=None):

        t_subplot = None
        if nb_rows == None and id_cell == None:
            t_subplot = plt.subplot(nb_cols,1,1)
        else:
            t_subplot = plt.subplot(nb_cols, nb_rows, id_cell)

        t_subplot.spines["top"].set_visible(False)
        t_subplot.spines["right"].set_visible(False)
        t_subplot.spines["bottom"].set_linewidth(0.3 * self.w)
        t_subplot.spines["left"].set_linewidth(0.3 * self.w)

        t_subplot.tick_params(
            axis='x',          # changes apply to the x-axis
            which='both',      # both major and minor ticks are affected
            bottom='off',      # ticks along the bottom edge are off
            top='off',         # ticks along the top edge are off
            labelbottom='on',  # labels along the bottom edge are off
            labelsize=int(15 * self.w))
        #
        t_subplot.tick_params(
            axis='y',          # changes apply to the x-axis
            which='both',      # both major and minor ticks are affected
            left='off',        # ticks along the bottom edge are off
            right='off',       # ticks along the top edge are off
            labelbottom='on',  # labels along the bottom edge are off
            labelsize=int(15 * self.w))

        t_subplot.set_xlabel(self.x_unit, fontsize=int(15 * self.w))
        t_subplot.set_ylabel(self.y_unit, fontsize=int(15 * self.w))

        return t_subplot
