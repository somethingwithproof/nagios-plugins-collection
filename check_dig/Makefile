# Makefile for dns_lookup

CC = gcc
CFLAGS = -Wall -Wextra -pedantic

dns_lookup: dns_lookup.c
	$(CC) $(CFLAGS) -o dns_lookup dns_lookup.c

dns_lookup_test: dns_lookup_test.c
	$(CC) $(CFLAGS) -o dns_lookup_test dns_lookup_test.c

test: dns_lookup_test
	./dns_lookup_test

clean:
	rm -f dns_lookup dns_lookup_test
