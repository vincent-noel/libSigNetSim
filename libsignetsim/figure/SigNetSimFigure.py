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
from __future__ import division


from libsignetsim.settings.Settings import Settings
import matplotlib.pyplot as plt


class SigNetSimFigure(object):


    default_width = 1000
    default_dpi = 600

    def __init__(self, width=default_width, dpi=default_dpi):

        self.__figure = plt.figure(figsize=(10, 6))

        self.curveIds = {}
        self.plots = []
        if dpi is None:
            self.__dpi = self.default_dpi
        else:
            self.__dpi = dpi
        if width is None:
            self.w = self.default_width/float(self.__dpi)
            self.h = (self.default_width * 0.667)/float(self.__dpi)
        else:
            self.w = width/float(self.__dpi)
            self.h = (width * 0.667)/float(self.__dpi)


    def add_subplot(self, nb_cols=1, nb_rows=None, id_cell=None, x_label=None, y_label=None):

        if nb_rows == None and id_cell == None:
            t_subplot = self.__figure.add_subplot(nb_cols,1,1)
        else:
            t_subplot = self.__figure.add_subplot(nb_cols, nb_rows, id_cell)


        self.curveIds.update({t_subplot: 0})
        # t_subplot.spines["top"].set_visible(False)
        # t_subplot.spines["right"].set_visible(False)
        # t_subplot.spines["bottom"].set_linewidth(0.3 * self.w)
        # t_subplot.spines["left"].set_linewidth(0.3 * self.w)

        t_subplot.tick_params(
            axis='x',          # changes apply to the x-axis
            which='both',      # both major and minor ticks are affected
            bottom=False,      # ticks along the bottom edge are off
            top=False,         # ticks along the top edge are off
            labelbottom=True,  # labels along the bottom edge are off
        )

        t_subplot.tick_params(
            axis='y',          # changes apply to the x-axis
            which='both',      # both major and minor ticks are affected
            left=False,        # ticks along the bottom edge are off
            right=False,       # ticks along the top edge are off
            labelbottom=True,  # labels along the bottom edge are off
        )

        if x_label is not None:
            t_subplot.set_xlabel(x_label, fontsize=int(15 * self.w))

        if y_label is not None:
            t_subplot.set_ylabel(y_label, fontsize=int(15 * self.w))

        self.plots.append(t_subplot)
        return t_subplot



    def plot(self, subplot, curve_id, x, y, x_name="", y_name=None, marker="-"):

        curve_id = self.curveIds[subplot]

        if y_name is None:
            subplot.plot(x, y, marker,
                color=Settings.color_scheme[curve_id % len(Settings.color_scheme)],
                # linewidth=int(5 * self.w),
                # label=y_name
            )
        else:
            subplot.plot(x, y, marker,
                 color=Settings.color_scheme[curve_id % len(Settings.color_scheme)],
                 # linewidth=int(5 * self.w),
                 label=y_name
            )

        self.curveIds.update({subplot: curve_id+1})
