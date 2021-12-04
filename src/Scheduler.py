import configparser
import os.path
import Config as c
import Generator
import Logger

class Block:

    def __init__(self, name, folder, num_files, bump_chance, prev_block):
        self.name = name
        self.folder = folder
        self.num_files = num_files
        self.bump_chance = bump_chance
        self.playlist = []
        self.prev_block = prev_block
        
        playlist, prev_block = Generator.gen_playlist(folder, num_files, prev_block)
        
        upnext = Generator.gen_upnext(	c.SCHEDULER_UPNEXT_VIDEO_FOLDER,
                                       c.SCHEDULER_UPNEXT_AUDIO_FOLDER,
                                       playlist=playlist,
                                       info_file=c.SCHEDULER_UPNEXT_WISDOM_FILE)

        self.playlist += [upnext] + playlist



class Scheduler:

    def __init__(self, input_file):
        self.config = configparser.ConfigParser()
        if not os.path.isfile(input_file):
            Logger.LOGGER.log(Logger.TYPE_INFO,
                    'Playout file not found!: {}'.format(input_file))
        self.config.read(input_file)

        self.blocklist = []

        c = self.config
        prev_block = []
        foo=1
        for i in self.config.sections():
            # print("\n############ BLOCK: ",foo,"\n")
            # foo+=1

            # print("\n############ FILES: ",c[i]['files'],"\n")

            block = Block(c[i]['name'], c[i]['folder'], c[i]
                          ['files'], float(c[i]['bump_chance']), prev_block)
            prev_block = block.prev_block
            self.blocklist.append(block)