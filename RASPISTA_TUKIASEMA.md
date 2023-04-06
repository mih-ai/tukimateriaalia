# Ohjeet sille, miten Rasperry PI:stä saa näppärästi tehtyä WLAN-tukiaseman eli "hotspotin" ILMAN router-ominaisuutta

Huomionarvoista on se, että "raspin" kaikenlaiset yksityiskohdat ovat aikojen saatossa päivittyneet monta kertaa, ja netistä löytyvät useat vanhat ohjeet eivät välttämättä enää toimi, aiheuttaen niitä lukevalle softankehittäjälle mahdollisesti harmaita hiuksia. Tässä on ohjeet, joilla tukiasemamääritykset voi onnistuneesti tehdä vuoden 2023 alkukupuolella. On lukuisia sovellustilanteita, joissa tukiasema on hyvä määrittää ilman router-ominaisuutta - siitä tämän ohjeen erityispiirteet. 

# Alustukset

Oletetaan että käytettävä raspi on kaikin puolin kunnossa ja siinä on ajantasainen käyttöjärjestelmä. Sen vuoksi emme välttämättä tarvitse komentoja: 

```sh
sudo apt-get update;sudo apt-get upgrade
```

Mutta, tärkeää on asentaa hotspottia varten "hostapd" (lyhenne sanoista hot ja niin edelleen) ja sen tarvitsema tukitoiminto "dnsmasq" (samoin lyhenne...):

```sh
sudo apt-get install hostapd
sudo apt-get install dnsmasq
```

# IP-osoitesäädöt

Tehdään varsinaiset säädöt tukiasemalle siten että ensin määritetään haluttu kiinteä IP mitä halutaan käyttää:

```sh
sudo nano /etc/dhcpcd.conf
```

Tähän tulee lisätä seuraavat rivit tiedoston loppuun (esimerkkinä jos haluttu IP-osoite olisi allaoleva): 

```sh
interface wlan0
static ip_address=192.168.2.150/24
nohook wpa_supplicant
```

Komento nohook voi myös olla yllättävän tärkeä, lue tarvittaessa siitä ja sen merkityksestä lisää muista lähteistä.
Tietoja ylläolevasta komennosta: kuvatuilla käskyillä halutaan mainittu IP-osoite käyttöön. IP-osoitteeen perässä 
oleva /24 kertoo montako ykköstä on "subnet maskissa". Esimerkiksi yllä käytetty 24 tarkoittaa että käytössä 
on 255.255.255.0 koska se on binäärimuodossa 11111111.11111111.11111111.00000000.

# dnsmasq-säädöt

Tässä hotspotissa käytetään DHCP-serverinä dnsmasq:ia. Tee vielä siihen tarvittavat säädöt komennolla:

```sh
sudo nano /etc/dnsmasq.conf
```

tyhjentämällä ensin koko tiedosto jossa on monenlaista turhaa tavaraa ennestään, ja kirjoittamalla tähän tiedostoon pelkästään näin:

```sh
interface=wlan0
dhcp-range=192.168.2.11,192.168.2.140,255.255.255.0,24h
```

Huomaa että tässä mainittu 24h ei liity subnetmaskiin, vaan siinä on kyse nk. "dhcp-lease time" ajasta, johon tuo 24h eli "jatkuvasti"
on ihan hyvä lähtökohta. Ja tietysti, korvaa esimerkin IP-osoite sillä osoitteella mitä itse haluat käyttää. 

# Hotspotin eli "hostapd":n säädöt

Luo uusi tiedosto komennolla:

```sh
sudo nano /etc/hostapd/hostapd.conf
```
Kirjoita tähän seuraavat tiedot:

```sh

interface=wlan0
#Huomaa ei bridge-moodia!
#bridge=br0
hw_mode=g
channel=7
wmm_enabled=0
macaddr_acl=0
auth_algs=1
ignore_broadcast_ssid=0
wpa=2
wpa_key_mgmt=WPA-PSK
wpa_pairwise=TKIP
rsn_pairwise=CCMP
ssid=NETWORK
wpa_passphrase=PASSWORD

#näistä kaikki eivät välttämättä ole tarpeellisia...
driver=nl80211
country_code=FI
ieee80211n=1
ieee80211d=1
```
Huomaa yllä olevassa lopussa oleva maakoodi, joka on "uutena juttuna" voi olla tärkeä, älä aliarvioi sitä kun kiireissäsi teet asetuksia "raspillesi".

Seuraavaksi, jotta edellä huolella laadityt määritykset ovat "hostapd":n löydettävissä muokkaa komennolla:

```sh
sudo nano /etc/default/hostapd
```

avautuvan tiedoston kohta "#DAEMON_CONF="" seuraavankaltaiseksi:

```sh
DAEMON_CONF="/etc/hostapd/hostapd.conf"
```
...ja kaikilla näillä vaiheilla nyt itse "hostapd" on nyt säädetty kohdalleen.

# Määritä muut tarvittavat

Lisää komennolla

```sh
sudo nano /etc/rc.local
```

seuraavat rivit juuri ennen viimeistä "exit 0" -riviä:

```sh
sudo hostapd /etc/hostapd/hostapd.conf &
```

Erityisesti, huomaa ylläoleva hostapd-käynnistysrivi ja sen tärkeys! Sen puuttuminen (useissa muissa ohjeissa) on aihettanut monelle paljon päänvaivaa. Tiedosto rc.local huolehtii siitä, että aina kun järjestelmä käynnistyy, kyseinen toiminto tapahtuu ja suoritetaan eli tässä tapauksessa hotspotti laitetaan päälle. Muista & -merkki loppuun!

# Entä jos se ei sittenkään toimi noilla ohjeilla?

Katso ensin tietokoneesi kalenteria; jos se näyttää esimerkiksi vuotta 2032, on kovastikin mahdollista, että tämä ohje on käynyt vanhaksi, jossa tapauksessa kannattaa luoda uusi ohje ja jakaa se sen jälkeen muillekin käytettäväksi. 
