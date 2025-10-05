init -990 python:
    store.mas_submod_utils.Submod(
        author="P and heart",
        name="Loop Play",
        description="允许你循环/循环播放MAS内的音乐",
        version='1.0'
    )

init -989 python:
    if store.mas_submod_utils.isSubmodInstalled("Submod Updater Plugin"):
        store.sup_utils.SubmodUpdater(
            submod="Loop Play",
            user_name="MAS-Submod-MoyuTeam",
            repository_name="Loop_Play_Submod",
            update_dir="",
            attachment_id=None
        )

default persistent._loop_play_shuffle_mode = False
default persistent._loop_play_auto_resume = False

init python:
    import os
    
    if renpy.android:
        external_dir = "/storage/emulated/0/MAS/custom_bgm"

        if os.path.isdir(external_dir):
            # 追加到 Ren'Py 的搜索路径
            renpy.config.searchpath.append(external_dir)

init python:        
    import random
        
    class MusicQueue(object):
        playlist = []
        shuffled_playlist = []
        paused = False
        loopmode = False
        shuffle_mode = False
        currplaying = ""
        """docstring for ClassName"""
        def __init__(self):
            self.playlist = self.Music_GetCatchSaveList()
            self.shuffled_playlist = self.playlist[:]  # 复制原始播放列表
            random.shuffle(self.shuffled_playlist)  # 初始化时打乱顺序
            if persistent._loop_play_shuffle_mode is not None:
                self.shuffle_mode = persistent._loop_play_shuffle_mode

        def Get_CurrPlaying(self):
            self.currplaying = renpy.music.get_playing()
            return self.currplaying

        def Pause(self):
            renpy.music.set_pause(not self.paused)
            self.paused = not self.paused

        def Toggle_Shuffle(self):
            """
            切换随机播放模式
            """
            self.shuffle_mode = not self.shuffle_mode
            persistent._loop_play_shuffle_mode = self.shuffle_mode
            if self.shuffle_mode:
                # 如果启用随机播放，重新打乱播放列表
                self.shuffled_playlist = self.playlist[:]
                random.shuffle(self.shuffled_playlist)
                # 确保当前播放的歌曲在随机列表中的位置合适
                if self.currplaying and self.currplaying in self.shuffled_playlist:
                    curr_index = self.shuffled_playlist.index(self.currplaying)
                    if curr_index > 0:
                        # 将当前播放的歌曲移到列表开头
                        self.shuffled_playlist.pop(curr_index)
                        self.shuffled_playlist.insert(0, self.currplaying)
            return self.shuffle_mode

        def Get_Current_Playlist(self):
            """
            根据当前模式返回相应的播放列表
            """
            if self.shuffle_mode:
                return self.shuffled_playlist
            else:
                return self.playlist

        def Next_Music_List(self):
            """
            获取以下一首音乐为开头的list
            """
            musicqueue = []
            currplaying = self.Get_CurrPlaying()
            current_playlist = self.Get_Current_Playlist()
            
            if currplaying and currplaying in current_playlist:
                pos = current_playlist.index(currplaying) + 1 
            else:
                pos = 0
                
            length = len(current_playlist)
            if pos >= length:
                pos = 0

            newlist1 = current_playlist[pos:length]
            newlist2 = current_playlist[0:pos]
            musicqueue = newlist1 + newlist2
            return musicqueue

        def Prev_Music_List(self):
            """
            获取以上一首音乐为开头的list
            """
            musicqueue = []
            currplaying = self.Get_CurrPlaying()
            current_playlist = self.Get_Current_Playlist()
            
            if currplaying and currplaying in current_playlist:
                pos = current_playlist.index(currplaying) - 1
            else:
                pos = len(current_playlist) - 1
                
            length = len(current_playlist)
            if pos < 0:
                pos = length - 1

            newlist1 = current_playlist[pos:length]
            newlist2 = current_playlist[0:pos]
            musicqueue = newlist1 + newlist2
            return musicqueue

        def Now_Music_List(self, song):
            """
            获取以指定音乐为开头的list
            """
            musicqueue = []
            current_playlist = self.Get_Current_Playlist()
            
            if song in current_playlist:
                pos = current_playlist.index(song)
            else:
                pos = 0
                
            length = len(current_playlist)
            if pos >= length:
                pos = 0

            newlist1 = current_playlist[pos:length]
            newlist2 = current_playlist[0:pos]
            musicqueue = newlist1 + newlist2
            return musicqueue
        
        def Prev_Music(self):
            """
            播放上一首音乐
            """
            if not self.loopmode:
                current_playlist = self.Get_Current_Playlist()
                if current_playlist:
                    self.Play_Music_Now(current_playlist[0])
                    self.loopmode = True
                    return current_playlist[0]
                return ""
            else:
                mlist = self.Prev_Music_List()
                prev_song = mlist[0] if mlist else ""
                if prev_song:
                    self.Music_Play_List(song=mlist)
                    self.currplaying = prev_song
                return prev_song
        
        def Next_Music(self):
            """
            播放下一首音乐
            """
            if not self.loopmode:
                current_playlist = self.Get_Current_Playlist()
                if current_playlist:
                    self.Play_Music_Now(current_playlist[0])
                    self.loopmode = True
                    return current_playlist[0]
                return ""
            else:
                mlist = self.Next_Music_List()
                next_song = mlist[0] if mlist else ""
                if next_song:
                    self.Music_Play_List(song=mlist)
                    self.currplaying = next_song
                return next_song

        def Play_Music_Now(self, song):
            """
            立刻播放指定音乐
            """
            self.loopmode = True
            mlist = self.Now_Music_List(song)
            self.Music_Play_List(song=mlist)
            self.currplaying = song
            return song

        def Get_ShortName(self):
            """
            返回短名称音乐列表
            """
            if not renpy.android:
                dirs = os.listdir(renpy.config.basedir+ "/custom_bgm/")
            else:
                dirs = os.listdir("/storage/emulated/0/MAS/custom_bgm/")
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
            if not renpy.android:
                dirs = os.listdir(renpy.config.basedir+ "/custom_bgm/")
            else:
                dirs = os.listdir("/storage/emulated/0/MAS/custom_bgm/")
            catched = []
            file_type = ["mp3", "wav", "ogg"]
            for file_name in dirs:
                playable = False
                for type in file_type:
                    if file_name.find(type) != 1:
                        playable = True
                        break
                if playable == True:
                    if not renpy.android:
                        catched.append((renpy.config.basedir + "/custom_bgm/" + file_name).replace("\\","/"))
                    else:
                        catched.append(file_name)
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
    
    # 启动时自动播放
    def auto_resume_music():
        if persistent._loop_play_shuffle_mode:
            # 随机播放模式：从随机列表中选择第一首
            lp_queue.Play_Music_Now(lp_queue.shuffled_playlist[0])
        else:
            # 顺序播放模式：从原始列表中选择第一首
            lp_queue.Play_Music_Now(lp_queue.playlist[0])
    
    # 注册启动时的回调
    config.start_callbacks.append(auto_resume_music)

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
            # 保存当前的随机播放状态
            $ old_shuffle_mode = lp_queue.shuffle_mode
            $ lp_queue = MusicQueue()
            # 恢复随机播放状态
            $ lp_queue.shuffle_mode = old_shuffle_mode
            # 如果随机播放模式开启，重新打乱播放列表
            if lp_queue.shuffle_mode:
                $ lp_queue.shuffled_playlist = lp_queue.playlist[:]
                $ random.shuffle(lp_queue.shuffled_playlist)
            # 重置循环模式状态
            $ lp_queue.loopmode = False
            "已更新"
            jump loop_play
        "上一首":
            $ lp_queue.Prev_Music()
        "下一首":
            $ lp_queue.Next_Music()
        "暂停":
            $ lp_queue.Pause()
        "随机播放: [ '开启' if lp_queue.shuffle_mode else '关闭' ]":
            $ lp_queue.Toggle_Shuffle()
            if lp_queue.shuffle_mode:
                $ lp_queue.Next_Music()
                "已开启随机播放模式"
            else:
                $ lp_queue.Next_Music()
                "已关闭随机播放模式"
        "启动时自动播放: [ '开启' if persistent._loop_play_auto_resume else '关闭' ]":
            $ persistent._loop_play_auto_resume = not persistent._loop_play_auto_resume
            if persistent._loop_play_auto_resume:
                "已开启启动时自动播放音乐"
                jump loop_play
            else:
                "已关闭启动时自动播放音乐"
                jump loop_play
    
    "OK - [lp_queue.currplaying]"
        
return

