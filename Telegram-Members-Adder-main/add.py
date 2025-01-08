'''
================SAIFALISEW1508=====================
Telegram members adding script
Coded by BRHOT - github.com/saifalisew1508
Apologies if anything in the code is dumb :)
Copy with credits
************************************************
'''

# استيراد المكتبات
from telethon.sync import TelegramClient
from telethon.tl.types import InputPeerChannel
from telethon.errors.rpcerrorlist import PeerFloodError, UserPrivacyRestrictedError, PhoneNumberBannedError, ChatAdminRequiredError
from telethon.errors.rpcerrorlist import ChatWriteForbiddenError, UserBannedInChannelError, UserAlreadyParticipantError, FloodWaitError
from telethon.tl.functions.channels import InviteToChannelRequest
import sys
from telethon.tl.functions.messages import ImportChatInviteRequest, AddChatUserRequest
from telethon.tl.functions.channels import JoinChannelRequest
import time
import random
from colorama import init, Fore
import os
import pickle
import socket
from threading import Thread

# تهيئة واجهة الألوان
init()
r = Fore.RED
lg = Fore.GREEN
rs = Fore.RESET
w = Fore.WHITE
grey = '\033[97m'
cy = Fore.CYAN
ye = Fore.YELLOW
colors = [r, lg, w, ye, cy]
info = f'{lg}[{w}i{lg}]{rs}'
error = f'{lg}[{r}!{lg}]{rs}'
success = f'{w}[{lg}*{w}]{rs}'
INPUT = f'{lg}[{cy}~{lg}]{rs}'
plus = f'{w}[{lg}+{w}]{rs}'
minus = f'{w}[{lg}-{w}]{rs}'

def banner():
    # شعار مع الألوان
    b = [
        '░█████╗░██████╗░██████╗░███████╗██████╗░',
        '██╔══██╗██╔══██╗██╔══██╗██╔════╝██╔══██╗',
        '███████║██║░░██║██║░░██║█████╗░░██████╔╝',
        '██╔══██║██║░░██║██║░░██║██╔══╝░░██╔══██╗',
        '██║░░██║██████╔╝██████╔╝███████╗██║░░██║',
        '╚═╝░░╚═╝╚═════╝░╚═════╝░╚══════╝╚═╝░░╚═╝'
    ]
    for char in b:
        print(f'{random.choice(colors)}{char}{rs}')
    print('Contact below address for get premium script')
    print(f'{lg}Version: {w}2.0{lg} | GitHub: {w}@saifalisew1508{rs}')
    print(f'{lg}Telegram: {w}@DearSaif{lg} | Instagram: {w}@_Prince.Babu_{rs}')

def clr():
    if os.name == 'nt':
        os.system('cls')
    else:
        os.system('clear')

def log_message(message):
    with open('log.txt', 'a') as log_file:
        log_file.write(f'{time.ctime()} - {message}\n')

def check_internet():
    try:
        socket.create_connection(("1.1.1.1", 53))
        return True
    except OSError:
        return False

def save_progress(scraped_grp, index):
    with open('progress.pkl', 'wb') as progress_file:
        pickle.dump({'group': scraped_grp, 'index': index}, progress_file)

# فحص الاتصال بالإنترنت
if not check_internet():
    print(f'{error}{r} تأكد من اتصالك بالإنترنت.')
    sys.exit()

# قراءة الحسابات
accounts = []
f = open('vars.txt', 'rb')
while True:
    try:
        accounts.append(pickle.load(f))
    except EOFError:
        break

# فحص الحسابات المحظورة
print('\n' + info + lg + ' Checking for banned accounts...' + rs)
banned = []
for a in accounts:
    phn = a[0]
    print(f'{plus}{grey} Checking {lg}{phn}')
    clnt = TelegramClient(f'sessions/{phn}', 3910389, '86f861352f0ab76a251866059a6adbd6')
    clnt.connect()
    if not clnt.is_user_authorized():
        try:
            clnt.send_code_request(phn)
            print('OK')
        except PhoneNumberBannedError:
            print(f'{error} {w}{phn} {r}is banned!{rs}')
            banned.append(a)
    for z in banned:
        accounts.remove(z)
        print(info+lg+' Banned account removed[Remove permanently using manager.py]'+rs)
    time.sleep(0.5)
    clnt.disconnect()

print(f'{info} Sessions created!')
clr()
banner()

# قراءة الحالة السابقة إذا كانت موجودة
try:
    with open('progress.pkl', 'rb') as f:
        status = pickle.load(f)
        f.close()
        lol = input(f'{INPUT}{cy} Resume scraping members from {w}{status["group"]}{lg}? [y/n]: {r}')
        if 'y' in lol:
            scraped_grp = status["group"]
            index = int(status["index"])
        else:
            os.remove('progress.pkl')
            scraped_grp = input(f'{INPUT}{cy} Public/Private group url link to scrape members: {r}')
            index = 0
