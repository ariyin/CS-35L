# Make x86-64 random byte generators.

# Copyright 2015, 2020, 2021 Paul Eggert

# This program is free software: you can redistribute it and/or
# mod@ify it under the terms of the GNU General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.

# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program.  @if not, see <http://www.gnu.org/licenses/>.  */

# Optimization level.  Change this -O2 to -Og or -O0 or whatever.
OPTIMIZE =

# The C compiler and its options.
CC = gcc
CFLAGS = $(OPTIMIZE) -g3 -Wall -Wextra -fanalyzer \
  -march=native -mtune=native -mrdrnd
  
# The archiver command, its options and filename extension.
TAR = tar
TARFLAGS = --gzip --transform 's,^,randall/,'
TAREXT = tgz

default: randall

randall: rand64-hw.o rand64-sw.o output.o options.o randall.o
	$(CC) $(CFLAGS) $^ -o $@

options.o: options.c options.h
	$(CC) $(CFLAGS) options.c -o options.o -c

output.o: output.c output.h
	$(CC) $(CFLAGS) output.c -o output.o -c

rand64-hw.o: rand64-hw.c rand64-hw.h
	$(CC) $(CFLAGS) rand64-hw.c -o rand64-hw.o -c

rand64-sw.o: rand64-sw.c rand64-sw.h
	$(CC) $(CFLAGS) rand64-sw.c -o rand64-sw.o -c

randall.o: randall.c rand64-hw.h
	$(CC) $(CFLAGS) randall.c -o randall.o -c

assignment: randall-assignment.$(TAREXT)
assignment-files = COPYING Makefile randall.c
randall-assignment.$(TAREXT): $(assignment-files)
	$(TAR) $(TARFLAGS) -cf $@ $(assignment-files)

submission-tarball: randall-submission.$(TAREXT)
submission-files = $(assignment-files) \
  notes.txt options.c options.h output.c output.h rand64-hw.c rand64-hw.h rand64-sw.c \
  rand64-sw.h randall.c
randall-submission.$(TAREXT): $(submission-files)
	$(TAR) $(TARFLAGS) -cf $@ $(submission-files)

repository-tarball:
	$(TAR) -czf randall-git.tgz .git

.PHONY: default clean assignment submission-tarball repository-tarball

clean:
	rm -f *.o *.$(TAREXT) randall

