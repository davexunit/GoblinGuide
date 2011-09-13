import ConfigParser
import os

# Open config file
config = ConfigParser.RawConfigParser()
config.read(os.path.join(os.environ['HOME'], ".goblinguide"))

