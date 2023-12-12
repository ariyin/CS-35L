#ifndef SW_H
#define SW_H

/* Initialize the software rand64 implementation. */
int
software_rand64_init (char* path);

/* Return a random value, using software operations. */
unsigned long long
software_rand64 (void);

/* Finalize the software rand64 implementation. */
void
software_rand64_fini (void);

#endif // SW_H