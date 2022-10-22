import os
import re
import shutil
import sys
import time
import random

from yt_dlp import YoutubeDL
from internetarchive import get_item, upload
from TikTokApi import TikTokApi
#Make sure to change to 'from .argparser import parse_args' when uploading
from .argparser import parse_args


api = TikTokApi()


def getVersion():
    return '2022.10.10'


def getUsernameVideos(username, limit):
    if limit is not None:
        count = int(limit)
    else:
        count = 9999
    user = api.user(username, count=limit)
    user.as_dict # -> dict of the user_object
    tiktok_list = []
    for video in user.videos():
        video.as_dict 
        tiktok_list.append((value[0], key))
    return tiktok_list

def getHashtagVideos(hashtag, limit):
    if limit is not None:
        count = int(limit)
    else:
        count = 9999
    hashtag = api.hashtag(name=hashtag, count=limit)
    hashtag.as_dict # -> dict of the user_object
    tiktok_list = []
    for video in hashtag.videos():
        video.as_dict 
        tiktok_list.append((value[0], key))
    return tiktok_list

def getSoundVideos(sound, limit):
    if limit is not None:
        count = int(limit)
    else:
        count = 9999
    sound = api.sound(name=sound, count=limit)
    sound.as_dict # -> dict of the user_object
    tiktok_list = []
    for video in sound.videos():
        video.as_dict 
        tiktok_list.append((value[0], key))
    return tiktok_list

def getLikedVideos(username, limit):
    if limit is not None:
        count = int(limit)
    else:
        count = 9999
    user = api.user(username, count=limit)
    user.as_dict # -> dict of the user_object
    tiktok_list = []
    for liked_video in user.videos():
        video.as_dict 
        tiktok_list.append((value[0], key))
    return tiktok_list

def downloadTikTok(username, tiktok, cwd, varTry, did):
    try:
        tiktokID = tiktok['id']
    except:
        try:
            tiktokID = tiktok['itemInfos']['id']
        except:
            tiktokID = tiktok['itemInfo']['itemStruct']['id']
    ydl_opts = {
        'writeinfojson': True,
        'writedescription': True,
        'write_all_thumbnails': True,
        'writeannotations': True,
        'writesubtitles': True,
        'allsubtitles': True,
        'ignoreerrors': True,
        'fixup': True,
        'quiet': True,
        'no_warnings': True,
        'restrictfilenames': True,
        'nooverwrites': True,
        'outtmpl': tiktokID + '.mp4',
    }
    if not os.path.exists(tiktokID):
        os.mkdir(tiktokID)
    os.chdir(tiktokID)
    filesExist = (os.path.exists(tiktokID + '.description') 
                  and os.path.getsize(tiktokID + '.description') > 0) 
                  and (os.path.exists(tiktokID + '.info.json') 
                  and os.path.getsize(tiktokID + '.info.json') > 0) 
                  and (os.path.exists(tiktokID + '.jpg')                
                  and os.path.getsize(tiktokID + '.jpg') > 0) 
                  and (os.path.exists(tiktokID + '.mp4') 
                  and os.path.getsize(tiktokID + '.mp4') > 0) 
                  and (os.path.exists('tiktok_info.json') 
                  and os.path.getsize('tiktok_info.json') > 0) 
                  and (os.path.exists('comments.json') 
                  and os.path.getsize('comments.json') > 0)
    if not filesExist:
        if varTry % 3 != 0:
            with YoutubeDL(ydl_opts) as ydl:
                # ydl.download([tiktok['itemInfo']['itemStruct']['video']['downloadAddr']])
                ydl.download(['https://www.tiktok.com/@' + username + '/video/' + tiktokID])
        else:
            mp4 = open(tiktokID + '.mp4', "wb")
            mp4.write(api.get_video_by_download_url(tiktok['itemInfo']['itemStruct']['video']['downloadAddr'], custom_did=did))
            mp4.close()
            #shutil.rmtree('tmp')
        try:
            mp4 = open(tiktokID + '.mp4', "r", encoding="latin-1")
            # For some reason, ytdl sometimes downloads the HTML page instead of the video
            # this removes the HTML
            check = str(mp4.read())[:15]
            if (check == '<!DOCTYPE html>') or (check[:6] == '<HTML>'):
                mp4.close()
                os.remove(tiktokID + '.mp4')
            else:
                mp4.close()
        except FileNotFoundError:
            pass
        x = os.listdir()
        for i in x:
            if i.endswith('.unknown_video'):
                base = os.path.splitext(i)[0]
                if os.path.exists(base + '.mp4'):
                    os.remove(base + '.mp4')
                os.rename(i, base + '.mp4')
        tiktokinfo = api.video(id='tiktokID').info_full()
        json = open("tiktok_info.json", "w", encoding="utf-8")
        json.write(str(tiktokinfo))
        json.close()
        if comments == True:
          json = open("comments.json", "w", encoding="utf-8")
          for comment in video.comments:
                json.write(comment.as_dict)
    os.chdir(cwd)


