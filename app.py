import asyncio
import aiohttp
import os

async def fetch_cloudflare_ips():
    ipv4_url = 'https://www.cloudflare.com/ips-v4'
    ipv6_url = 'https://www.cloudflare.com/ips-v6'

    async with aiohttp.ClientSession() as session:
        ipv4_response = await session.get(ipv4_url)
        ipv6_response = await session.get(ipv6_url)

        ipv4_ips = await ipv4_response.text()
        ipv6_ips = await ipv6_response.text()

    return ipv4_ips.splitlines(), ipv6_ips.splitlines()

def generate_ufw_commands(ports, ipv4_ips, ipv6_ips, allow_type):
    commands = []

    for port in ports:
        for ip in ipv4_ips:
            commands.append(f"sudo ufw {allow_type} from {ip} to any port {port} proto tcp")
            commands.append(f"sudo ufw {allow_type} from {ip} to any port {port} proto udp")

        for ip in ipv6_ips:
            commands.append(f"sudo ufw {allow_type} from {ip} to any port {port} proto tcp")
            commands.append(f"sudo ufw {allow_type} from {ip} to any port {port} proto udp")

    return commands

async def main():
    ipv4_ips, ipv6_ips = await fetch_cloudflare_ips()

    while True:
        os.system('cls' if os.name == 'nt' else 'clear')
        ports_input = input("Enter ports separated by commas (e.g., 80,443, default is \"80,443\"): ").replace(" ", "").lower() or "80,443"
        allow_type = input("Would you like to delete these records or allow these records (e.g., allow/deny/delete allow, default is \"allow\"): ").lower() or "allow"
        ports = [port.strip() for port in ports_input.split(',')]
        print(f"Command example: sudo ufw {allow_type} from {ipv4_ips[0]} to any port {ports[0]} proto tcp")
        _continue = input("Continue: (y/N): ").replace(" ", "").lower()
        if _continue in ["y", "yes"]:
            os.system('cls' if os.name == 'nt' else 'clear')
            break
        else:
            os.system('cls' if os.name == 'nt' else 'clear')
            continue

    commands = generate_ufw_commands(ports, ipv4_ips, ipv6_ips, allow_type)

    print("Generated commands:")
    for command in commands:
        print(command)
    input("Press Enter to continue...: ")

if __name__ == "__main__":
    asyncio.run(main())
