#!/usr/bin/python3
"""Usage:
	autorip.py <first_episode> <season> <series_name> <device_or_iso> <dvd_titles>... 

"""
import sys
#import argparse
import docopt
import logging

def build_handbrake_list(device_or_iso, title, output):
	handbrake_cmd_list = [
		"HandBrakeCLI",
		"-i",
		"'" + device_or_iso + "'",
		"--title",
		title,
		"-a",
		"1,2,3,4,5,6,7,8,9,10",
		"--subtitle",
		"1,2,3,4,5,6,7,8,9,10",
		"--preset=\'High Profile\'",
		"-o",
		"'" + output + "'",
		]

	return handbrake_cmd_list

def get_logger():
	return logging.getLogger(__name__)

def get_output_name(series, season, episode):
	return "{:s} S{:02d}E{:02d}.m4v".format(series, season, episode)

def get_args():
	#parser = argparse.ArgumentParser(description="Use HandBrakeCLI to rip episodes from a DVD")
	#parser.add_argument("first_episode", type=int, help="Number of the first episode e.g. for episdes E04, E06 and E06, episode should be 4")
	#parser.add_argument("dvd_titles", nargs='+', help="List of the DVD titles to be encoded in episode order")
	#parser.add_argument("season", type=int, help="The DVD season")
	#parser.add_argument("series_name", type=str, help="The name of the show")
	#parser.add_argument("device_or_iso", type=str, help="The DVD device or ISO path to rip from.")
	#parser.add_argument("-n", action="store_true", help="Show HandBrakeCLI commands without running them")
	#return parser.parse_args()
	return docopt.docopt(__doc__)

args = get_args()

logging.basicConfig(level=logging.INFO)

episode_count = len(args["<dvd_titles>"])
first_episode = int(args["<first_episode>"])
episode_numbers =  range(first_episode, first_episode + episode_count)
episode_out_names = [get_output_name(args["<series_name>"], int(args["<season>"]), episode) for episode in episode_numbers]

get_logger().info("Ripping %d episodes (%s) from %s: %s", episode_count, ', '.join(args["<dvd_titles>"]), args["<device_or_iso>"], ', '.join(episode_out_names))

for ep_number, ep_title in zip(args["<dvd_titles>"], episode_out_names):
	commands = build_handbrake_list(args["<device_or_iso>"], ep_number, ep_title)

	print(' '.join(commands))
