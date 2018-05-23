# Copyright (C) 2016 Vincent Noel (vincent.noel@butantan.gov.br)
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
# along with libSigNetSim. If not, see <http://www.gnu.org/licenses/>.

log_dir = logs

MPICC=$(echo $(find /usr -name mpicc) | cut -d' ' -f1)
SRCDIR = src
LIBDIR = lib

IDIR = $(SRCDIR)/integrate
FLAGS = -Wall -Werror -pedantic -std=gnu99 -O3
LIBS = -lsundials_cvode -lsundials_nvecserial -lsundials_ida -lm -llapack -latlas -lblas
IOBJ = $(LIBDIR)/integrate.so
OBJ = model.o data.o $(IOBJ)
SOBJ = main-serial.o
POBJ = main-parallel.o

all: sim-serial sim-parallel
	$(RM) *.o

sim-serial: $(OBJ) $(SOBJ)
	$(CC) $(SOBJ) $(OBJ) $(LIBS) -o sim-serial

sim-parallel: $(OBJ) $(POBJ)
	$(MPICC) $(POBJ) $(OBJ) $(LIBS) -o sim-parallel


# Generated
model.o: $(SRCDIR)/model.c $(SRCDIR)/model.h
	$(CC) -pedantic -std=gnu99 -c $(SRCDIR)/model.c

data.o: $(SRCDIR)/data.c $(SRCDIR)/data.h
	$(CC) $(FLAGS) -c $(SRCDIR)/data.c


#Main
main-serial.o:	$(SRCDIR)/main.c
	$(CC) $(FLAGS) -c $(SRCDIR)/main.c -o main-serial.o

main-parallel.o:	$(SRCDIR)/main.c
	$(MPICC) $(FLAGS) -DMPI -c $(SRCDIR)/main.c -o main-parallel.o

# clean
clean:
	$(RM) -f *.o results/* *_sim *_comp
