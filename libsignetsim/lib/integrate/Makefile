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

SRCDIR = src
LIBDIR = lib
LIBSDIR = /usr/lib64/atlas-basic/
FLAGS = -Wall -Werror -fPIC -pedantic -std=gnu99
LIBS = -lsundials_cvode -lsundials_nvecserial -lsundials_ida -lm -llapack -latlas -lblas


IOBJ = shared.o events.o ode.o dae.o integrate.o realtype_math.o

SUNDIALS_INCLUDE = /usr/include
SUNDIALS_MAIN_VERSION := $(shell cat $(SUNDIALS_INCLUDE)/sundials/sundials_config.h | grep SUNDIALS_PACKAGE_VERSION | cut -d' ' -f3 | tr -d '"' | cut -d'.' -f1)



integrate.so: $(IOBJ)
	$(CC) -shared -o integrate.so $(IOBJ) $(LIBS) -L$(LIBSDIR)
	$(RM) *.o

#Integrate
realtype_math.o: $(SRCDIR)/realtype_math.c $(SRCDIR)/realtype_math.h
	$(CC) $(FLAGS) -c $(SRCDIR)/realtype_math.c

shared.o: $(SRCDIR)/shared.c $(SRCDIR)/shared.h
	$(CC) $(FLAGS) -c $(SRCDIR)/shared.c

events.o: $(SRCDIR)/events.c $(SRCDIR)/events.h
	$(CC) $(FLAGS) -c $(SRCDIR)/events.c

ode.o: $(SRCDIR)/ode.c $(SRCDIR)/ode.h
ifeq ($(SUNDIALS_MAIN_VERSION), 2)
	$(CC) $(FLAGS) -c $(SRCDIR)/ode.c
else
	$(CC) $(FLAGS) -c $(SRCDIR)/ode.c -DSUNDIALS3
endif

dae.o: $(SRCDIR)/dae.c $(SRCDIR)/dae.h
ifeq ($(SUNDIALS_MAIN_VERSION), 2)
	$(CC) $(FLAGS) -c $(SRCDIR)/dae.c
else
	$(CC) $(FLAGS) -c $(SRCDIR)/dae.c -DSUNDIALS3

endif

integrate.o: $(SRCDIR)/integrate.c $(SRCDIR)/integrate.h
	$(CC) $(FLAGS) -c $(SRCDIR)/integrate.c

clean:
	$(RM) *.o *.so
