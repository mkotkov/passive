import argparse
import requests
import os

def save_result(data, filename="result.txt"):
    count = 1
    while os.path.exists(filename):
        filename = f"result{count}.txt"
        count += 1
    with open(filename, "w") as file:
        file.write(data)
    print(f"Saved in {filename}")

def full_name_lookup(first_name, last_name):
    # Dummy data for demonstration
    result = f"First name: {first_name}\nLast name: {last_name}\nAddress: 7 rue du Progrès\n75016 Paris\nNumber: +33601010101"
    return result

def ip_lookup(ip):
    response = requests.get(f"http://ip-api.com/json/{ip}")
    if response.status_code == 200:
        data = response.json()
        result = f"ISP: {data['isp']}\nCity Lat/Lon: ({data['lat']}) / ({data['lon']})"
        return result
    return "Error retrieving IP information"

def username_lookup(username):
    platforms = {"Facebook": "yes", "Twitter": "yes", "Linkedin": "yes", "Instagram": "no", "Skype": "yes"}
    result = "\n".join([f"{platform} : {status}" for platform, status in platforms.items()])
    return result

def main():
    parser = argparse.ArgumentParser(description="Passive Recon Tool")
    parser.add_argument("-fn", nargs=2, metavar=("FirstName", "LastName"), help="Search with full name")
    parser.add_argument("-ip", metavar="IP", help="Search with IP address")
    parser.add_argument("-u", metavar="Username", help="Search with username")
    args = parser.parse_args()

    if args.fn:
        result = full_name_lookup(args.fn[0], args.fn[1])
        save_result(result)
    elif args.ip:
        result = ip_lookup(args.ip)
        save_result(result)
    elif args.u:
        result = username_lookup(args.u)
        save_result(result)
    else:
        print("No valid option provided. Use --help for usage.")
        
if __name__ == "__main__":
    main()