testNum = 10
check: randall
	@if [ `./randall $(testNum) | wc -c` -eq $(testNum) ]; \
		then echo "./randall $(testNum) - Success"; \
		else echo "./randall $(testNum) - Fail"; \
	fi

	@if [ `./randall 0 | wc -c` -eq 0 ]; \
		then echo "./randall 0 - Success"; \
		else echo "./randall 0 - Fail"; \
	fi

	@if [ `./randall -i rdrand $(testNum) | wc -c` -eq $(testNum) ]; \
		then echo "./randall -i rdrand $(testNum) - Success"; \
		else echo "./randall -i rdrand $(testNum) - Fail"; \
	fi

	@if [ `./randall -i lrand48_r $(testNum) | wc -c` -eq $(testNum) ]; \
		then echo "./randall -i lrand48_r $(testNum) - Success"; \
		else echo "./randall -i lrand48_r $(testNum) - Fail"; \
	fi

	@if [ `./randall -i /dev/random $(testNum) | wc -c` -eq $(testNum) ]; \
		then echo "./randall -i /dev/random $(testNum) - Success"; \
		else echo "./randall -i /dev/random $(testNum) - Fail"; \
	fi

	@if [ `./randall -o stdio $(testNum) | wc -c` -eq $(testNum) ]; \
		then echo "./randall -o stdio $(testNum) - Success"; \
		else echo "./randall -o stdio $(testNum) - Fail"; \
	fi

	@if [ `./randall -o 1 $(testNum) | wc -c` -eq $(testNum) ]; \
		then echo "./randall -o 1 $(testNum) - Success"; \
		else echo "./randall -o 1 $(testNum) - Fail"; \
	fi

	@if [ `./randall -o $(testNum) $(testNum) | wc -c` -eq $(testNum) ]; \
		then echo "./randall -o $(testNum) $(testNum) - Success"; \
		else echo "./randall -o $(testNum) $(testNum) - Fail"; \
	fi

	@if [ `./randall -o 100 $(testNum) | wc -c` -eq $(testNum) ]; \
		then echo "./randall -o 100 $(testNum) - Success"; \
		else echo "./randall -o 100 $(testNum) - Fail"; \
	fi

	@if [ `./randall -i rdrand -o stdio $(testNum) | wc -c` -eq $(testNum) ]; \
		then echo "./randall -i rdrand -o stdio $(testNum) - Success"; \
		else echo "./randall -i rdrand -o stdio $(testNum) - Fail"; \
	fi

	@if [ `./randall -i rdrand -o 1 $(testNum) | wc -c` -eq $(testNum) ]; \
		then echo "./randall -i rdrand -o 1 $(testNum) - Success"; \
		else echo "./randall -i rdrand -o 1 $(testNum) - Fail"; \
	fi

	@if [ `./randall -i rdrand -o $(testNum) $(testNum) | wc -c` -eq $(testNum) ]; \
		then echo "./randall -i rdrand -o $(testNum) $(testNum) - Success"; \
		else echo "./randall -i rdrand -o $(testNum) $(testNum) - Fail"; \
	fi

	@if [ `./randall -i rdrand -o 100 $(testNum) | wc -c` -eq $(testNum) ]; \
		then echo "./randall -i rdrand -o 100 $(testNum) - Success"; \
		else echo "./randall -i rdrand -o 100 $(testNum) - Fail"; \
	fi

	@if [ `./randall -i lrand48_r -o stdio $(testNum) | wc -c` -eq $(testNum) ]; \
		then echo "./randall -i lrand48_r -o stdio $(testNum) - Success"; \
		else echo "./randall -i lrand48_r -o stdio $(testNum) - Fail"; \
	fi

	@if [ `./randall -i lrand48_r -o 1 $(testNum) | wc -c` -eq $(testNum) ]; \
		then echo "./randall -i lrand48_r -o 1 $(testNum) - Success"; \
		else echo "./randall -i lrand48_r -o 1 $(testNum) - Fail"; \
	fi

	@if [ `./randall -i lrand48_r -o $(testNum) $(testNum) | wc -c` -eq $(testNum) ]; \
		then echo "./randall -i lrand48_r -o $(testNum) $(testNum) - Success"; \
		else echo "./randall -i lrand48_r -o $(testNum) $(testNum) - Fail"; \
	fi

	@if [ `./randall -i lrand48_r -o 100 $(testNum) | wc -c` -eq $(testNum) ]; \
		then echo "./randall -i lrand48_r -o 100 $(testNum) - Success"; \
		else echo "./randall -i lrand48_r -o 100 $(testNum) - Fail"; \
	fi

	@if [ `./randall -i /dev/random -o stdio $(testNum) | wc -c` -eq $(testNum) ]; \
		then echo "./randall -i /dev/random -o stdio $(testNum)  - Success"; \
		else echo "./randall -i /dev/random -o stdio $(testNum)  - Fail"; \
	fi

	@if [ `./randall -i /dev/random -o 1 $(testNum) | wc -c` -eq $(testNum) ]; \
		then echo "./randall -i /dev/random -o 1 $(testNum) - Success"; \
		else echo "./randall -i /dev/random -o 1 $(testNum) - Fail"; \
	fi

	@if [ `./randall -i /dev/random -o $(testNum) $(testNum) | wc -c` -eq $(testNum) ]; \
		then echo "./randall -i /dev/random -o $(testNum) $(testNum)  - Success"; \
		else echo "./randall -i /dev/random -o $(testNum) $(testNum)  - Fail"; \
	fi

	@if [ `./randall -i /dev/random -o 100 $(testNum) | wc -c` -eq $(testNum) ]; \
		then echo "./randall -i /dev/random -o 100 $(testNum) - Success"; \
		else echo "./randall -i /dev/random -o 100 $(testNum) - Fail"; \
	fi

	@if [ `./randall -i $(testNum) | wc -c` -eq $(testNum) ]; \
		then echo "./randall -i $(testNum) - Success"; \
		else echo "./randall -i $(testNum) - Fail"; \
	fi

	@if [ `./randall -o $(testNum) | wc -c` -eq $(testNum) ]; \
		then echo "./randall -o $(testNum) - Success"; \
		else echo "./randall -o $(testNum) - Fail"; \
	fi

	@if [ `./randall -i rdrand -w $(testNum) | wc -c` -eq $(testNum) ]; \
		then echo "./randall -i rdrand -w $(testNum) - Success"; \
		else echo "./randall -i rdrand -w $(testNum) - Fail"; \
	fi

	@if [ `./randall -o stdio -w $(testNum) | wc -c` -eq $(testNum) ]; \
		then echo "./randall -o stdio -w $(testNum) - Success"; \
		else echo "./randall -o stdio -w $(testNum) - Fail"; \
	fi

	@if [ `./randall -o 0 $(testNum) | wc -c` -eq $(testNum) ]; \
		then echo "./randall -o 0 $(testNum) - Success"; \
		else echo "./randall -o 0 $(testNum) - Fail"; \
	fi

	@if [ `./randall -o $(testNum) -$(testNum) | wc -c` -eq $(testNum) ]; \
		then echo "./randall -o $(testNum) -$(testNum) - Success"; \
		else echo "./randall -o $(testNum) -$(testNum) - Fail"; \
	fi