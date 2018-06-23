#!/usr/bin/env python3
"""Usage:
	autorip.py <first_episode> <season> <series_name> <device_or_iso> <dvd_titles> 

"""
import sys
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
		"--preset=\'Super HQ 1080p30 Surround\'",
		"-o",
		"'" + output + "'",
		]

	return handbrake_cmd_list

def get_logger():
	return logging.getLogger(__name__)

def get_output_name(series, season, episode):
	return "{:s} S{:02d}E{:02d}.m4v".format(series, season, episode)

def split_to_titles(dvd_title_ranges):
	titles = []
	for dvd_title_range in dvd_title_ranges.split(","):
		if "-" in dvd_title_range:
			(start, end) = dvd_title_range.split("-")
			title_range = [str(t) for t in range(int(start), int(end)+1)]
			titles.extend(title_range)
		else:
			titles.extend([dvd_title_range])
	return titles

args = docopt.docopt(__doc__)

logging.basicConfig(level=logging.INFO)

dvd_title_ranges = args["<dvd_titles>"]

dvd_titles = split_to_titles(dvd_title_ranges)
episode_count = len(dvd_titles)

first_episode = int(args["<first_episode>"])
episode_numbers =  range(first_episode, first_episode + episode_count)
episode_out_names = [get_output_name(args["<series_name>"], int(args["<season>"]), episode) for episode in episode_numbers]

get_logger().info("Ripping %d episodes (%s) from %s: %s", episode_count, ', '.join(dvd_titles), args["<device_or_iso>"], ', '.join(episode_out_names))

for ep_number, ep_title in zip(dvd_titles, episode_out_names):
	commands = build_handbrake_list(args["<device_or_iso>"], ep_number, ep_title)

	print(' '.join(commands))
