#include "rand64-sw.h"
#include <stdio.h>
#include <stdlib.h>

/* Software implementation. */

/* Input stream containing random bytes. */
static FILE *urandstream;

/* Initialize the software rand64 implementation. */
int
software_rand64_init (char* path)
{
    urandstream = fopen (path, "r");
    if (! urandstream)
    {
        fprintf(stderr, "No such file or directory\n");
        return 1;
    }
    return 0;
}

/* Return a random value, using software operations. */
unsigned long long
software_rand64 (void)
{
    unsigned long long int x;
    if (fread (&x, sizeof x, 1, urandstream) != 1)
    {
        fprintf(stderr, "No such file or directory\n");
        abort ();
    }
    return x;
}

/* Finalize the software rand64 implementation. */
void
software_rand64_fini (void)
{
    fclose (urandstream);
}