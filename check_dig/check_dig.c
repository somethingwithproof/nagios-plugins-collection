/*
 * dns_lookup.c
 *
 * This program uses the dig command to lookup a DNS record.
 *
 * Author: Thomas Vincent
 * Date: 2023-04-28
 *
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

int main(int argc, char *argv[]) {
  // Get the command line arguments.
  char *query_address = argv[1];
  int server_port = 53;
  char *record_type = "A";

  for (int i = 2; i < argc; i++) {
    if (strcmp(argv[i], "-p") == 0) {
      server_port = atoi(argv[i + 1]);
      i++;
    } else if (strcmp(argv[i], "-t") == 0) {
      record_type = argv[i + 1];
      i++;
    }
  }

  // Check if the query address is specified.
  if (query_address == NULL) {
    printf("ERROR: No query address specified\n");
    return 1;
  }

  // Run the command.
  char *command_line = malloc(1024);
  sprintf(command_line, "dig @%s -p %d %s -t %s", query_address, server_port, record_type, "");
  if (verbose) {
    printf("Running command: %s\n", command_line);
  }
  int status = system(command_line);
  free(command_line);

  // Check the status of the command.
  if (status != 0) {
    printf("ERROR: Command failed with status %d\n", status);
    return 1;
  }

  // Get the output of the command.
  char *output = NULL;
  size_t output_size = 0;
  getline(&output, &output_size, stdin);
  if (output == NULL) {
    printf("ERROR: Could not read output of command\n");
    return 1;
  }

  // Parse the output of the command.
  char *record = NULL;
  char *address = NULL;
  char *colon = strchr(output, ':');
  if (colon == NULL) {
    printf("ERROR: Could not find colon in output of command\n");
    return 1;
  }
  record = strndup(output, colon - output);
  address = strndup(colon + 1, strlen(output) - (colon - output) - 1);

  // Check if the expected address was found.
  if (expected_address != NULL && strcmp(expected_address, address) != 0) {
    printf("ERROR: Expected address %s not found\n", expected_address);
    return 1;
  }

  // Print the output.
  if (verbose) {
    printf("Output: %s\n", output);
  }
  printf("DNS %s - %s\n", record, address);

  // Return the status.
  if (warning_interval > 0 && status >= warning_interval) {
    return 2;
  } else if (critical_interval > 0 && status >= critical_interval) {
    return 3;
  } else
    return 0;
}
