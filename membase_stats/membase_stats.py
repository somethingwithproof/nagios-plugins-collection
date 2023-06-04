#!/usr/bin/env python3
"""
membase_stats.py

Description:
A script to fetch and process Membase stats.

Author:
Thomas Vincent

License:
MIT License
"""

import getopt
import sys
import urllib.request
import base64
import json
from collections import defaultdict


class MembaseStats:
    RESOURCE_NAME_MAPPING = {
        "curr_items": {"description": "Current active items", "unit": "", "type": "current", "name": "current_active_items"},
        "curr_items_tot": {"description": "Current total items", "unit": "", "type": "current", "name": "current_total_items"},
        "ep_num_active_non_resident": {"description": "Current non-resident item", "unit": "", "type": "current", "name": "num_active_items_not_in_RAM"},
        "get_hits": {"description": "Number of fetches", "unit": "", "type": "cumulative", "name": "num_successful_get"},
        "ep_bg_fetched": {"description": "Number of items fetched from the disk", "unit": "", "type": "cumulative", "name": "num_items_get_from_disk"},
        "ep_num_non_resident": {"description": "Number of items stored only on disk, not cached in RAM", "unit": "", "type": "current", "name": "num_total_items_not_in_RAM"},
        "ep_total_enqueued": {"description": "Total number of items queued for storage", "unit": "", "type": "cumulative", "name": "total_items_enqueued_for_storage"},
        "ep_total_new_items": {"description": "Total number of persisted new items", "unit": "", "type": "cumulative", "name": "num_persisted_new_items"},
        "get_misses": {"description": "Number of unsuccessful fetches", "unit": "", "type": "cumulative", "name": "num_unsuccessful_get"},
        "mem_used": {"description": "Current memory usage", "unit": "B", "type": "current", "name": "memory_usage"},
        "ep_total_cache_size": {"description": "Cache size", "unit": "B", "type": "current", "name": "total_cache_size"},
        "bytes_written": {"description": "Number of bytes written", "unit": "B", "type": "cumulative", "name": "bytes_written"},
        "ep_queue_size": {"description": "Number of items in the disk written queue", "unit": "", "type": "current", "name": "disk_write_queue_size"},
        "ep_io_num_write": {"description": "Number of io write operations", "unit": "", "type": "cumulative", "name": "num_io_write_operations"},
        "ep_io_num_read": {"description": "Number of io read operations", "unit": "", "type": "cumulative", "name": "num_io_read_operations"},
        "ep_total_persisted": {"description": "Total number of persisted items", "unit": "", "type": "cumulative", "name": "num_items_persisted"},
        "ep_total_del_items": {"description": "Total number of persisted deletions", "unit": "", "type": "cumulative", "name": "num_items_deleted"},
        "ep_item_commit_failed": {"description": "Number of times a transaction failed to commit due to storage errors", "unit": "", "type": "cumulative", "name": "num_failed_transactions"},
        "ep_expired": {"description": "Number of times an item was expired", "unit": "", "type": "cumulative", "name": "expired_items"},
    }

    def __init__(self):
        self.data_file_name = "./membase_stats_data"
        self.prev_stats = set()
        self.d_stats = defaultdict(int)
        self.list_stats = False
        self.url = None
        self.username = None
        self.password = None

    def before_work(self):
        try:
            with open(self.data_file_name, 'r') as file:
                self.prev_stats = set(line.split()[0] for line in file)
        except FileNotFoundError:
            pass

    def after_work(self):
        try:
            with open(self.data_file_name, 'w') as file:
                file.writelines(f"{key} {self.prev_stats[key]}\n" for key in self.prev_stats)
        except IOError:
            pass

    def usage(self):
        print("usage:\n\tmembase_stats.py [-l|--list|-h|--help|--url=URL|--username=USER|--password=PASS]\n\tmembase_stats.py metric|all\n\t\tWhere metric is one of the metrics shown with a -l|--list")

    def get_status(self, src_url, remote_user, remote_pass):
        request = urllib.request.Request(src_url)
        base64string = base64.b64encode(f'{remote_user}:{remote_pass}'.encode()).decode()
        request.add_header("Authorization", f"Basic {base64string}")
        result = urllib.request.urlopen(request)
        content = result.read()
        parsed = json.loads(content)["op"]["samples"]
        self.d_stats = defaultdict(int, {key: parsed[key][-1] for key in parsed})

    def main(self):
        try:
            opts, args = getopt.getopt(sys.argv[1:], "lh", ["list", "help", "url=", "username=", "password="])
        except getopt.GetoptError as err:
            print(str(err))
            self.usage()
            sys.exit(2)

        self.before_work()

        for opt, arg in opts:
            if opt == "--url":
                self.url = arg
            elif opt == "--username":
                self.username = arg
            elif opt == "--password":
                self.password = arg
            elif opt in ("-l", "--list"):
                self.list_stats = True
            elif opt in ("-h", "--help"):
                self.usage()
                sys.exit(0)

        self.get_status(src_url=self.url, remote_user=self.username, remote_pass=self.password)

        if self.list_stats:
            print("\n".join(self.d_stats.keys()))
            sys.exit(0)

        perf_data = "Membase_Stats:OK | "
        keys = args if args and args[0] != "all" else self.d_stats.keys()

        data_strings = [self.process_data(key) for key in keys]
        perf_data += "".join(data_strings)
        perf_data += self.get_resident_ratio()
        perf_data += self.get_cache_miss_ratio()
        perf_data += self.get_replica_resident_ratio()
        print(perf_data)

        self.after_work()

    def process_data(self, key):
        if key in self.RESOURCE_NAME_MAPPING:
            resource_mapping = self.RESOURCE_NAME_MAPPING[key]
            resource_type = resource_mapping.get('type', 'current')
            resource_name = resource_mapping.get('name', key)
            if resource_type == "cumulative":
                diff = self.d_stats[key] - self.prev_stats.get(key, 0)
                self.prev_stats[key] = self.d_stats[key]
                return f"{resource_name}={diff}{resource_mapping['unit']} "
            return f"{resource_name}={self.d_stats[key]}{resource_mapping['unit']} "
        return f"{key}={self.d_stats[key]} "

    def get_resident_ratio(self):
        if 'ep_num_active_non_resident' in self.d_stats and 'curr_items' in self.d_stats and self.d_stats['curr_items'] > 0:
            resident_item_ratio = 100 - float(self.d_stats['ep_num_active_non_resident']) / float(self.d_stats['curr_items']) * 100
            resident_item_ratio = max(resident_item_ratio, 0)
            return f"resident_item_ratio={resident_item_ratio}% "
        return ""

    def get_cache_miss_ratio(self):
        if 'get_hits' in self.d_stats and 'ep_bg_fetched' in self.d_stats and self.d_stats['get_hits'] > 0:
            cache_miss_ratio = float(self.d_stats['ep_bg_fetched']) / float(self.d_stats['get_hits']) * 100
            return f"cache_miss_ratio={cache_miss_ratio}% "
        return ""

    def get_replica_resident_ratio(self):
        if 'ep_num_non_resident' in self.d_stats and 'curr_items_tot' in self.d_stats and 'curr_items' in self.d_stats and 'ep_num_active_non_resident' in self.d_stats:
            total_items_diff = self.d_stats['curr_items_tot'] - self.d_stats['curr_items']
            if total_items_diff > 0:
                numerator = self.d_stats['ep_num_non_resident'] - self.d_stats['ep_num_active_non_resident']
                denominator = total_items_diff
                replica_resident_ratio = 100 - (numerator / denominator) * 100
                replica_resident_ratio = max(replica_resident_ratio, 0)
                return f"replica_resident_ratio={replica_resident_ratio}% "
        return ""


if __name__ == "__main__":
    stat = MembaseStats()
    stat.main()
