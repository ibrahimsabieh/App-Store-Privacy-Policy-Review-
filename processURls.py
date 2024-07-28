import json
from urllib.parse import urlparse


def extract_domains_from_har(har_file_path):
    with open(har_file_path, "r") as file:
        har_data = json.load(file)

    domains = set()

    for entry in har_data["log"]["entries"]:
        full_url = entry["request"]["url"]
        parsed_url = urlparse(full_url)
        domain = parsed_url.netloc
        domains.add(domain)

    return domains


def extract_simple_domains_from_har(har_file_path):
    with open(har_file_path, "r") as file:
        har_data = json.load(file)

    domains = set()

    for entry in har_data["log"]["entries"]:
        full_url = entry["request"]["url"]
        parsed_url = urlparse(full_url)
        domain_parts = parsed_url.netloc.split(".")

        # Extract the SLD and TLD (e.g., 'example' from 'sub.example.com')
        simple_domain = ".".join(domain_parts[-2:])
        domains.add(simple_domain)

    return domains


def read_domains_from_json(json_file_path):
    with open(json_file_path, "r") as file:
        return set(json.load(file))


# Path to your HAR file and JSON file
har_file_path = "./ios_log/har/dump.har"
json_file_path = "./data/Third-Party-Trackers.json"

# Extract domain names
har_domains_withSub = extract_simple_domains_from_har(har_file_path)
har_domains_withoutSub = extract_domains_from_har(har_file_path)

json_domains = read_domains_from_json(json_file_path)

# Check for common domain names
common_domains = set()

common_domains_withSub = har_domains_withSub.intersection(json_domains)
common_domains_withoutSub = har_domains_withoutSub.intersection(json_domains)

common_domains.update(common_domains_withSub, (common_domains_withoutSub))


# Print common domain names
print(common_domains)

# print(json_domains)
# print("\n", extract_simple_domains_from_har(har_file_path))
