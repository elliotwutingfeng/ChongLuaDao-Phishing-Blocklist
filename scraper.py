"""Extract phishing URLs found at https://chongluadao.vn
and write them to a .txt blocklist
"""
from __future__ import annotations
import ipaddress
import logging
import re
import socket
from datetime import datetime

import requests
import tldextract

logger = logging.getLogger()
logging.basicConfig(level=logging.INFO, format="%(message)s")


def current_datetime_str() -> str:
    """Current time's datetime string in UTC

    Returns:
        str: Timestamp in strftime format "%d_%b_%Y_%H_%M_%S-UTC".
    """
    return datetime.utcnow().strftime("%d_%b_%Y_%H_%M_%S-UTC")


def clean_url(url: str) -> str:
    """Remove zero width spaces, leading/trailing whitespaces, trailing slashes,
    and URL prefixes from a URL

    Args:
        url (str): URL.

    Returns:
        str: URL without zero width spaces, leading/trailing whitespaces, trailing slashes,
    and URL prefixes.
    """
    removed_zero_width_spaces = re.sub(r"[\u200B-\u200D\uFEFF]", "", url)
    removed_leading_and_trailing_whitespaces = removed_zero_width_spaces.strip()
    removed_trailing_slashes = removed_leading_and_trailing_whitespaces.rstrip("/")
    removed_https = re.sub(r"^[Hh][Tt][Tt][Pp][Ss]:\/\/", "", removed_trailing_slashes)
    removed_http = re.sub(r"^[Hh][Tt][Tt][Pp]:\/\/", "", removed_https)

    return removed_http


def extract_phishing_urls() -> set[str]:
    """Extract phishing URLs from chongluadao.vn phishing URL API

    Returns:
        set[str]: Unique phishing URLs.
    """
    try:
        response = requests.get("https://api.chongluadao.vn/v1/blacklist", timeout=120)
        if response.status_code != 200:
            logger.error("API response status code: %d", response.status_code)
            raise OSError("Unable to retrieve API response")

        body = response.json()
        urls = set(
            clean_url(entry["url"].replace("*.", "").replace("/*", ""))
            for entry in body
            if "url" in entry
        )
        return urls
    except Exception as error:
        logger.error(error)
        return set()


if __name__ == "__main__":
    urls: set[str] = extract_phishing_urls()
    ips: set[str] = set()
    non_ips: set[str] = set()
    fqdns: set[str] = set()
    registered_domains: set[str] = set()

    if not urls:
        raise ValueError("Failed to scrape URLs")
    for url in urls:
        res = tldextract.extract(url)
        registered_domain, domain, fqdn = (
            res.registered_domain,
            res.domain,
            res.fqdn,
        )
        if domain and not fqdn:
            # Possible IPv4 Address
            try:
                socket.inet_pton(socket.AF_INET, domain)
                ips.add(domain)
            except socket.error:
                # Is invalid URL and invalid IP -> skip
                pass
        elif fqdn:
            non_ips.add(url)
            fqdns.add(fqdn)
            registered_domains.add(registered_domain)

    if not non_ips and not ips:
        logger.error("No content available for blocklists.")
    else:
        non_ips_timestamp: str = current_datetime_str()
        non_ips_filename = "urls.txt"
        with open(non_ips_filename, "w") as f:
            f.writelines("\n".join(sorted(non_ips)))
            logger.info(
                "%d non-IPs written to %s at %s",
                len(non_ips),
                non_ips_filename,
                non_ips_timestamp,
            )

        ips_timestamp: str = current_datetime_str()
        ips_filename = "ips.txt"
        with open(ips_filename, "w") as f:
            f.writelines("\n".join(sorted(ips, key=ipaddress.IPv4Address)))
            logger.info(
                "%d IPs written to %s at %s", len(ips), ips_filename, ips_timestamp
            )

        fqdns_timestamp: str = current_datetime_str()
        fqdns_filename = "urls-pihole.txt"
        with open(fqdns_filename, "w") as f:
            f.writelines("\n".join(sorted(fqdns)))
            logger.info(
                "%d FQDNs written to %s at %s",
                len(fqdns),
                fqdns_filename,
                fqdns_timestamp,
            )

        registered_domains_timestamp: str = current_datetime_str()
        registered_domains_filename = "urls-UBL.txt"
        with open(registered_domains_filename, "w") as f:
            f.writelines("\n".join(f"*://*.{r}/*" for r in sorted(registered_domains)))
            logger.info(
                "%d Registered Domains written to %s at %s",
                len(registered_domains),
                registered_domains_filename,
                registered_domains_timestamp,
            )
