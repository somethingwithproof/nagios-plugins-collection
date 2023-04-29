// Test that the program can lookup the A record for www.google.com and print the output.
void test_lookup_and_print_www_google_com() {
  char *output = dns_lookup("www.google.com");
  assert(output != NULL);
  printf("DNS lookup for www.google.com: %s\n", output);
}

// Test that the program can lookup the CNAME record for www.google.com and print the output.
void test_lookup_and_print_www_google_com_cname() {
  char *output = dns_lookup("www.google.com", "CNAME");
  assert(output != NULL);
  printf("DNS lookup for www.google.com (CNAME): %s\n", output);
}

// Test that the `main()` function returns 0 if the query address is not specified.
void test_main_no_query_address() {
  int expected_status = 1;
  int actual_status = main(0, NULL);
  assert(expected_status == actual_status);
}

// Test that the `main()` function returns 0 if the query address is specified.
void test_main_with_query_address() {
  int expected_status = 0;
  int actual_status = main(1, (char *[]){"www.google.com"});
  assert(expected_status == actual_status);
}

// Test that the `get_command_line()` function returns a valid command line.
void test_get_command_line() {
  char *expected_command_line = "dig @8.8.8.8 -p 53 www.google.com -t A";
  char *actual_command_line = get_command_line("www.google.com");
  assert(strcmp(expected_command_line, actual_command_line) == 0);
}

// Test that the `run_command()` function returns 0 if the command succeeds.
void test_run_command_success() {
  int expected_status = 0;
  int actual_status = run_command("echo hello");
  assert(expected_status == actual_status);
}

// Test that the `run_command()` function returns 1 if the command fails.
void test_run_command_failure() {
  int expected_status = 1;
  int actual_status = run_command("echo hello > /dev/null");
  assert(expected_status == actual_status);
}
