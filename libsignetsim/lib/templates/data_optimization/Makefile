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

SRCDIR = src
LIBDIR = lib

IDIR = $(SRCDIR)/integrate
GDIR = $(SRCDIR)

FLAGS = -Wall -Werror -pedantic -std=gnu99
LIBS = -lsundials_cvode -lsundials_nvecserial -lsundials_ida -lm -llapack -latlas -lblas
OBJ = scoreFunctions.o model.o data.o $(IOBJ)
SOBJ = optim.o $(LIBDIR)/libplsa-serial.so main.o
POBJ = optim_p.o $(LIBDIR)/libplsa-parallel.so main_p.o
IOBJ = $(LIBDIR)/integrate.so


lsa: $(OBJ) $(SOBJ)
	gcc $(OBJ) $(SOBJ) $(LIBS) -o lsa
	rm *.o

lsa.mpi: $(OBJ) $(POBJ)
	mpicc $(OBJ) $(POBJ) $(LIBS) -DMPI -o lsa.mpi
	rm *.o


# Generated
model.o: $(GDIR)/model.c $(GDIR)/model.h
	gcc -pedantic -std=gnu99 -c $(GDIR)/model.c

data.o: $(GDIR)/data.c $(GDIR)/data.h
	gcc $(FLAGS) -c $(GDIR)/data.c

optim.o: $(GDIR)/optim.c $(GDIR)/optim.h
	gcc $(FLAGS) -c $(GDIR)/optim.c


optim_p.o: $(GDIR)/optim.c $(GDIR)/optim.h
	mpicc $(FLAGS) -c -DMPI $(GDIR)/optim.c -o optim_p.o


#Other ones
main.o:	$(SRCDIR)/main.c
	gcc $(FLAGS) -c $(SRCDIR)/main.c

main_p.o:	$(SRCDIR)/main.c
	mpicc $(FLAGS) -c -DMPI $(SRCDIR)/main.c -o main_p.o

scoreFunctions.o: $(SRCDIR)/scoreFunctions.c $(SRCDIR)/scoreFunctions.h
	gcc $(FLAGS) -c $(SRCDIR)/scoreFunctions.c


# clean
clean:
	rm -f lsa lsa.mpi *.o *.state *.log \
	$(log_dir)/res_* \
	$(log_dir)/ref_res_* \
	$(log_dir)/res/res* \
	$(log_dir)/score/score*

clean_logs:
	rm $(log_dir)/res_* \
	$(log_dir)/ref_res_* \
	$(log_dir)/res/res* \
	$(log_dir)/score/score*
