init -990 python:
    store.mas_submod_utils.Submod(
        author="P",
        name="Loop Play",
        description="允许你循环播放MAS内的音乐",
        version='0.1.0'
    )

init -989 python:
    if store.mas_submod_utils.isSubmodInstalled("Submod Updater Plugin"):
        store.sup_utils.SubmodUpdater(
            submod="Loop Play",
            user_name="PencilMario",
            repository_name="Loop_Play_Submod",
            update_dir="",
            attachment_id=None
        )

init python:
    class MusicQueue(object):
        playlist = []
        paused = False
        loopmode = False
        currplaying = ""
        """docstring for ClassName"""
        def __init__(self):
            self.playlist = self.Music_GetCatchSaveList()

        def Get_CurrPlaying(self):
            self.currplaying = renpy.music.get_playing()
            return self.currplaying

        def Pause(self):
            renpy.music.set_pause(not self.paused)
            self.paused = not self.paused

        def Next_Music_List(self):
            """
            获取以下一首音乐为开头的list
            """
            musicqueue = []
            currplaying = self.Get_CurrPlaying()
            pos = self.playlist.index(self.currplaying) + 1 
            length = len(self.playlist)
            if pos>length:
                pos = length

            newlist1 = self.playlist[pos:length]
            newlist2 = self.playlist[0:pos]
            musicqueue = newlist1+newlist2
            #i = pos + 1
            #if i > length:
            #    i = 1
            #while i <= length:
            #    musicqueue.append(self.playlist[i-1])
            #    i = i + 1
            #i=1
            #while i < pos:
            #    musicqueue.append(self.playlist[i-1])
            #    i = i + 1
            return musicqueue

        def Prev_Music_List(self):
            """
            获取以上一首音乐为开头的list
            """
            musicqueue = []
            currplaying = self.Get_CurrPlaying()
            pos = self.playlist.index(self.currplaying)
            length = len(self.playlist)
            if pos < 0:
                pos = 0
            #if i < 1:
            #    i = length
            #while i <= length:
            #    musicqueue.append(self.playlist[i-1])
            #    i = i+1
            #i=1
            #while i < pos:
            #    musicqueue.append(self.playlist[i-1])
            #    i = i+1
            newlist1 = self.playlist[pos-1:length]
            newlist2 = self.playlist[0:pos-1]
            musicqueue=newlist1+newlist2
            return musicqueue

        def Now_Music_List(self, song):
            """
            获取以指定音乐为开头的list
            """
            musicqueue = []
            currplaying = self.Get_CurrPlaying()
            pos = self.playlist.index(song)
            length = len(self.playlist)
            if pos>length:
                pos = length

            newlist1 = self.playlist[pos:length]
            newlist2 = self.playlist[0:pos]
            musicqueue = newlist1+newlist2
            #i = pos + 1
            #if i > length:
            #    i = 1
            #while i <= length:
            #    musicqueue.append(self.playlist[i-1])
            #    i = i + 1
            #i=1
            #while i < pos:
            #    musicqueue.append(self.playlist[i-1])
            #    i = i + 1
            return musicqueue
        
        def Prev_Music(self):
            """
            播放上一首音乐
            """
            if not self.loopmode:
                self.Play_Music_Now(self.playlist[0])
                self.loopmode=True
            else:
                mlist = self.Prev_Music_List()
                self.Music_Play_List(song=mlist)
                return self.Get_CurrPlaying()
        
        def Next_Music(self):
            """
            播放下一首音乐
            """
            if not self.loopmode:
                self.Play_Music_Now(self.playlist[0])
                self.loopmode=True
            else:
                mlist = self.Next_Music_List()
                self.Music_Play_List(song=mlist)
                return self.Get_CurrPlaying()

        def Play_Music_Now(self, song):
            """
            立刻播放指定音乐
            """
            self.loopmode=True
            mlist = self.Now_Music_List(song)
            self.Music_Play_List(song=mlist)
            return self.Get_CurrPlaying()

        def Get_ShortName(self):
            """
            返回短名称音乐列表
            """
            dirs = os.listdir(renpy.config.basedir+ "/custom_bgm/")
            catched = []
            file_type = ["mp3", "wav", "ogg"]
            for file_name in dirs:
                playable = False
                for type in file_type:
                    if file_name.find(type) != 1:
                        playable = True
                        break
                if playable == True:
                    catched.append((file_name).replace("\\","/"))
            return catched

        def Music_GetCatchSaveList(self):
            """
            获取音乐列表
            """
            dirs = os.listdir(renpy.config.basedir+ "/custom_bgm/")
            catched = []
            file_type = ["mp3", "wav", "ogg"]
            for file_name in dirs:
                playable = False
                for type in file_type:
                    if file_name.find(type) != 1:
                        playable = True
                        break
                if playable == True:
                    catched.append((renpy.config.basedir + "/custom_bgm/" + file_name).replace("\\","/"))
            return catched
        
        def Music_Play_List(self, song, fadein=1.2, loop=True, set_per=False, fadeout=1.2, if_changed=False):
            """
            播放已缓存列表
            IN:
                song - Song to play. If None, the channel is stopped
                fadein - Number of seconds to fade the song in
                    (Default: 0.0)
                loop - True if we should loop the song if possible, False to not loop.
                    (Default: True)
                set_per - True if we should set persistent track, False if not
                    (Default: False)
                fadeout - Number of seconds to fade the song out
                    (Default: 0.0)
                if_changed - Whether or not to only set the song if it's changing
                    (Use to play the same song again without it being restarted)
                    (Default: False)
            """
            if song is None or song == []:
                renpy.music.stop(channel="music", fadeout=fadeout)
            else:
                renpy.music.play(
                    song,
                    channel="music",
                    loop=loop,
                    synchro_start=True,
                    fadein=fadein,
                    fadeout=fadeout,
                    if_changed=if_changed
                )    
    lp_queue = MusicQueue()

init 5 python:
    addEvent(
            Event(
                persistent.event_database,          
                eventlabel="loop_play",       
                category=["媒体"],                   
                prompt="循环播放音乐",     
                pool=True,
                unlocked=True
            ),
        restartBlacklist=True
        )

label loop_play:                               
    menu:
        "更新播放队列":
            $ lp_queue = MusicQueue()
        "上一首":
            $ lp_queue.Prev_Music()
        "下一首":
            $ lp_queue.Next_Music()
        "暂停":
            $ lp_queue.Pause()
    
    "OK - [lp_queue.currplaying]"
        
return                                                     
