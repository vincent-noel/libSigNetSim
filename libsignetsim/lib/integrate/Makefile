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

FLAGS = -Wall -Werror -fPIC -pedantic -std=gnu99
LIBS = -lsundials_cvode -lsundials_nvecserial -lsundials_ida -lm

IOBJ = shared.o events.o ode.o dae.o integrate.o realtype_math.o

integrate.so: $(IOBJ)
	gcc -shared -o integrate.so $(IOBJ)
	rm -f *.o


#Integrate
realtype_math.o: $(SRCDIR)/realtype_math.c $(SRCDIR)/realtype_math.h
	gcc $(FLAGS) -c $(SRCDIR)/realtype_math.c

shared.o: $(SRCDIR)/shared.c $(SRCDIR)/shared.h
	gcc $(FLAGS) -c $(SRCDIR)/shared.c

events.o: $(SRCDIR)/events.c $(SRCDIR)/events.h
	gcc $(FLAGS) -c $(SRCDIR)/events.c

ode.o: $(SRCDIR)/ode.c $(SRCDIR)/ode.h
	gcc $(FLAGS) -c $(SRCDIR)/ode.c

dae.o: $(SRCDIR)/dae.c $(SRCDIR)/dae.h
	gcc $(FLAGS) -c $(SRCDIR)/dae.c

integrate.o: $(SRCDIR)/integrate.c $(SRCDIR)/integrate.h
	gcc $(FLAGS) -c $(SRCDIR)/integrate.c

clean:
	rm -f *.o *.so
