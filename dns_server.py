import socket

LOCAL_IPV4 = "192.168.1.176"

print(f"[DNS] Listening on {LOCAL_IPV4}:53 -> Redirecting all DNS to {LOCAL_IPV4}")

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind(("0.0.0.0", 53))

while True:
    data, addr = sock.recvfrom(512)
    print(f"[DNS] Request from Switch {addr}")
    tx_id = data[:2]
    flags = b"\x81\x80"
    qdcount = data[4:6]
    ancount = b"\x00\x01"
    nscount = b"\x00\x00"
    arcount = b"\x00\x00"

    idx = 12
    while data[idx] != 0:
        idx += data[idx] + 1
    question = data[12 : idx + 5]

    answer = b"\xc0\x0c\x00\x01\x00\x01\x00\x00\x00\x3c\x00\x04" + socket.inet_aton(LOCAL_IPV4)
    response = tx_id + flags + qdcount + ancount + nscount + arcount + question + answer
    sock.sendto(response, addr)

