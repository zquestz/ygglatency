import os
import re
import sys
import requests
from icmplib import ping
from bs4 import BeautifulSoup

# Public set of Yggdrasil network peers.
PUBLIC_PEERS_URI = "https://publicpeers.neilalexander.dev/"

def get_hostname(peer):
    """Get hostname of peer"""
    match = re.match(r"(tls|tcp|quic):\/\/\[?(.[a-zA-Z0-9:.\-]*)\]?:", peer)
    return match.group(2) if match else None

def fetch_peers(uri):
    """Fetch peers from Yggdrasil public peers listing"""
    peers = {}

    response = requests.get(uri)
    if response.status_code != 200:
        print(f'Failed to retrieve the page: {response.status_code}')
        return peers

    soup = BeautifulSoup(response.text, 'html.parser')

    tags = soup.find_all('td')
    for tag in tags:
        hostname = get_hostname(tag.text)
        if hostname is not None:
          peers[tag.text] = hostname

    return peers

def run() -> {}:
    """Output list of Yggdrasil peers by latency"""
    # Dictionary to store the latency for each peer.
    latencies = {}

    # Get peers from the site.
    peers = fetch_peers(PUBLIC_PEERS_URI)
    
    # Ping each peer and record the latency.
    for peer in peers:
        try:
            response = ping(peers[peer], count=1, privileged=False)
            latencies[peer] = response.avg_rtt
        except Exception as err:
            print(f"{err}")

    return(latencies)

def display(latencies):
    """Print latency information to screen"""
    # Sort the peers by latency
    sorted_peers = sorted(latencies, key=latencies.get)

    # Find the longest peer and latencies for formatting
    max_peer_length = max(len(peer) for peer in sorted_peers)
    max_peer_latencies_length = max(len(str(latencies[peer])) for peer in sorted_peers)

    # Latencies are short, usually the header is longer.
    latencyHeader = 'Latency (ms)'
    max_latencies_length = max(len(latencyHeader), max_peer_latencies_length) + 3

    # Print the header with dynamic spacing.
    header = f"{'Peer'.ljust(max_peer_length)}{latencyHeader.rjust(max_latencies_length)}"
    print(header)
    print("-" * len(header))

    # Print each row, and format from the widths above.
    for peer in sorted_peers:
        if latencies[peer] > 0:
            print(f"{peer.ljust(max_peer_length)}{str(latencies[peer]).rjust(max_latencies_length)}")
