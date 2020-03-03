import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Import packages for testing
from Controller.rssfeeds import feed as rssfeed
from Controller.atomfeeds import feed as atomfeed

