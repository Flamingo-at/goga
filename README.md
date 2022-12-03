<h1 align="center">GOGA</h1>

<p align="center">Registration of referrals for the GOGA application</p>
<p align="center">
<img src="https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54">
<img src="https://img.shields.io/badge/Tor-7D4698?style=for-the-badge&logo=Tor-Browser&logoColor=white">
</p>

## Installation
+ Install python
+ Download and extract repository
+ Install requirements:
```python
pip install -r requirements.txt
```
Bot supports **tor proxy**, for this you need to install the [Tor Browser](https://www.torproject.org/download/)

## Preparing
**Bot only supports rambler email with activated IMAP**
+ Create ```rambler_emails.txt``` in the project folder
+ Insert emails each on a new line
  + Example: ```email@rambler.ru:password```
+ Run the bot:
```python
python goga.py
```

## Usage
1. ```Refferal code``` - your referral code from the application
2. ```Threads``` - number of simultaneous registrations
3. ```Delay(sec)``` - delay between referral registrations in seconds
4. ```Use tor proxies?(y/n)``` - if you select ```n```, referrals will be registered to your ip. If you select ```y```, each referral will have a different ip, but for this you need to launch the Tor Browser

**Successfully registered referrals are saved in** ```registered.txt```
