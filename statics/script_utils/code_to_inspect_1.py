    def randrange(self, start, stop=None, step=1):

        """Choose a random item from range(start, stop[, step]).



        This fixes the problem with randint() which includes the

        endpoint; in Python this is usually not what you want.



        """



        # This code is a bit messy to make it fast for the

        # common case while still doing adequate error checking.

        istart = int(start)

        if istart != start:

            raise ValueError("non-integer arg 1 for randrange()")

        if stop is None:

            if istart > 0:

                return self._randbelow(istart)

            raise ValueError("empty range for randrange()")



        # stop argument supplied.

        istop = int(stop)

        if istop != stop:

            raise ValueError("non-integer stop for randrange()")

        width = istop - istart

        if step == 1 and width > 0:

            return istart + self._randbelow(width)

        if step == 1:

            raise ValueError("empty range for randrange() (%d, %d, %d)" % (istart, istop, width))



        # Non-unit step argument supplied.

        istep = int(step)

        if istep != step:

            raise ValueError("non-integer step for randrange()")

        if istep > 0:

            n = (width + istep - 1) // istep

        elif istep < 0:

            n = (width + istep + 1) // istep

        else:

            raise ValueError("zero step for randrange()")



        if n <= 0:

            raise ValueError("empty range for randrange()")



        return istart + istep * self._randbelow(n)

