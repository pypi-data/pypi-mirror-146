"""Parse .ninja_log file and print statistics."""
import argparse
import os
from glob import glob
from os.path import isfile, isdir
import logging
from operator import itemgetter
import datetime


def parse_ninja_log(logfile: str) -> list:
    """Parse .ninja_log file and return the statistics as a list
    of tuples (time, object_path).
    Parameters
    ----------
    logfile (str): Path to .ninja_log file.
    Returns
    ----------
    stats (list): List of tuples containing build times and objects.
    """
    with open(logfile, 'r') as f:
        lines = f.readlines()
    header = lines[0]
    if header.startswith('# ninja log'):
        ninja_version = header.split()[-1]
    else:
        logging.error(
            '{0} is not a valid ninja_log file!'.format(logfile))
        exit()
    stats = [(' ', 0)]*(len(lines)-1)
    for i, line in enumerate(lines[1:]):
        logging.debug('Line {0}: {1}'.format(i, line))
        tokens = line.split()
        assert len(tokens) == 5
        begin = int(tokens[0])
        end = int(tokens[1])
        obj = tokens[3]
        stats[i] = (end-begin, obj)
    return stats


def main():
    parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter,
                                     description="""Parse .ninja_log files.""")
    logging.basicConfig(
        format='%(levelname)s: %(message)s', level=logging.INFO)
    parser.add_argument('path', nargs='*',
                        help='''Path to .ninja_log file or the directory that
                             contains it. Default is the current directory.''')
    parser.add_argument('-t', '--top', type=int,
                        default=10,
                        help='''Print only top `n` items. Prints top 10 by default. 
                        Use -t -1 to print all.''')
    parser.add_argument('-f', '--filter', type=str,
                        default='',
                        help='''Print aggregated stats for objects that includes
                             the filter. Default is an empty string, no filtering.''')

    args = parser.parse_args()
    pathlist = args.path
    filterstr = args.filter
    if len(pathlist) == 0:
        logfile = '.ninja_log'
    elif len(pathlist) == 1:
        if isdir(pathlist[0]):
            logfile = pathlist[0] + os.path.sep + '.ninja_log'
        else:
            logfile = pathlist[0]
    elif len(pathlist) == 2:
        logging.error(
            'Comparison of .ninja_log files have not been implemented, yet. Stay tuned.')
        exit()
    else:
        logging.error('More than two positional arguments is not supported.')
        exit()
    if isfile(logfile):
        logging.info('Parsing {0} file'.format(logfile))
    else:
        logging.error('{} file not found!'.format(logfile))
        exit()
    factor = 0.001  # convert to seconds
    stats = parse_ninja_log(logfile)
    totaltime = sum([pair[0] for pair in stats]) * factor
    nobj = len(stats)
    print("Found {} items in the build.".format(nobj))
    print("Ninja build time: {:.3f} seconds ({}). \n".format(
        totaltime, str(datetime.timedelta(seconds=int(totaltime)))))

    if filterstr:
        stats = list(filter(lambda x: (filterstr in x[1]), stats))
        ftime = sum([pair[0] for pair in stats]) * factor
        percentage = ftime / totaltime * 100.
        print("{} items matched the given filter ('{}')".format(
            len(stats), filterstr))
        print("Ninja build time: {0:.3f} seconds ({1}). {2:6.2f} % of total time. \n".format(
            ftime, str(datetime.timedelta(seconds=int(ftime))), percentage))

    sortedstats = sorted(stats, key=itemgetter(0), reverse=True)

    logging.info('''\n Note that total compute time reported here can be significantly more than the total wall time for the build since Ninja might be using many threads.\n''')
    print('{0:10} {1:^18} {2:^30}'.format('Percentage', 'Time (s)', 'Object'))
    print('{0:10} {1:^18} {2:}'.format('-'*10, '-'*16, '-'*30))
    for stat in sortedstats[:args.top]:
        time = stat[0] * factor
        obj = stat[1]
        percentage = time/totaltime * 100.
        print('{0:8.2f} {1:18.3f}   {2}'.format(percentage, time, obj))


if __name__ == "__main__":
    main()
