#include "options.h"
#include <errno.h>
#include <string.h>
#include <unistd.h>
#include <stdio.h>
#include <stdlib.h>

// argc: Number of command-line arguments
// argv: Array of command-line arguments
// ret: A pointer to a struct optionInfo that holds information about the parsed options
void 
parseOptions(int argc, char **argv, struct optionInfo* ret)
{
    /* Check arguments. */
    bool valid = true;
    long long nbytes = 0;

    bool rdrand = true; // default
    bool lrand48_r = false;
    bool file = false;
    char* path = "";

    bool stdio = true; // default
    bool N = false;
    unsigned int nInt = 0;
  
    int c;

    // While there are i/o arguments
    while((c = getopt(argc, argv, ":i:o:")) != -1) 
    {
        switch(c)
        {
            case 'i':
                // rdrand (default)
                if(strcmp(optarg, "rdrand") == 0)
                {
                    break;
                }

                // lrand48_r
                else if(strcmp(optarg, "lrand48_r") == 0)
                {
	                rdrand = false;
	                lrand48_r = true;
	                file = false;
                }
      
                // /F
                else if(optarg[0] == '/')
                {
	                rdrand = false;
	                lrand48_r = false;
	                file = true;
	                path = optarg;
                }
      
                else
                {
                    fprintf(stderr, "-i requires an operand 'rdrand', 'lrand48_r', '/...'\n");
                    valid = false;
                }

                break;

            case 'o':
                // stdio (default)
                if(strcmp(optarg, "stdio") == 0)
                {
                    break;
                }

                // N (positive decimal integer)
                else 
                {
                    stdio = false;
                    N = true;
                    char *endptr;
                    errno = 0;
                    // Convert the string optarg to an unsigned long integer (nInt)
                    // &endptr is used to store the pointer to the first character 
                    // after the numerical value in the string
	                nInt = strtoul(optarg, &endptr, 10);

                    // If error
                    if(errno)
                    {
                        perror(optarg);
                        valid = false;
                    }
                    
                    // No error, additional validation
                    else
                    { 
                        // Checks if the conversion consumed the entire string
                        // *endptr is the null terminator
                        // And if valid was already valid
                        valid = !*endptr && 0 <= nbytes && valid;
                    }

                    // No operand provided or the provided operand isn't a valid positive integer
	                if(nInt == 0)
                    {
                        fprintf(stderr, "-o requires a positive integer operand\n");
                        valid = false;
	                }
                }

                break;
            
            // Required argument for an option is missing
            case ':':
                fprintf(stderr, "Option -%c requires an operand\n", optopt);
                valid = false;
                break;
    
            // Unrecognized option
            case '?':
                fprintf(stderr, "Unrecognized option: '-%c'\n", optopt);
                valid = false;
                break;
            }
        }

        // optind: The index of the next element in the argv array to be processed by getopt
        // argc - 1: The index of the last element in the argv array
        // If additional arguments present or not valid
        if(optind != argc - 1 || valid == false)
        {
            valid = false;
        } 
  
        // Original required number input
        else 
        {
            char *endptr;
            errno = 0;
            // Uses strtoll to convert the string argv[optind] to a long long integer (nbytes)
            // Base 10 (decimal) conversion
            nbytes = strtoll(argv[optind], &endptr, 10);

            // If error
            if(errno) 
            {
                perror(argv[optind]);
                valid = false;
            }
            
            // No error, additional validation
            else 
            {
                // Checks if the conversion consumed the entire string
                // *endptr is the null terminator
                // And if valid was already valid
                valid = !*endptr && 0 <= nbytes && valid;
            }
        }

    // Set values of the struct optionInfo based on the results of parsing command-line options
    ret->valid = valid;
    ret->rdrand = rdrand;
    ret->lrand48_r = lrand48_r;
    ret->file = file;
    ret->stdio = stdio;
    ret->N = N;
    ret->path = path;
    ret->nInt = nInt;
    ret->nbytes = nbytes;
}