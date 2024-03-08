from scapy.all import sniff, IP, IPv6, TCP, UDP

def packet_handler(packet):
    data = ""
    ip_protocol = False
    if IP in packet:
        data+=packet[IP].src
        data+=","
        data+=packet[IP].dst
        data+=","
        
    elif IPv6 in packet:
        data+=packet[IPv6].src
        data+=","
        data+=packet[IPv6].dst
        data+=","
        ip_protocol =True
    if TCP in packet:
        data+=str(packet[TCP].sport)
        data+=","
        data+=str(packet[TCP].dport)
        data+=","
    elif UDP in packet:
        data+=str(packet[UDP].sport)
        data+=","
        data+=str(packet[UDP].dport)
        data+=","
    if ip_protocol is True:
        data+="IPv6\n"
    else:
        data+="IPv4\n"
    with open("data.csv",mode="a")as file:
        file.write(data)
        



cap = sniff(prn = packet_handler,count=5,filter = "ip or ip6")