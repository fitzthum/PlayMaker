import m3u8

from urllib import parse
from os import path
from argparse import ArgumentParser
import xml.etree.ElementTree as ET 


def main(args):
  if not args.target: 
    target = args.source

  playlist = m3u8.load(args.playlist)
  target_tree = ET.parse(args.xml)  
  target_root = target_tree.getroot()
  
  new_playlist = ET.SubElement(target_root, "playlist")
  new_playlist.set("name", args.name)
  new_playlist.set("show-browser", "false")
  new_playlist.set("search-type", "search-match")
  new_playlist.set("type", "static")

  for segment in playlist.segments:
    # maybe should use path lib here to avoid sticking in an extra slash or something
    target_uri = segment.uri.replace(args.source, args.target)
    if not path.exists(target_uri):
      print("NOT FOUND: {}".format(target_uri))
      continue
    
    # idk why rhythmbox uses this format... 
    # maybe there is a better way to encode?
    # this might not be complete
    target_uri = parse.quote(target_uri,safe="'/&()!;,.:+?")
    target_uri = "file://{}".format(target_uri)
    location = ET.SubElement(new_playlist, "location")
    location.text = target_uri
   
  # why you no pretty print?
  # i might fix at some point
  target_tree.write(args.xml)


if __name__ == "__main__":
  parser = ArgumentParser(prog="PlayMaker.py", description="Add m3u playlists to Rhythmbox playlist XML")
  parser.add_argument("-n","--name", required=True)
  parser.add_argument("-x","--xml", required=True)
  parser.add_argument("-p","--playlist", required=True)
  parser.add_argument("-s","--source", required=True, help="Path to library in input playlist")
  parser.add_argument("-t","--target", help="Path to library for target playlist XML")

  args = parser.parse_args()
  main(args)
