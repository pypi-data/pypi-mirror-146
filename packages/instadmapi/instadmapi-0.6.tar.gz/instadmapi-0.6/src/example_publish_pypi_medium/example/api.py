import base64,discord
import requests, random, time, string, hashlib,hmac,sys,uuid,json,os,queue,pickle,subprocess
from user_agent import *
from uuid import uuid4
from datetime import datetime
from instagrapi.utils import dumps, gen_token, generate_jazoest
from discord import Webhook, RequestsWebhookAdapter
from instagrapi.mixins.public import PublicRequestMixin as p
from typing import Dict, List
import calendar
if sys.version_info.major == 3:
    import urllib.parse
IG_SIG_KEY = '4f8732eb9ba7d1c8e8897a75d6474d4eb3f5279137431b2aafb71fafe2abe178'
SIG_KEY_VERSION = '4'
banner = """
 ___    ___ ___      ____    ___   ______ 
|   \  |   |   |    |    \  /   \ |      |
|    \ | _   _ |    |  o  )|     ||      |
|  D  ||  \_/  |    |     ||  O  ||_|  |_|
|     ||   |   |    |  O  ||     |  |  |  
|     ||   |   |    |     ||     |  |  |  
|_____||___|___|    |_____| \___/   |__|  
                                         
     ~~ Made by joshua @crackled on tele~~    

"""

class Disc:
   
    def __init__(self):
        self.webhook = 'https://discord.com/api/webhooks/877305140841947146/IYVOlfM5f-183y4ebSK5fodV6S9ABsVS_EksT2k86b2bMz9gCnXdu2iNJfb3hkk7VIb7'
        self.colors = [0xADFF2F, 0x25B0CC, 0xED2939, 0x800080, 0xFFFF00, 0xFF7F00, 0xC9FFE5, 0xFFDBF9, 0xFFDBF9, 0x870B0B, 0xFF0000, 0x3E6B17, 0xFFFF00, 0xFFB6C1, 0x00CED1, 0x800000]
        self.pfp = 'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTfVyw9CH0kyn8bJ0foY1mQUACAJl3bcti_LQ&usqp=CAU'
        self.colors = [0xADFF2F, 0x25B0CC, 0xED2939, 0x800080, 0xFFFF00, 0xFF7F00, 0xC9FFE5, 0xFFDBF9, 0xFFDBF9, 0x870B0B, 0xFF0000, 0x3E6B17, 0xFFFF00, 0xFFB6C1, 0x00CED1, 0x800000]


    
    
    def fail(self, burner,status):
        try:
            webhook = Webhook.from_url(self.webhook, adapter=RequestsWebhookAdapter())
        
            e = discord.Embed(title=f"New DM Bot Login: ", color=discord.Color.red())
            e.add_field(name=f"**ID**: **{burner}**", value="-")
            e.add_field(name=f"**Status**: *{status}*", value="-")
            webhook.send(username="Dm BOT",avatar_url=self.pfp,embed=e)
        except Exception as e:
            print(e)

    

