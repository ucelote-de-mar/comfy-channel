import os
import random
from datetime import datetime, timedelta

import Logger
from MediaItem import MediaItem


def get_time_hm():
    return datetime.now()


def listdir_nohidden(path):
    for f in os.listdir(path):
        if not f.startswith('.'):
            yield os.path.join(path, f)

def listdir_file_walk(dir):
    directory_listing = []

    for path, dirs, files in os.walk(dir):
        files = [f for f in files if not f[0] == '.']
        dirs[:] = [d for d in dirs if not d[0] == '.']
        for name in files:
            directory_listing += [os.path.join(path, name)]

    return directory_listing


def gen_playlist(dir, num_files=5, prev_block=[]):
    num_files=int(num_files)
    Logger.LOGGER.log(Logger.TYPE_INFO,
                      'Generating playlist from directory: {}'.format(dir))
    playlist = []
    directory_listing = []
    
    already_played = open('random_test.txt', 'a')
    already_played.write('HERE IT COMES...\n')

    # https://stackoverflow.com/questions/2909975/python-list-directory-subdirectory-and-files
    for path, dirs, files in os.walk(dir):
        files = [f for f in files if not f[0] == '.']
        dirs[:] = [d for d in dirs if not d[0] == '.']
        for name in files:
            directory_listing += [os.path.join(path, name)]

    # Do not repeat songs that often

    # print("\n DIRECTORY LISTING \n")
    # for x in directory_listing:
    #     print(x)
    # print("\n PREV BLOCK \n")
    # for x in prev_block:
    #     print(x)

    directory_left = [x for x in directory_listing if x not in prev_block]

    # print("\n DIRECTORY LEFT \n")
    # for x in directory_left:
    #     print(x)

    if len(directory_left) < num_files:

        # print("\n############ NOT ENOUGH FILES: \n")

        following_vids = [x for x in directory_listing if x not in directory_left]

        random.shuffle(directory_left)
        random.shuffle(following_vids)
        directory_left += following_vids
        directory_listing = directory_left

        prev_block = [x for x in prev_block if x not in directory_listing]
    else:
        random.shuffle(directory_left)
        directory_listing = directory_left

    # print("\n DIRECTORY LEFT shuffled \n")
    # for x in directory_left:
    #     print(x)

    for i in directory_listing[:num_files]:
        already_played.write(i+"\n")
        prev_block += i
        playlist.append(MediaItem(i))
    already_played.close()

    # print("\n PREV BLOCK \n")
    # for x in prev_block:
    #     print(x)

    return playlist, prev_block

def gen_upnext(video_dir, audio_dir=None, playlist=None, info_file=None):
    video_file = None
    audio_file = None
    info_text = None

    video_file = random.choice(list(listdir_nohidden(video_dir)))
    audio_file = random.choice(listdir_file_walk(audio_dir))

    if playlist:
        info_text = gen_upnext_text(playlist, info_file=info_file)

    return MediaItem(video_path=video_file, audio_path=audio_file, media_type="upnext", overlay_text=info_text)


def gen_upnext_text(playlist, info_file=None):
    overlay_text = ""
    time_index = get_time_hm()
    time_index += timedelta(seconds=30)
    for i in range(len(playlist)):
        item = playlist[i]
        if i == 0:
            overlay_text += 'Next -' + \
            "  " + item.title + "\n\n"
        else:
            overlay_text += time_index.strftime("%H:%M") + ' -' + \
            "  " + item.title + "\n\n"
        time_index += timedelta(seconds=(item.duration/1000))

    if info_file:
        overlay_text += "\n" + get_random_line(info_file)

    return overlay_text


def get_random_line(file):
    file = open(file)
    random_line = random.choice(file.readlines())
    random_line += str("\n")
    file.close()
    return random_line
