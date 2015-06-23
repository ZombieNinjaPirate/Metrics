#!/usr/bin/env python


import argparse
import os
import psutil
import socket
import time
from Bifrozt.CPU import Proc
from Bifrozt.MEM import Ram
from influxdb.influxdb08 import InfluxDBClient


__author__ = 'Are Hansen'
__date__ = '2015, June 18'
__version__ = '0.0.5'


def parse_args():
    """Command line options."""
    parser = argparse.ArgumentParser(description='Send data to InfluxDB')
    xdb = parser.add_argument_group('- InfluxDB options')
    dbp = 8086
    xdb.add_argument(
                    '-H', 
                    dest='db_host', 
                    help='InfluxDB host IPv4 or FQDN',
                    required=True
                    )
    xdb.add_argument(
                    '-D',
                    dest='db_name',
                    help='Database name',
                    required=True
                    )
    xdb.add_argument(
                    '-U',
                    dest='db_user',
                    help='Database user name',
                    required=True
                    )
    xdb.add_argument(
                    '-A',
                    dest='auth_file',
                    help='File with database user authentication',
                    nargs='?',
                    type=argparse.FileType('r'),
                    required=True
                    )
    xdb.add_argument(
                    '-p', 
                    dest='db_port', 
                    help='InfluxDB API port (default: {0})'.format(dbp),
                    type=int,
                    default=dbp
                    )
    met = parser.add_argument_group('- Metric options')
    met.add_argument(
                    '-mc',
                    dest='cpu',
                    help='CPU load',
                    action='store_true'
                    )
    met.add_argument(
                    '-mr',
                    dest='ram',
                    help='Percentage of used RAM',
                    action='store_true'
                    )
    met.add_argument(
                    '-mn',
                    dest='inet',
                    help='Total bytes sent and received',
                    action='store_true'
                    )

    args = parser.parse_args()
    return args


def cpu_load():
    metric = "cpu_load.{0}".format(socket.gethostname())
    json_body =  [
    {
        "name": metric,
        "columns": [
            "time",
            "host",
            "value"
        ],
        "points": [
            [
                float(time.time()),
                socket.gethostname(),
                cpu.use(2)
            ]
        ]
      }
    ]
    return json_body


def ram_usage():
    metric = "ram_prcnt.{0}".format(socket.gethostname())
    json_body = [
    {
        "name": metric,
        "columns": [
            "time",
            "host",
            "value"
        ],
        "points": [
            [
                float(time.time()),
                socket.gethostname(),
                ram.use()
            ]
        ]
      }
    ]
    return json_body


def inet_bytes():
    metric = "inet_io.{0}".format(socket.gethostname())
    json_body = [
    {
        "name": metric,
        "columns": [
            "time",
            "host",
            "bytes_sent",
            "byte_received"
        ],
        "points": [
            [
                float(time.time()),
                socket.gethostname(),
                psutil.net_io_counters().bytes_sent,
                psutil.net_io_counters().bytes_recv
            ]
        ]
      }
    ]
    return json_body


def check_args(args):
    """Process those angry args. """
    cli = InfluxDBClient(
          args.db_host, args.db_port, args.db_user, args.auth_file.readline().rstrip(), args.db_name
          )
    if args.ram:
        ram = ram_usage()
        cli.write_points(ram)
    if args.cpu:
        cpu = cpu_load()
        cli.write_points(cpu)
    if args.inet:
        inet = inet_bytes()
        cli.write_points(inet)

def main():
    """Main function. """
    args = parse_args()
    check_args(args)


if __name__ == '__main__':
    cpu = Proc()
    ram = Ram()
    main()
