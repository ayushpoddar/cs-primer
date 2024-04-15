# Problem statement
A TCP SYN flood is a denial-of-service attack where TCP handshakes are initiated but not completed. In this problem, you will analyze a simulation of a TCP SYN flood by parsing a packet capture file.

Ultimately, your objective will be to determine which percentage of incoming SYN messages captured in the file were ACKed. Please watch the first section of the video for more context on what this involves, and if these concepts are new you may wish to also continue watching through "Planning and hints".

# Strategy

- Parse the pcap savefile header, to confirm that we are opening and parsing the file correctly, but mostly just to get to the end of the header. For this you can use man pcap-savefile if that exists on your system, or google for the same
- Parse each of the per-packet pcap headers, to determine the limits of each (they are variable length, so expect to see alternating packets and payload).
- Parse the very brief "link layer header", in this case a small placeholder to indicate that packets were captured over the loopback interface
- Parse the IP headers, using something like the IPv4 Wikipedia article to determine the header layout. Details are not necessary, although you could use IP addresses to know which messages are "inbound"
- Next will come the TCP headers. From here you will want to parse flag bits to determine which contain SYN and/or ACK flags. You may also wish to use the ports to determine inbound vs outbound messages, if you didn't already derive this from the IP headers. Again the Wikipedia article (this time on TCP obviously) should be sufficient for the header structure.


# Links and resources
- [Wiki on SYN flood](https://en.wikipedia.org/wiki/SYN_flood)
- [IPv4 Packet structure](https://en.wikipedia.org/wiki/Internet_Protocol_version_4#Packet_structure)
- [TCP Segment structure](https://en.wikipedia.org/wiki/Transmission_Control_Protocol#TCP_segment_structure)
- Learn more about pcap file structure by running `man pcap-savefile`

# Learnings
In a pcap file, after the pcap headers, there are data packets. Each packet has the following structure:
1. Link Layer Header
2. IP Header
3. TCP Header
4. TCP payload

The IP Header and TCP Header and TCP Payload all follow the network byte order, i.e., Big Endian.
