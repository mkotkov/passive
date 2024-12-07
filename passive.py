import argparse
import requests # type: ignore
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
    try:
        response = requests.get(f"http://ip-api.com/json/{ip}")
        if response.status_code == 200:
            data = response.json()
            result = (
                f"IP: {ip}\n"
                f"ISP: {data.get('isp', 'Not found')}\n"
                f"City: {data.get('city', 'Not found')}\n"
                f"Region: {data.get('regionName', 'Not found')}\n"
                f"Country: {data.get('country', 'Not found')}\n"
                f"Coordinates: ({data.get('lat', 'N/A')}), ({data.get('lon', 'N/A')})"
            )
            return result
        else:
            return f"Error: Could not fetch IP data. Status code: {response.status_code}."
    except Exception as e:
        return f"An error occurred: {e}"

def username_lookup(username):
    try:
        # URL для загрузки базы WhatsMyName
        url = "https://raw.githubusercontent.com/WebBreacher/WhatsMyName/main/wmn-data.json"
        response = requests.get(url)
        
        if response.status_code != 200:
            return f"Error: Failed to download WhatsMyName database. Status code: {response.status_code}"

        # Загружаем JSON-данные
        data = response.json()

        # Сайты, по которым выполняется проверка
        target_sites = {"facebook", "twitter", "telegram", "instagram", "github"}

        # База данных сайтов
        sites = data.get("sites", [])
        filtered_sites = [site for site in sites if site.get("name", "").lower() in target_sites]

        # Проверим, что фильтрация прошла успешно
        if not filtered_sites:
            return "Error: None of the target sites found in the database."

        print(f"Filtered sites: {[site['name'] for site in filtered_sites]}")  # Отладка

        results = {}
        for site in filtered_sites:
            site_name = site.get("name", "Unknown")
            uri_check = site.get("uri_check", "").replace("{account}", username)
            if uri_check:
                try:
                    # Проверяем наличие страницы через HEAD-запрос
                    response = requests.head(uri_check, timeout=15)
                    if response.status_code == site.get("e_code", 200):
                        results[site_name] = "yes"
                    else:
                        results[site_name] = "no"
                except requests.RequestException:
                    results[site_name] = "no"

        # Форматируем результаты
        formatted_result = "\n".join([f"{site}: {status}" for site, status in results.items()])
        return f"Search results for username '{username}':\n{formatted_result}"

    except Exception as e:
        return f"An error occurred: {e}"

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