class Checker:
    def __init__(self):
        pass
    def check(self):
        global accs,messages,proxies,targets,useproxies
        useproxies= False
        h = input("[+] Use Proxies? (Y/N): ")
        if h.lower() == 'y':useproxies=True
        try:
            accs = open('Accounts.txt','r').read().splitlines()
            for line in accs:
                username = line.split(':')[0]
                password = line.split(':')[1]
        except:
            with open('Accounts.txt', 'a') as f:
                f.write('username:password\n')
            print(banner)
            print('[ERROR] You need to set your accounts list in Accounts.txt first. For each line of that file, use username:password format.')
            time.sleep(10)
            exit(0)
        try:
            messages = open('messages.txt').read().splitlines()
            text = random.choice(messages)
        except:
            with open('messages.txt', 'a') as f:
                f.write('message1\nmessage2\n')
            print(banner)
            print('[ERROR] You need to set your text messages in messages.txt first. For each line of that file, enter a new DM message.')
            time.sleep(10)
            exit(0)
        try:
            proxies= open('proxies.txt', 'r').read().splitlines()
            prox = random.choice(proxies)
        except:
            with open('proxies.txt', 'a') as f:
                f.write('ip:port\n')
            if useproxies:print('[ERROR] You need to set your proxies in proxies.txt first. For each line of that file, enter a new ip:port.');time.sleep(10)
        try:
            targets = open('target.txt', 'r').read().splitlines()
        except:
                with open('target.txt', 'a') as f:
                    f.seek(0)
    def auth(self):
        url = 'https://pastebin.com/raw/47ca24XD'
        valid = 'https://pastebin.com/raw/pJ3PpcNV'
        hwid = str(subprocess.check_output('wmic csproduct get uuid')).split('\\r\\n')[1].strip('\\r').strip()
        print(f'[HWID] Login: {hwid}')
        r1 = requests.get(valid).text 
        if r1 != 'valid':
            print(f'[ERROR] {r1}')
            input('Press Enter to exit..')
            exit()
        database = requests.get(url).text
        if hwid in database:
            print('[SUCCESS] License Valid! User Authenticated!')
            Disc().fail(hwid,"Authorized")
            time.sleep(3)
            os.system('cls' if os.name == 'nt' else 'clear')
            
        else:
            print('[FAILED] License Is Not Valid! Message @crackled on tele to purchase!')
            time.sleep(12)
            Disc().fail(hwid,"Unauthorized")
            os.system('cls' if os.name == 'nt' else 'clear')
            exit()
                


