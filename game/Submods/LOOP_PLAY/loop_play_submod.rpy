init -990 python:
    store.mas_submod_utils.Submod(
        author="P and heart",
        name="Loop Play",
        description="允许你循环/随机播放MAS内的音乐",
        version='0.5.0'
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

default persistent.music_start_sloopplay = False
default persistent.music_start_random = False

init python:

    from mutagen.mp3 import MP3
    from mutagen.oggvorbis import OggVorbis
    #from mutagen.wave import WAVE
    import threading
    import os
    import random
   
    class MusicQueue(object):
        playlist = []
        paused = False
        loopmode = False
        currplaying = ""
        current_mode = "sequential"  # 新增播放模式标识："sequential"或"random"
        current_playlist = []        # 当前生效的播放列表
        current_random_list = []     # 随机播放时生成的列表
        """docstring for ClassName"""
        def __init__(self):
            self.playlist = self.Music_GetCatchSaveList()
            self.current_index = 0
            self.current_index = 0
            self.current_playlist = list(self.playlist)  # 初始化当前播放列表
            self.current_mode = "sequential"
            self.stop_playing = False  # 新增停止标志
            self.panding = False

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
            """根据当前模式获取下一首列表"""
            if self.current_mode == "random":
                 return self._get_next_random_list()
            return self._get_next_sequential_list()
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
            """根据当前模式获取上一首列表"""
            if self.current_mode == "random":
                return self._get_prev_random_list()
            return self._get_prev_sequential_list()
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
            self.panding = False
            if not renpy.android:
                if not self.loopmode:
                     self.Play_Music_Now(self.playlist[0])
                     self.loopmode=True
                else:
                     mlist = self.Prev_Music_List()
                     self.Music_Play_List(song=mlist)
                     return self.Get_CurrPlaying()
                     
                     
            else:
                if not self.loopmode:
                     self.Play_Music_Now(self.playlist[0])
                     self.loopmode=True
                else:
                     mlist = self.Prev_Music_List()
                     self.play_songs(song=mlist)
                     self.currplaying = mlist[0]
                     return self.currplaying
                     #return self.Get_CurrPlaying()
        
        def Next_Music(self):
            """
            播放下一首音乐
            """
            self.panding = False
            if not renpy.android:
                if not self.loopmode:
                      self.Play_Music_Now(self.playlist[0])
                      self.loopmode=True
                else:
                      mlist = self.Next_Music_List()
                      self.Music_Play_List(song=mlist)
                      return self.Get_CurrPlaying()
                      
            else:
                if not self.loopmode:
                      self.Play_Music_Now(self.playlist[0])
                      self.loopmode=True
                else:
                      mlist = self.Next_Music_List()
                      self.play_songs(song=mlist)
                      self.currplaying = mlist[0]
                      return self.currplaying
                      #return self.Get_CurrPlaying()
                      
        def Next_Music2(self):
            """
            循环自启动开关
            """
            
            self.panding = True
            self.Play_Music_Now(self.playlist[0])
                      
                

        def Play_Music_Now(self, song):
            """
            立刻播放指定音乐
            """
            """根据当前模式处理立即播放"""
            if self.current_mode == "random":
                # 在随机列表中重新定位
                try:
                    new_index = self.current_random_list.index(song)
                    self.current_playlist = self.current_random_list[new_index:] + self.current_random_list[:new_index]
                except ValueError:
                    pass
            if not renpy.android:
                  self.loopmode=True
                  mlist = self.Now_Music_List(song)
                  self.Music_Play_List(song=mlist)
                  return self.Get_CurrPlaying()
            else:
                  self.loopmode=True
                  mlist = self.Now_Music_List(song)
                  self.play_songs(song=mlist)
                  self.currplaying = mlist[0]
                  return self.currplaying
                  #return self.Get_CurrPlaying()   
                  
        def Stop(self):
            """停止播放并终止循环"""
            self.stop_playing = True
            renpy.music.stop(channel='music')
            self.current_music_index = 0  # 重置索引       
                  
##########################随机音乐列表####################                  
                  
        def Random_Music_List(self):
           """
           生成随机顺序的播放列表
           """
           shuffled = list(self.playlist)
           random.shuffle(shuffled)
           return shuffled
           
        def _get_next_sequential_list(self):
            pos = self.current_playlist.index(self.currplaying) + 1
            return self._generate_rotated_list(pos)

        def _get_next_random_list(self):
            try:
                pos = self.current_random_list.index(self.currplaying) + 1
            except ValueError:
                pos = 0
            return self._generate_rotated_list(pos, self.current_random_list)
            
        def _get_prev_sequential_list(self):
            pos = self.current_playlist.index(self.currplaying)
            return self._generate_rotated_list(pos, reverse=True)

        def _get_prev_random_list(self):
            try:
                pos = self.current_random_list.index(self.currplaying)
            except ValueError:
                pos = 0
            return self._generate_rotated_list(pos-1, self.current_random_list, reverse=True)
  
        def _generate_rotated_list(self, pos, base_list=None, reverse=False):
            """通用列表旋转方法"""
            base = base_list or self.current_playlist
            length = len(base)
            pos = max(0, min(pos, length))
        
            if reverse:
                newlist1 = base[pos::-1]
                newlist2 = base[:pos:-1]
            else:
                newlist1 = base[pos:]
                newlist2 = base[:pos]
            return newlist1 + newlist2  
         
        def Random_Music(self):
            """开始随机播放"""
            self.current_mode = "random"
            self.current_random_list = self.Random_Music_List()
            self.current_playlist = self.current_random_list  # 切换当前播放列表
        
            if not renpy.android:
                self.Music_Play_List(song=self.current_playlist)
            else:
                self.play_songs(song=self.current_playlist)
            return self.Get_CurrPlaying()
            
        def Random_Music2(self):
            """自启动随机播放"""
            self.current_mode = "random"
            self.current_random_list = self.Random_Music_List()
            self.current_playlist = self.current_random_list  # 切换当前播放列表
        
            self.panding = True
            self.play_songs(song=self.current_playlist)
            return self.Get_CurrPlaying()




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
                          catched.append(("/storage/emulated/0/MAS/custom_bgm/" + file_name).replace("\\","/"))
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
                
        def play_songs(self, song):
            # 当前播放的音乐索引
            self.current_music_index = 0
            self.current_playlist = song.copy()

            
            
            # 启动线程播放音乐
            #self.play_next_song()
            if not self.panding:
                     renpy.invoke_in_thread(self.play_next_song)
            else:
                     renpy.invoke_in_thread(self.play_next_song2)
        def play_next_song(self):
                
                self.stop_playing = False  # 重置停止标志
                # 播放列表中的音乐
                while self.current_music_index < len(self.current_playlist):
                       # 获取当前音乐文件路径
                       current_music = self.current_playlist[self.current_music_index]
                       self.currplaying = current_music  # 立即更新当前播放歌曲
                       #提取歌曲名
                       from os.path import basename, splitext
                       song_name = splitext(basename(current_music))[0]  # 获取不带扩展名的文件名

                       # 播放音乐（使用当前音乐路径）
                       play_song(current_music, loop=False, fadein=1.2, fadeout=1.2)
                       if current_music.lower().endswith(".mp3"):
                          audio = MP3(current_music)
                       elif current_music.lower().endswith(".ogg"):
                          audio = OggVorbis(current_music)
                       # 如需支持.wav，取消注释以下代码
                       # elif current_song.lower().endswith(".wav"):
                       #     audio = WAVE(current_song_path)
                       else:
                           renpy.notify("获取失败")

                       # 等待音乐播放完毕
                       song_duration = audio.info.length 
                      
                       if song_duration is None:
                           song_duration = 0.1  # 避免无限等待
                        
                       renpy.notify("{}".format(song_name))  # 显示歌曲名
                       time.sleep(song_duration + 1)   
                       if self.stop_playing:
                           break
                       #检测音乐是否播放完毕
                       while renpy.music.is_playing():
                             #i = 1
                             #b += i
                             #renpy.notify("进入循环 {} ".format(b))
                             time.sleep(0.5 + 0.5)
                             

                       # 停止当前音乐
                       renpy.music.stop(fadeout=3.0, channel='music')

                       self.current_music_index += 1

                # 播放列表结束提示
                renpy.notify("音乐播放列表播放完毕")
                
        #自启动调用                    
        def play_next_song2(self):
                
                self.stop_playing = False  # 重置停止标志
                # 播放列表中的音乐
                if self.current_music_index < len(self.current_playlist):
                       # 获取当前音乐文件路径
                       current_music = self.current_playlist[self.current_music_index]
                       self.currplaying = current_music  # 立即更新当前播放歌曲
                       #提取歌曲名
                       from os.path import basename, splitext
                       song_name = splitext(basename(current_music))[0]  # 获取不带扩展名的文件名

                       # 播放音乐（使用当前音乐路径）
                       play_song(current_music, loop=False, fadein=1.2, fadeout=1.2)
                       if current_music.lower().endswith(".mp3"):
                          audio = MP3(current_music)
                       elif current_music.lower().endswith(".ogg"):
                          audio = OggVorbis(current_music)
                       # 如需支持.wav，取消注释以下代码
                       # elif current_song.lower().endswith(".wav"):
                       #     audio = WAVE(current_song_path)
                       else:
                           renpy.notify("获取失败")

                       # 等待音乐播放完毕
                       song_duration = audio.info.length 
                      
                       if song_duration is None:
                           song_duration = 0.1  # 避免无限等待
                        
                       renpy.notify("{}".format(song_name))  # 显示歌曲名
                       time.sleep(song_duration + 1)   
                       if self.stop_playing:
                           return                            
                       # 停止当前音乐
                       renpy.music.stop(fadeout=3.0, channel='music')

                       self.current_music_index += 1
                       self.play_next_song2()
                            
                        
                
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
            "更新完成"
            jump loop_play
        "随机列表播放":  # 新增选项
            $ lp_queue.Random_Music()
            "随机播放已启动 - [lp_queue.currplaying]"
            jump loop_play
        "上一首":
            $ lp_queue.Prev_Music()
            "OK - [lp_queue.currplaying]"
            jump loop_play
        "下一首":
            $ lp_queue.Next_Music()
            "OK - [lp_queue.currplaying]"
            jump loop_play
        "确认":
              return                 
        
        "暂停/继续":
            $ lp_queue.Pause()
            "已暂停/继续"
            jump loop_play
        "停止播放":
            $ lp_queue.Stop()
            "已停止"
            jump loop_play
        "自启动设置":
#            default persistent.music_autoplay = False
            jump autos
    
    #"OK - [lp_queue.currplaying]"
        
return                                                     

label autos:
      "是否在启动时开启随机播放"
      menu:
            "默认列表：[persistent.music_start_sloopplay] \n 随机列表：[persistent.music_start_random]"
            "默认列表启用" if True:
                    $ persistent.music_start_sloopplay = True
                    $ persistent.music_start_random = False
            "随机列表启用" if True:
                    $ persistent.music_start_sloopplay = False
                    $ persistent.music_start_random = True
            "禁用" if True:
                    $ persistent.music_start_sloopplay = False
                    $ persistent.music_start_random = False
      "好的"
      jump loop_play

#自启动设置
init 950 python:

    
        
      
        
      def music_autoplay():  
        import os
        if store.persistent.music_start_sloopplay:
            try:
                if not renpy.android:
                     lp_queue.Next_Music()
                else:
                     lp_queue.Next_Music2()
            except Exception as e:
                store.mas_submod_utils.submod_log.error("播放缓存失败：{}".format(e))
            
        elif store.persistent.music_start_random:
            try:
                if not renpy.android:
                      lp_queue.Random_Music()
                else:
                      lp_queue.Random_Music2()
            except Exception as e:
                store.mas_submod_utils.submod_log.error("播放缓存失败：{}".format(e))
            
      store.mas_submod_utils.registerFunction('ch30_preloop', music_autoplay)
      
      
      



      