except:
    scraped_grp = input(f'{INPUT}{cy} Public/Private group url link to scrape members: {r}')
    index = 0

print(f'{info}{lg} Total accounts: {w}{len(accounts)}')
number_of_accs = int(input(f'{INPUT}{cy} How Many Accounts You Want Use In Adding: {r}'))
print(f'{info}{cy} Choose an option{lg}')
print(f'{cy}[0]{lg} Add to public group')
print(f'{cy}[1]{lg} Add to private group')
choice = int(input(f'{INPUT}{cy} Enter choice: {r}'))
if choice == 0:
    target = str(input(f'{INPUT}{cy} Enter public group url link: {r}'))
else:
    target = str(input(f'{INPUT}{cy} Enter private group url link: {r}'))

print(f'{grey}_'*50)
status_choice = str(input(f'{INPUT}{cy} Do you wanna add active members?[y/n]: {r}'))
to_use = list(accounts[:number_of_accs])
for l in to_use: accounts.remove(l)

# تحديد وقت التأخير بين الطلبات
sleep_time = int(input(f'{INPUT}{cy} Enter delay time per request{w}[{lg}0 for None, i suggest enter 30 to add members properly{w}]: {r}'))

# تحديد الوظيفة لإضافة الأعضاء
def add_members(account):
    c = TelegramClient(f'sessions/{account[0]}', 3910389 , '86f861352f0ab76a251866059a6adbd6')
    c.start(account[0])
    acc_name = c.get_me().first_name
    try:
        if '/joinchat/' in scraped_grp:
            g_hash = scraped_grp.split('/joinchat/')[1]
            try:
                c(ImportChatInviteRequest(g_hash))
                print(f'{plus}{grey} User: {cy}{acc_name}{lg} -- Joined group to scrape')
            except UserAlreadyParticipantError:
                pass 
        else:
            c(JoinChannelRequest(scraped_grp))
            print(f'{plus}{grey} User: {cy}{acc_name}{lg} -- Joined group to scrape')
        scraped_grp_entity = c.get_entity(scraped_grp)
        if choice == 0:
            c(JoinChannelRequest(target))
            print(f'{plus}{grey} User: {cy}{acc_name}{lg} -- Joined group to add')
            target_entity = c.get_entity(target)
            target_details = InputPeerChannel(target_entity.id, target_entity.access_hash)
        else:
            try:
                grp_hash = target.split('/joinchat/')[1]
                c(ImportChatInviteRequest(grp_hash))
                print(f'{plus}{grey} User: {cy}{acc_name}{lg} -- Joined group to add')
            except UserAlreadyParticipantError:
                pass
            target_entity = c.get_entity(target)
            target_details = target_entity
    except Exception as e:
        print(f'{error}{r} User: {cy}{acc_name}{lg} -- Failed to join group')
        print(f'{error} {r}{e}')
        return

    c.get_dialogs()
    try:
        members = c.get_participants(scraped_grp_entity, aggressive=False)
    except Exception as e:
        print(f'{error}{r} Couldn\'t scrape members')
        print(f'{error}{r} {e}')
        return
    
    approx_members_count = len(members)
    assert approx_members_count != 0
    if index >= approx_members_count:
        print(f'{error}{lg} No members to add!')
        return

    print(f'{info}{lg} Start: {w}{index}')
    adding_status = 0
    peer_flood_status = 0
    for user in members[index:index + 60]:
        index += 1
        if peer_flood_status == 10:
            print(f'{error}{r} Too many Peer Flood Errors! Closing session...')
            break
        try:
            if choice == 0:
                c(InviteToChannelRequest(target_details, [user]))
            else:
                c(AddChatUserRequest(target_details.id, user, 42))
            user_id = user.first_name
            target_title = target_entity.title
            print(f'{plus}{grey} User: {cy}{acc_name}{lg} -- {cy}{user_id} {lg}--> {cy}{target_title}')
            adding_status += 1
            print(f'{info}{grey} User: {cy}{acc_name}{lg} -- Sleep {w}{sleep_time} {lg}second(s)')
            time.sleep(sleep_time)
        except PeerFloodError:
            print(f'{error}{grey} User: {cy}{acc_name}{lg} -- {r}Peer Flood Error.')
            peer_flood_status += 1
            continue
        except FloodWaitError as e:
            print(f'{error}{r} {e}')
            time.sleep(e.seconds + 10)  # الانتظار مع إضافة وقت احتياطي
            continue
        except Exception as e:
            print(f'{error} {e}')
            continue

# تشغيل الوظائف عبر عدة خيوط (Threads)
threads = []
for acc in to_use:
    thread = Thread(target=add_members, args=(acc,))
    threads.append(thread)
    thread.start()

for thread in threads:
    thread.join()

print(f"{info}{lg} Adding session ended")
save_progress(scraped_grp, index)
