import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Import packages for testing

from controller.rssfeeds import feed as rssfeed
from controller.atomfeeds import feed as atomfeed