def uploadTikTok(username, tiktok, deletionStatus, file):
    regex = re.compile('[0-9]{17}')
    regexA = re.compile('[0-9]{18}')
    regexB = re.compile('[0-9]{19}')
    regexC = re.compile('[0-9]{8}')
    regexD = re.compile('[0-9]{9}')
    if os.path.isdir(tiktok):
        if (
            regex.match(str(tiktok))
            or (regexA.match(str(tiktok)))
            or (regexB.match(str(tiktok)))
            or (regexC.match(str(tiktok)))
            or (regexD.match(str(tiktok)))
        ):  # TODO: use or regex with "|" instead of this
            item = get_item('tiktok-' + tiktok)
            if username is None:
                if file is not None:
                    file.write(str(tiktok))
                    file.write('\n')
                return None
            item.upload(
                './' + tiktok + '/',
                verbose=True,
                checksum=True,
                delete=deletionStatus,
                metadata=dict(
                    collection='opensource_movies',
                    subject='tiktok',
                    creator=username,
                    title='TikTok Video by ' + username,
                    originalurl='https://www.tiktok.com/@' + username + '/video/' + tiktok,
                    scanner='TikUp Neo ' + getVersion(),
                ),
                retries=9001,
                retries_sleep=60,
            )
            if deletionStatus:
                os.rmdir(tiktok)
            print()
            print('Uploaded to https://archive.org/details/tiktok-' + tiktok)
            print()
            if file is not None:
                file.write(str(tiktok))
                file.write('\n')


def downloadTikToks(username, tiktoks, file, downloadType, did):
    cwd = os.getcwd()
    try:
        lines = file.readlines()
        for x in range(0, len(lines)):
            lines[x] = lines[x].replace('\n', '')
    except:
        lines = ''
    ids = []
    for tiktok in tiktoks:
        if str(type(tiktok)) == '<class \'dict\'>':
            try:
                tiktok = tiktok['id']
            except KeyError:
                tiktok = tiktok['itemInfos']['id']
        if file is not None and doesIdExist(lines, tiktok):
            print(tiktok + " has already been archived.")
        else:
            tiktokObj = getTikTokObject(tiktok, did)
            username = getUsername(tiktok)
            if username is None:
                print(tiktok + ' has been deleted or is private')
                ids.append(tiktok)
            else:
                downloadTikTok(username, tiktokObj, cwd, 1, did)
                i = 1
                while not os.path.exists(tiktok + '/' + tiktok + '.mp4'):
                    tiktokObj = getTikTokObject(tiktok, did)
                    username = getUsername(tiktok)
                    time.sleep(1)
                    downloadTikTok(username, tiktokObj, cwd, i, did)
                    i += 1
                print(tiktok + ' has been downloaded')
                ids.append(tiktok)
    return ids


def uploadTikToks(tiktoks, file, delete):
    for tiktok in tiktoks:
        uploadTikTok(getUsername(tiktok), tiktok, delete, file)


def doesIdExist(lines, tiktok):
    return tiktok in lines


def getUsername(tiktokId):
    thing = api.get_tiktok_by_id(tiktokId)
    try:
        return thing['itemInfo']['itemStruct']['author']['uniqueId']
    except:
        return None


def getTikTokObject(tiktokId, did):
    
    thing = api.video(id=tiktokId, custom_did=did)
    return thing


def main():
    args = parse_args()
    username = args.user
    delete = args.no_delete
    limit = args.limit
    archive = args.use_download_archive
    folder = args.folder
    sound = args.sound
    comments = args.comments 
    global upload
    upload = args.no_upload

    if folder == None:
        os.chdir(os.path.expanduser('~'))
        if not os.path.exists('./.tikup'):
            os.mkdir('./.tikup')
        os.chdir('./.tikup')
    else:
        if not os.path.exists(folder):
            os.mkdir(folder)
        os.chdir(folder)

    downloadType = ''
    if archive:
        try:
            file = open('archive.txt', 'r+')
        except FileNotFoundError:
            f = open('archive.txt', 'x')
            f.close()
            file = open('archive.txt', 'r+')
    else:
        file = None
    did = str(random.randint(10000, 999999999))
    if args.hashtag:  # Download hashtag
        downloadType = 'hashtag'
        tiktoks = getHashtagVideos(username, limit)
    elif args.id:  # Download user ID
        downloadType = 'id'
        tiktoks = [username]
    elif args.liked:  # Download liked
        downloadType = 'liked'
        tiktoks = getLikedVideos(username, limit)
    elif args.sound:  # Download videos of a music track
        downloadType = 'sound'
        tiktoks = getSoundVideos(sound, limit)
    else:  # Download username
        downloadType = 'username'
        tiktoks = getUsernameVideos(username, limit)
    tiktoks = downloadTikToks(username, tiktoks, file, downloadType, did)
    if upload == True:
        uploadTikToks(tiktoks, file, delete)

    try:
        for tiktok_id in tiktoks:
            file.write(tiktok_id + '\n')
        file.close()
    except:
        pass
    print('')


if __name__ == "__main__":
    main()
