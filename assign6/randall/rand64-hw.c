#include "rand64-hw.h"
#include <immintrin.h>
#include <cpuid.h>
#include <time.h>

/* Hardware implementation. */

/* Description of the current CPU. */
struct cpuid { unsigned eax, ebx, ecx, edx; };

/* Return information about the CPU. See <http://wiki.osdev.org/CPUID>. */
static struct cpuid
cpuid (unsigned int leaf, unsigned int subleaf)
{
    struct cpuid result;
    asm ("cpuid"
        : "=a" (result.eax), "=b" (result.ebx),
          "=c" (result.ecx), "=d" (result.edx)
        : "a" (leaf), "c" (subleaf));
    return result;
}

/* Return true if the CPU supports the RDRAND instruction. */
bool
rdrand_supported (void)
{
    struct cpuid extended = cpuid (1, 0);
    return (extended.ecx & bit_RDRND) != 0;
}

/* Initialize the hardware rand64 implementation. */
void
hardware_rand64_init (void)
{
}

/* Return a random value, using hardware operations. */
unsigned long long
hardware_rand64 (void)
{
    unsigned long long int x;

    /* Work around GCC bug 107565 <https://gcc.gnu.org/bugzilla/show_bug.cgi?id=107565>. */
    x = 0;

    while (! _rdrand64_step (&x))
        continue;
    return x;
}

/* Finalize the hardware rand64 implementation. */
void
hardware_rand64_fini (void)
{
}

/* Initialize the buffer. */
static struct drand48_data buffer;

/* Initialize the hardware rand48 implementation. */
void
hardware_rand48_init (void)
{
    // Initialize the random number generator state (buffer) based on the current time
    srand48_r(time(NULL), &buffer);
}

/* Return a random value, using hardware operations. */
unsigned long long
hardware_rand48 (void)
{
    long int x;

    // Reinitialize the random number generator state with the current time and buffer
    srand48_r(time(NULL), &buffer); 

    // Obtain a random long integer (x) based on the updated state
    lrand48_r(&buffer, &x); 
    
    return (unsigned long long) x;
}

/* Finalize the hardware rand64 implementation. */
void
hardware_rand48_fini (void)
{
}