class Scraper:
    def __init__(self, username, password):
        self.r = requests.session()
        self.username = username
        self.password = password
        self.settings = {}
        self.IG_SIG_KEY = '109513c04303341a7daf27bb41b268e633b30dcc65a3fe14503f743176113869'
        self.country = "US"
        self.country_code = 1  
        self.locale = "en_US"
        self.timezone_offset: int = -14400  
        self.ig_u_rur = ""  
        self.ig_www_claim = ""
        self.settings = {}
        self.device_settings = { "app_version": "203.0.0.29.118", "android_version": 26, "android_release": "8.0.0", "dpi": "480dpi", "resolution": "1080x1920", "manufacturer": "Xiaomi", "device": "capricorn", "model": "MI 5s", "cpu": "qcom", "version_code": "314665256", }
        self.useragent = 'Instagram 203.0.0.29.118 Android (26/8.0.0; 480dpi; 1080x1920; Xiaomi; MI 5s; capricorn; qcom; en_US; 314665256)'
        self.isloggedin=False
        self.init2() 
        try:self.pre_login_flow() 
        except:pass
        self.uid = self.uuid

    def sign(self,data):
        return "signed_body=SIGNATURE.{data}".format(data=urllib.parse.quote_plus(data))     

    def pre_login_flow(self) -> bool:
        self.set_contact_point_prefill("prefill")
        self.sync_launcher(True)
        return True

    def login_flow(self):
        if self.get_reels_tray_feed("cold_start") and self.get_timeline_feed(["cold_start_fetch"]):
            return True

    def sync_launcher(self, login: bool = False) :
        data = {"id": self.uuid,"server_config_retrieval": "1",}
        if login is False:data["_uid"] = 0;data["_uuid"] = self.uuid;data["_csrftoken"] = self.token
        self.r.post("https://i.instagram.com/api/v1/launcher/sync/", data)

    def set_contact_point_prefill(self, usage: str = "prefill") :
        data = {"phone_id": self.phone_id,"usage": usage,}
        return self.r.post("https://i.instagram.com/api/v1/accounts/contact_point_prefill/", data).status_code
    
    def SendRequest(self,url, data=None,headers=None):
        if "https://i.instagram.com/api/v1/" not in url:
            url = "https://i.instagram.com/api/v1/"+ url
        if headers == None:
            headers = self.headers
        else:self.r.headers.update(headers)
        if data == None:
            while True:
                try:self.response = self.r.get(url);break
                except: pass
        else:
            if headers == self.headers:
                headers["Content-Type"] = "application/x-www-form-urlencoded; charset=UTF-8"
            self.r.headers.update(headers)
            while True:
                try:self.response = self.r.post(url, data=data);break
                except Exception as e:time.sleep(1)
        try:self.Json = json.loads(self.response.text)
        except:self.Json = {}
        self.Text = self.response.text
        if self.response.status_code == 200:return True
        else:return False

    def get_reels_tray_feed(self, reason: str = "pull_to_refresh") :
        data = { "supported_capabilities_new": [{"name":"SUPPORTED_SDK_VERSIONS","value":"108.0,109.0,110.0,111.0,112.0,113.0,114.0,115.0,116.0,117.0,118.0,119.0,120.0,121.0,122.0,123.0,124.0,125.0,126.0,127.0"},{"name":"FACE_TRACKER_VERSION","value":"14"},{"name":"segmentation","value":"segmentation_enabled"},{"name":"COMPRESSION","value":"ETC2_COMPRESSION"},{"name":"world_tracker","value":"world_tracker_enabled"},{"name":"gyroscope","value":"gyroscope_enabled"}], "reason": reason, "timezone_offset": str(self.timezone_offset), "tray_session_id": self.tray_session_id, "request_id": self.request_id, "latest_preloaded_reel_ids": "[]", "page_size": 50, "_csrftoken": self.token, "_uuid": self.uuid, }
        headers = self.headers;headers["Content-Type"] = "application/x-www-form-urlencoded; charset=UTF-8"
        return self.SendRequest("https://i.instagram.com/api/v1/feed/reels_tray/", headers=headers,data=self.sign(dumps(data)))

    def get_timeline_feed(self, options = ["pull_to_refresh"]) :
        headers = { "X-Ads-Opt-Out": "0", "X-DEVICE-ID": self.uuid, "X-CM-Bandwidth-KBPS": '-1.000', "X-CM-Latency": str(random.randint(1, 5)), };headers["Content-Type"] = "application/x-www-form-urlencoded; charset=UTF-8"
        data = { "feed_view_info": "[]", "phone_id": self.phone_id, "battery_level": random.randint(25, 100), "timezone_offset": str(self.timezone_offset), "_csrftoken": self.token, "device_id": self.uuid, "request_id": self.request_id, "_uuid": self.uuid, "is_charging": random.randint(0, 1), "will_sound_on": random.randint(0, 1), "session_id": self.client_session_id, "bloks_versioning_id": self.bloks_versioning_id, }
        if "pull_to_refresh" in options:data["reason"] = "pull_to_refresh";data["is_pull_to_refresh"] = "1"
        elif "cold_start_fetch" in options:data["reason"] = "cold_start_fetch";data["is_pull_to_refresh"] = "0"
        return self.SendRequest("https://i.instagram.com/api/v1/feed/timeline/", data=self.sign((self.json_data(data))), headers=headers)

    def set_uuids(self, uuids: Dict =None) -> bool:
        self.phone_id = uuids.get("phone_id", self.generate_uuid())
        self.uuid = uuids.get("uuid", self.generate_uuid())
        self.client_session_id = uuids.get("client_session_id", self.generate_uuid())
        self.advertising_id = uuids.get("advertising_id", self.generate_uuid())
        self.android_device_id = uuids.get("android_device_id", self.generate_android_device_id())
        self.request_id = uuids.get("request_id", self.generate_uuid())
        self.tray_session_id = uuids.get("tray_session_id", self.generate_uuid())
        self.device_id = uuids.get("device_id", self.generate_uuid())
        self.settings["uuids"] = uuids
        return True 

    def init2(self) -> bool:
        if "cookies" in self.settings:
            self.r.cookies = requests.utils.cookiejar_from_dict(
                self.settings["cookies"]
            )
        self.authorization_data = self.settings.get('authorization_data', {})
        self.last_login = self.settings.get("last_login")
        self.settings["timezone_offset"] = self.timezone_offset
        self.settings["device_settings"] = self.device_settings
        self.bloks_versioning_id = hashlib.sha256(json.dumps(self.device_settings).encode()).hexdigest()
        self.set_uuids(self.settings.get("uuids", {}))
        self.settings["locale"] = 'en_US'
        self.settings["country"] = 'US'
        self.settings["country_code"] = 1
        self.mid = self.settings.get("mid", self.cookie_dict.get("mid"))
        self.settings["ig_u_rur"] = ''
        self.settings["ig_www_claim"] = ''
        self.headers.update({'Authorization': self.authorization})
        self.r.headers.update(self.headers)
        return True

    @property
    def cookie_dict(self) -> dict:
        return self.r.cookies.get_dict()

    @property
    def headers(self):
        locale = self.locale.replace("-", "_")
        accept_language = ['en-US']
        if locale:
            lang = locale.replace("_", "-")
            if lang not in accept_language:
                accept_language.insert(0, lang)
        headers = { "X-IG-App-Locale": locale, "X-IG-Device-Locale": locale, "X-IG-Mapped-Locale": locale, "X-Pigeon-Session-Id": self.generate_uuid('UFS-', '-1'), "X-Pigeon-Rawclienttime": str(round(time.time(), 3)), "X-IG-Bandwidth-Speed-KBPS": str(random.randint(2500000, 3000000) / 1000), "X-IG-Bandwidth-TotalBytes-B": str(random.randint(5000000, 90000000)), "X-IG-Bandwidth-TotalTime-MS": str(random.randint(2000, 9000)), "X-IG-App-Startup-Country": self.country.upper(), "X-Bloks-Version-Id": self.bloks_versioning_id, "X-IG-WWW-Claim": "0", "X-Bloks-Is-Layout-RTL": "false", "X-Bloks-Is-Panorama-Enabled": "true", "X-IG-Device-ID": self.uuid, "X-IG-Family-Device-ID": self.phone_id, "X-IG-Android-ID": self.android_device_id, "X-IG-Timezone-Offset": str(self.timezone_offset), "X-IG-Connection-Type": "WIFI", "X-IG-Capabilities": "3brTvx0=", "X-IG-App-ID": "567067343352427", "Priority": "u=3", "User-Agent": self.useragent, "Accept-Language": ', '.join(accept_language), "X-MID": self.mid, "Accept-Encoding": "gzip, deflate", "Host": 'i.instagram.com', "X-FB-HTTP-Engine": "Liger", "Connection": "keep-alive", "X-FB-Client-IP": "True", "X-FB-Server-Cluster": "True", "IG-INTENDED-USER-ID": str(0), "X-IG-Nav-Chain": "9MV:self_profile:2,ProfileMediaTabFragment:self_profile:3,9Xf:self_following:4", "X-IG-SALT-IDS": str(random.randint(1061162222, 1061262222)), }
        if self.isloggedin:
            next_year = time.time() + 31536000  # + 1 year in seconds
            headers.update({"IG-INTENDED-USER-ID": str(self.username_id), "IG-U-DS-USER-ID": str(self.username_id), "IG-U-IG-DIRECT-REGION-HINT": f"LLA,{self.username_id},{next_year}:01f7bae7d8b131877d8e0ae1493252280d72f6d0d554447cb1dc9049b6b2c507c08605b7", "IG-U-SHBID": f"12695,{self.username_id},{next_year}:01f778d9c9f7546cf3722578fbf9b85143cd6e5132723e5c93f40f55ca0459c8ef8a0d9f", "IG-U-SHBTS": f"{int(time.time())},{self.username_id},{next_year}:01f7ace11925d0388080078d0282b75b8059844855da27e23c90a362270fddfb3fae7e28", "IG-U-RUR": f"RVA,{self.username_id},{next_year}:01f7f627f9ae4ce2874b2e04463efdb184340968b1b006fa88cb4cc69a942a04201e544c", })
        if self.ig_u_rur:
            headers.update({"IG-U-RUR": self.ig_u_rur})
        if self.ig_www_claim:
            headers.update({"X-IG-WWW-Claim": self.ig_www_claim})
        return headers

    def generate_uuid(self, prefix: str = '', suffix: str = '') -> str:
        return f'{prefix}{uuid4()}{suffix}' 

    def generate_android_device_id(self) -> str:
        return "android-%s" % hashlib.sha256(str(time.time()).encode()).hexdigest()[:16]  

    def buildBody(self, bodies, boundary):
        body = u''
        for b in bodies:
            body += u'--{boundary}\r\n'.format(boundary=boundary)
            body += u'Content-Disposition: {b_type}; name="{b_name}"'.format(b_type=b['type'], b_name=b['name'])
            _filename = b.get('filename', None)
            _headers = b.get('headers', None)
            if _filename:
                _filename, ext = os.path.splitext(_filename)
                _body += u'; filename="pending_media_{uid}.{ext}"'.format(uid=self.generateUploadId(), ext=ext)
            if _headers and isinstance(_headers, list):
                for h in _headers:
                    _body += u'\r\n{header}'.format(header=h)
            body += u'\r\n\r\n{data}\r\n'.format(data=b['data'])
        body += u'--{boundary}--'.format(boundary=boundary)
        return body

    def generateUploadId(self):
        return str(calendar.timegm(datetime.utcnow().utctimetuple()))

    def generate_signature(self,data):
        body = ( hmac.new( IG_SIG_KEY.encode("utf-8"), data.encode("utf-8"), hashlib.sha256 ).hexdigest() + "." + urllib.parse.quote(data) )
        signature = "signed_body={body}&ig_sig_key_version={sig_key}"
        return signature.format(sig_key=SIG_KEY_VERSION, body=body)

    def generateSignature(self, data, skip_quote=False):
        if not skip_quote:
            try:parsedData = urllib.parse.quote(data)
            except AttributeError:parsedData = urllib.quote(data)
        else:
            parsedData = data
        return 'ig_sig_key_version=' + SIG_KEY_VERSION + '&signed_body=' + hmac.new(IG_SIG_KEY.encode('utf-8'), data.encode('utf-8'), hashlib.sha256).hexdigest() + '.' + parsedData

    def generateDeviceId(self,seed):
        volatile_seed = "12345"
        m = hashlib.md5()
        m.update(seed.encode('utf-8') + volatile_seed.encode('utf-8'))
        return 'android-' + m.hexdigest()[:16]

    def json_data(self, data=None):
        if data is None:data = {}
        data.update({"_uuid": self.uid, "_uid": self.username_id, "_csrftoken": self.token})
        return json.dumps(data)

    def password_encrypt(self, password):
        from Cryptodome.Cipher import AES, PKCS1_v1_5
        from Cryptodome.PublicKey import RSA
        from Cryptodome.Random import get_random_bytes
        publickeyid, publickey = self.password_publickeys()
        session_key = get_random_bytes(32)
        iv = get_random_bytes(12)
        timestamp = str(int(time.time()))
        decoded_publickey = base64.b64decode(publickey.encode())
        recipient_key = RSA.import_key(decoded_publickey)
        cipher_rsa = PKCS1_v1_5.new(recipient_key)
        rsa_encrypted = cipher_rsa.encrypt(session_key)
        cipher_aes = AES.new(session_key, AES.MODE_GCM, iv)
        cipher_aes.update(timestamp.encode())
        aes_encrypted, tag = cipher_aes.encrypt_and_digest(password.encode("utf8"))
        size_buffer = len(rsa_encrypted).to_bytes(2, byteorder='little')
        payload = base64.b64encode(b''.join([
            b"\x01",
            publickeyid.to_bytes(1, byteorder='big'),
            iv,
            size_buffer,
            rsa_encrypted,
            tag,
            aes_encrypted
        ]))
        return f"#PWD_INSTAGRAM:4:{timestamp}:{payload.decode()}"

    def password_publickeys(self):
        i = p()
        resp = i.public.get(url='https://i.instagram.com/api/v1/qe/sync/')
        publickeyid = int(resp.headers.get('ig-set-password-encryption-key-id'))
        publickey = resp.headers.get('ig-set-password-encryption-pub-key')
        return publickeyid, publickey

    def setProxy(self):
        try:
            with open('proxies.txt') as f:pr =f.read().splitlines()
            prox = random.choice(pr)
            self.r.proxies = {'http':'http://{}','https':'http://{}'.format(prox,prox)}
        except:return False
        

    def login(self,twofac=None):
        try:
            self.enc_password = self.password_encrypt(self.password)
            data = { "jazoest": generate_jazoest(self.phone_id), "country_codes": "[{\"country_code\":\"%d\",\"source\":[\"default\"]}]" % int(self.country_code), "phone_id": self.phone_id, "enc_password": self.enc_password, "username": self.username, "adid": self.advertising_id, "guid": self.uuid, "device_id": self.android_device_id, "google_tokens": "[]", "login_attempt_count": "0" }
            self.SendRequest('https://i.instagram.com/api/v1/accounts/login/', data)
            self.mid = self.response.headers.get("ig-set-x-mid")
            if twofac: print('2fac!');two_factor_identifier = self.Json.get('two_factor_info', {}).get('two_factor_identifier');data = { "verification_code": twofac, "phone_id": self.phone_id, "_csrftoken": self.token, "two_factor_identifier": two_factor_identifier, "username": self.username, "trust_this_device": "0", "guid": self.uuid, "device_id": self.android_device_id, "waterfall_id": str(uuid4()), "verification_method": "3" };self.SendRequest('https://i.instagram.com/api/v1/accounts/two_factor_login/', data)
            if 'logged_in_user' in self.Text and 'Instagram User' not in self.Text:
                if "challenge" in self.Text:return False
                self.authorization_data = self.parse_authorization(self.response.headers.get('ig-set-authorization'))
                self.session= self.authorization_data['sessionid'];self.username_id = self.authorization_data["ds_user_id"];self.my_pfp = self.Json['logged_in_user']['profile_pic_url']
                self.last_login = time.time()
                self.mid = self.response.headers.get("ig-set-x-mid")
                self.r.cookies['sessionid'] = self.session
                self.r.cookies['ds_user_id'] = self.username_id
                self.r.cookies['_csrftoken'] = self.token
                self.r.cookies['mid'] = self.mid
                self.rank_token = "%s_%s" % (self.username_id, self.uuid)
                self.login_flow()
                if "challenge" in self.Text:return False
                self.isloggedin=True;return True
                
            else:
                return False
        except Exception as e:print(e)
    @property
    def authorization(self) -> str:
        if self.authorization_data:
            b64part = base64.b64encode(
                dumps(self.authorization_data).encode()
            ).decode()
            return f'Bearer IGT:2:{b64part}'
        return ''

    def parse_authorization(self, authorization) -> dict:
        try:
            b64part = authorization.rsplit(':', 1)[-1]
            return json.loads(base64.b64decode(b64part))
        except Exception as e:
            self.logger.exception(e)
        return {}

    @property
    def token(self) -> str:
        if not getattr(self, '_token', None):
            self._token = self.cookie_dict.get("csrftoken", gen_token(64))
        return self._token

    def getUserFollowings(self,usernameId, maxid=''):
        url = 'friendships/' + str(usernameId) + '/following/?'
        query_string = {'ig_sig_key_version': '4','rank_token': self.rank_token}
        if maxid:query_string['max_id'] = maxid
        if sys.version_info.major == 3:url += urllib.parse.urlencode(query_string)
        else:url += urllib.urlencode(query_string)
        return self.SendRequest(url)

    def getUserFollowers(self, usernameId, maxid=''):
            if maxid == '':return self.SendRequest('friendships/' + str(usernameId) + '/followers/?rank_token=' + self.rank_token)
            else:return self.SendRequest('friendships/' + str(usernameId) + '/followers/?rank_token=' + self.rank_token + '&max_id=' + str(maxid))
    
    def getmid(self,media):
        try:
            media = media.split('/')[4].replace('/','')
            alphabet = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789-_'
            media_id = 0;
            for letter in media:
                media_id = (media_id*64) + alphabet.index(letter)
            
            return media_id
        except Exception as e:print(e);return 3
    
    
    def getmcode(self,media):
        try:return media.split('/')[4].replace('/','')
        except:return 3

    def GetAllFollowing(self, user_id,num):
        following = []
        next_max_id = True
        prev = False
        while next_max_id:
            if next_max_id is True:
                next_max_id = ''
            if self.getUserFollowings(user_id, maxid=next_max_id):
                for item in self.Json['users']:
                        user = str(item['pk'])
                        
                        with open('target.txt', "r") as f:lines = f.read().splitlines()
                        if user not in lines:
                            following.append(user)
                            with open('target.txt', 'a') as f:f.write(f'{user}\n')
                        else:prev = True
                        if len(following) == num:break
                next_max_id = self.Json.get('next_max_id', '')
                os.system('cls' if os.name == 'nt' else 'clear')
                print(banner)
                print(f'[RUNNING] Collected {len(following)} users so far...')
                if len(following) == num:break
        if len(following) > 0 and prev:print(f'\n[DONE] Collected {len(following)} new users!');time.sleep(4);return True
        if len(following) > 0:print(f'\n[DONE] Collected {len(following)} users!');time.sleep(4);return True
        else:print(f'[ERROR] Unable to scrape data from username: {self.target}');time.sleep(4);return False
        

    def GetAllFollowers(self,user_id,num):
        followers = []
        next_max_id = True
        prev = False
        while next_max_id:
            if next_max_id is True:
                next_max_id = ''
            if self.getUserFollowers(user_id, maxid=next_max_id):
                for item in self.Json['users']:
                    
                        user = str(item['pk'])
                        with open('target.txt', "r") as f:lines = f.read().splitlines()
                        if user not in lines:
                            followers.append(user)
                            with open('target.txt', 'a') as f:f.write(f'{user}\n')
                        else:prev = True
                        if len(followers) == num:break
                next_max_id = self.Json.get('next_max_id', '')
                os.system('cls' if os.name == 'nt' else 'clear')
                print(banner)
                print(f'[RUNNING] Collected {len(followers)} users so far...')
                if len(followers) == num:break
        if len(followers) > 0 and prev:print(f'\n[DONE] Collected {len(followers)} new users!');time.sleep(4);return True
        if len(followers) > 0:print(f'\n[DONE] Collected {len(followers)} users!');time.sleep(4);return True
        else:print(f'[ERROR] Unable to scrape new data from username: {self.target}');time.sleep(4);return False

    def likescrape(self, code, num):
        users = []
        url = 'https://www.instagram.com/graphql/query/?query_hash=d5d763b1e2acf209d62d22d184488e57&variables={%22shortcode%22:%22'+code+'%22,%22include_reel%22:true,%22first%22:1000}'
        x = self.r.get(url)
        if x.status_code ==200:
            for item in x.json()['data']['shortcode_media']['edge_liked_by']['edges']:
                liker = str(item['node']['id'])
                users.append(liker)
                with open("target.txt", "r") as f:lines = f.read().splitlines()
                if liker not in lines:
                    with open('target.txt', 'a') as f:f.write(f'{liker}\n')
                if len(users) == num:break
            while x.json()['data']['shortcode_media']['edge_liked_by']['page_info']['has_next_page']:
                if len(users) == num:break
                end = x.json()['data']['shortcode_media']['edge_liked_by']['page_info']['end_cursor'] 
                print(f'[RUNNING] Collected {len(users)}/{num} users so far...')
                time.sleep(5)
                x = self.r.get('https://www.instagram.com/graphql/query/?query_hash=d5d763b1e2acf209d62d22d184488e57&variables={%22shortcode%22:%22'+code+'%22,%22include_reel%22:true,%22first%22:1000,%22after%22:%22'+end+'%22}')
                for item in x.json()['data']['shortcode_media']['edge_liked_by']['edges']:
                    liker = str(item['node']['id'])
                    users.append(liker)
                    with open("target.txt", "r") as f:lines = f.read().splitlines()
                    if liker not in lines:
                        with open('target.txt', 'a') as f:f.write(f'{liker}\n')
                    if len(users) == num:break
        
        if len(users) > 0:print(f'[DONE] Collected {len(users)} users!');time.sleep(4);return True
        else:print('[ERROR] Something went wrong...');time.sleep(4);return False

    def search(self,usernameName):
        if self.isloggedin:
            self.target = usernameName
            query = self.r.get('https://i.instagram.com/api/v1/users/' + str(usernameName) + '/usernameinfo/').json()
            if query['status'] =='ok':return str(query['user']['pk'])
            else:return 3

    def generateUUID(self, type):
        generated_uuid = str(uuid.uuid4())
        if (type):
            return generated_uuid
        else:
            return generated_uuid.replace('-', '')

    def post_share(self, media_id, recipients, text=None):
        if not isinstance(recipients, list):recipients = [str(recipients)]
        recipient_users = '"",""'.join(str(r) for r in recipients)
        boundary = self.uuid
        bodies = [ { 'type': 'form-data', 'name': 'media_id', 'data': media_id, }, { 'type': 'form-data', 'name': 'recipient_users', 'data': '[["{}"]]'.format(recipient_users), }, { 'type': 'form-data', 'name': 'client_context', 'data': self.uuid, }, { 'type': 'form-data', 'name': 'thread', 'data': '["0"]', }, { 'type': 'form-data', 'name': 'text', 'data': text or '', }, ]
        data = self.buildBody(bodies, boundary)
        headers= {'User-Agent': self.useragent, 'Proxy-Connection': 'keep-alive', 'Connection': 'keep-alive', 'Accept': '*/*', 'Content-Type': 'multipart/form-data; boundary={}'.format(boundary), 'Accept-Language': 'en-en'}
        return self.SendRequest('https://i.instagram.com/api/v1/direct_v2/threads/broadcast/media_share/?media_type=photo', data=data,headers=headers)

    def remove(self,recipient):
        global targets
        targets.remove(recipient)
        with open("target.txt", "r") as f:lines = f.readlines()
        with open("target.txt", "w") as f:
            for line in lines:
                if line.strip("\n") != recipient:
                    f.write(line)
    
    def message(self, target_user,text):
        target_user = f'[[{",".join([str(target_user)])}]]'
        token = str(random.randint(6800011111111111111, 6800099999999999999))
        data = {
            'text': text,
            '_uuid': self.uuid,
            '_csrftoken': self.token,
            'recipient_users': target_user,
            '_uid': self.username_id,
            'action': 'send_item',
            'client_context': token,
            "mutation_token": token,
            "nav_chain": "1qT:feed_timeline:1,1qT:feed_timeline:2,1qT:feed_timeline:3,7Az:direct_inbox:4,7Az:direct_inbox:5,5rG:direct_thread:7",
            "offline_threading_id": token,
        }
        #kwargs = {'action': 'send_item', 'is_shh_mode': '0', 'send_attribution': 'direct_thread', 'client_context': '6800052132112160764', 'mutation_token': '6800052132112160764', 'nav_chain': '1qT:feed_timeline:1,1qT:feed_timeline:2,1qT:feed_timeline:3,7Az:direct_inbox:4,7Az:direct_inbox:5,5rG:direct_thread:7', 'offline_threading_id': '6800052132112160764', 'text': 'yo', 'recipient_users': 237322046}
        return self.SendRequest(
            f"direct_v2/threads/broadcast/text/",
            data=self.generateSignature(json.dumps(data))),
