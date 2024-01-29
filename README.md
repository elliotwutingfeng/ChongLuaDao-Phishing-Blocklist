# ChongLuaDao Phishing Blocklist

![Python](https://img.shields.io/badge/Python-FFD43B?style=for-the-badge&logo=python&logoColor=blue)
![GitHub Actions](https://img.shields.io/badge/GitHub_Actions-2088FF?style=for-the-badge&logo=github-actions&logoColor=white)

[![GitHub license](https://img.shields.io/badge/LICENSE-BSD--3--CLAUSE-GREEN?style=for-the-badge)](LICENSE)
[![scraper](https://img.shields.io/github/actions/workflow/status/elliotwutingfeng/ChongLuaDao-Phishing-Blocklist/scraper.yml?branch=main&label=SCRAPER&style=for-the-badge)](https://github.com/elliotwutingfeng/ChongLuaDao-Phishing-Blocklist/actions/workflows/scraper.yml)
![Total Blocklist URLs](https://tokei-rs.onrender.com/b1/github/elliotwutingfeng/ChongLuaDao-Phishing-Blocklist?label=Total%20Blocklist%20URLS&style=for-the-badge)

Machine-readable `.txt` blocklist of phishing URLs and IP Addresses from the [Chống Lừa Đảo](https://chongluadao.vn) project, updated once a day.

The URLs and IP Addresses in this blocklist are compiled by the **Chống Lừa Đảo** project.

**Disclaimer:** _This project is not sponsored, endorsed, or otherwise affiliated with the Chống Lừa Đảo project._

## Blocklist download

| File | Download |
|:-:|:-:|
| urls.txt | [:floppy_disk:](urls.txt?raw=true) |
| urls-ABP.txt | [:floppy_disk:](urls-ABP.txt?raw=true) |
| urls-UBO.txt | [:floppy_disk:](urls-UBO.txt?raw=true) |
| urls-UBL.txt | [:floppy_disk:](urls-UBL.txt?raw=true) |
| urls-pihole.txt | [:floppy_disk:](urls-pihole.txt?raw=true) |
| ips.txt | [:floppy_disk:](ips.txt?raw=true) |

## Requirements

- Python 3.12+

## Setup instructions

`git clone` and `cd` into the project directory, then run the following

```bash
python3 -m venv venv
venv/bin/python3 -m pip install --upgrade pip
venv/bin/python3 -m pip install -r requirements.txt
```

## Usage

```bash
venv/bin/python3 scraper.py
```

## Libraries/Frameworks used

- [tldextract](https://github.com/john-kurkowski/tldextract)

&nbsp;

<sup>These files are provided "AS IS", without warranty of any kind, express or implied, including but not limited to the warranties of merchantability, fitness for a particular purpose and noninfringement. In no event shall the authors or copyright holders be liable for any claim, damages or other liability, arising from, out of or in connection with the files or the use of the files.</sup>

<sub>Any and all trademarks are the property of their respective owners.</sub>
