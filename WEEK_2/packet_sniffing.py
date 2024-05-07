from scapy.all import sniff, IP, IPv6, TCP, UDP

def packet_handler(packet):
    data = ""
    cnt=0
    ip_protocol = False
    if IP in packet:
        data+=packet[IP].src
        data+=","
        data+=packet[IP].dst
        data+=","
        cnt+=1
        
    elif IPv6 in packet:
        data+=packet[IPv6].src
        data+=","
        data+=packet[IPv6].dst
        data+=","
        ip_protocol =True
        cnt+=1
    if TCP in packet:
        data+=str(packet[TCP].sport)
        data+=","
        data+=str(packet[TCP].dport)
        data+=","
        cnt+=1
    elif UDP in packet:
        data+=str(packet[UDP].sport)
        data+=","
        data+=str(packet[UDP].dport)
        data+=","
        cnt+=1
    if ip_protocol is True :
        data+="IPv6\n"
    else:
        data+="IPv4\n"
    if cnt==2:
        with open("data.csv",mode="a")as file:
            file.write(data)
        



cap = sniff(prn = packet_handler,count=5,filter = "ip or ip6")