/*
 * dns_lookup.c
 *
 * This program uses the dig command to lookup a DNS record.
 *
 * Author: Thomas Vincent
 * Date: 2023-05-28
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

#define MAX_COMMAND_LENGTH 1024

void print_error(const char* message) {
  fprintf(stderr, "ERROR: %s\n", message);
}

void print_command(const char* command) {
  printf("Running command: %s\n", command);
}

int run_command(const char* command) {
  return system(command);
}

char* read_command_output() {
  char* output = NULL;
  size_t output_size = 0;
  ssize_t bytes_read = getline(&output, &output_size, stdin);
  if (bytes_read < 0) {
    print_error("Could not read output of command");
    free(output);
    return NULL;
  }
  return output;
}

char* parse_output(const char* output, const char* expected_address) {
  char* record = NULL;
  char* address = NULL;
  char* colon = strchr(output, ':');
  if (colon == NULL) {
    print_error("Could not find colon in output of command");
    return NULL;
  }
  record = strndup(output, colon - output);
  address = strndup(colon + 1, strlen(output) - (colon - output) - 1);

  if (expected_address != NULL && strcmp(expected_address, address) != 0) {
    print_error("Expected address not found");
    free(record);
    free(address);
    return NULL;
  }

  printf("DNS %s - %s\n", record, address);
  free(record);
  free(address);

  return output;
}

int main(int argc, char* argv[]) {
  // Get the command line arguments.
  char* query_address = NULL;
  int server_port = 53;
  char* record_type = "A";

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
  snprintf(command_line, sizeof(command_line), "dig @%s -p %d %s -t %s", query_address, server_port, record_type, "");
  print_command(command_line);
  int status = run_command(command_line);

  // Check the status of the command.
  if (status != 0) {
    printf("ERROR: Command failed with status %d\n", status);
    return 1;
  }

  // Get the output of the command.
  char* output = read_command_output();
  if (output == NULL) {
    return 1;
  }

  // Parse the output of the command.
  if (parse_output(output, NULL) == NULL) {
    free(output);
    return 1;
  }

  // Return the status.
  if (warning_interval > 0 && status >= warning_interval) {
    return 2;
  } else if (critical_interval > 0 && status >= critical_interval) {
    return 3;
  } else {
    return 0;
  }
}
