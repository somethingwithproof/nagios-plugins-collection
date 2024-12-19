/*
 * dns_lookup.c
 *
 * This program uses the dig command to lookup a DNS record.
 *
 * Copyright (c) 2023-2024 Thomas Vincent
 *
 * Permission is hereby granted, free of charge, to any person obtaining a copy
 * of this software and associated documentation files (the "Software"), to deal
 * in the Software without restriction, including without limitation the rights
 * to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
 * copies of the Software, and to permit persons to whom the Software is
 * furnished to do so, subject to the following conditions:
 *
 * The above copyright notice and this permission notice shall be included in all
 * copies or substantial portions of the Software.
 *
 * THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
 * IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
 * FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
 * AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
 * LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
 * OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
 * SOFTWARE.
 */
 * Usage:
 *
 *   dns_lookup <query_address> [-p <server_port>] [-t <record_type>]
 *
 * Options:
 *
 *   -p <server_port>: The port number of the DNS server.
 *   -t <record_type>: The type of DNS record to lookup.
 *
 * Example:
 *
 *   dns_lookup www.google.com
 *
 * This will lookup the A record for www.google.com.
 */

#include <stdlib.h>
#include <stdio.h>
#include <string.h>

#define MAX_COMMAND_LENGTH 1024

// Function to print errors to stderr
void print_error(const char *message) {
  fprintf(stderr, "ERROR: %s\n", message);
}

// Function to print the command being executed (for debugging)
void print_command(const char *command) {
  printf("Running command: %s\n", command);
}

// Function to execute a command using system()
int run_command(const char *command) {
  return system(command);
}

// Function to read the output of a command (from stdout)
// Note: This function is not used in the current code and can be removed
char *read_command_output() {
  char *output = NULL;
  size_t output_size = 0;
  ssize_t bytes_read = getline(&output, &output_size, stdin);
  if (bytes_read < 0) {
    print_error("Could not read output of command");
    free(output);
    return NULL;
  }
  return output;
}

// Function to parse the output of the dig command
// This function currently just prints the record and address. 
// It can be extended to return specific information or perform more advanced parsing.
char *parse_output(const char *output, const char *expected_address) {
  char *record = NULL;
  char *address = NULL;
  char *colon = strchr(output, ':');
  if (colon == NULL) {
    print_error("Could not find colon in output of command");
    return NULL;
  }
  record = strndup(output, colon - output);
  address = strndup(colon + 1, strlen(output) - (colon - output) - 2); // -2 to remove newline and space

  if (expected_address != NULL && strcmp(expected_address, address) != 0) {
    print_error("Expected address not found");
    free(record);
    free(address);
    return NULL;
  }

  printf("DNS %s - %s\n", record, address);
  free(record);
  free(address);

  return (char *)output; // Cast to avoid warning
}

int main(int argc, char *argv[]) {
  // Get the command line arguments.
  char *query_address = NULL;
  int server_port = 53;
  char *record_type = "A";

  for (int i = 1; i < argc; i++) {
    if (strcmp(argv[i], "-p") == 0) {
      if (i + 1 < argc) {
        server_port = atoi(argv[i + 1]);
        i++;
      } else {
        print_error("No server port specified");
        return 1;
      }
    } else if (strcmp(argv[i], "-t") == 0) {
      if (i + 1 < argc) {
        record_type = argv[i + 1];
        i++;
      } else {
        print_error("No record type specified");
        return 1;
      }
    } else {
      if (query_address == NULL) {
        query_address = argv[i];
      } else {
        print_error("Too many arguments");
        return 1;
      }
    }
  }

  // Check if the query address is specified.
  if (query_address == NULL) {
    print_error("No query address specified");
    return 1;
  }

  // Run the command.
  char command_line[MAX_COMMAND_LENGTH];
  snprintf(command_line, sizeof(command_line), "dig @%s -p %d %s +short", 
           query_address, server_port, record_type);
  print_command(command_line);
  int status = run_command(command_line);

  // Check the status of the command.
  if (status != 0) {
    fprintf(stderr, "ERROR: Command failed with status %d\n", status);
    return 1;
  }

  // Parse the output of the command.
  // Since we're using `+short`, dig will output only the IP address
  char output[MAX_COMMAND_LENGTH];
  fgets(output, sizeof(output), stdin); 
  parse_output(output, NULL); // You can add expected address checking here

  return 0; 
}
