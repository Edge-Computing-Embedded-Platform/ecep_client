"""
Edge Computing Embedded Platform
Developed by Abhishek Gurudutt, Chinmayi Divakara
Praveen Prabhakaran, Tejeshwar Chandra Kamaal
"""

import wamp_client
import callContainer_api
import deviceRegister
import fetcher
client = None
def init(path):
    fetcher.init_fetcher(path)
