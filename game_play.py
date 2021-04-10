'''
主要流程：
1、首先加载视频，摄像头视频，同时开启人体关键点检测；
2、加载音乐和对应的beat信息，两者一定要对应；

音乐和视频要在一个统一的平台上展示，这个有暂时有一个方案是用pygame，pygame可以在界面上放置控件
'''
import time
import cv2
import os
import pygame
import wave
import time

from pose.openpose.openpose_play import pose_estimate, pose_init, pose_track

class VideoReader(object):
    def __init__(self, file_name):
        self.file_name = file_name
        try:  # OpenCV needs int to read from webcam
            self.file_name = int(file_name)
        except ValueError:
            pass

    def __iter__(self):
        self.cap = cv2.VideoCapture(self.file_name)
        if not self.cap.isOpened():
            raise IOError('Video {} cannot be opened'.format(self.file_name))
        return self

    def __next__(self):
        was_read, img = self.cap.read()
        if not was_read:
            raise StopIteration
        return img

class FDGame(object):
	def __init__(self, beat_file, music_file, camera_id):
		self.beat_file = beat_file
		self.music_file = music_file
		self.camera_id = camera_id
	
	def play(self):
		#==================== music ==================
		# read beat file
		beat_file = open(self.beat_file, "r")
		beat_nums = []
		for line in beat_file:
			beat_nums.append(float(line))

		# play music
		fhandle = wave.open(self.music_file, "rb")
		params = fhandle.getparams()
		nchannels, sampwidth, framerate, nframes = params[:4]
		fhandle.close()

		frame_provider = VideoReader(self.camera_id)

		pygame.mixer.init(framerate)
		pygame.mixer.music.load(self.music_file)

		net = pose_init()

		#==================== open camera ==================
		previous_poses = []
		for frame in frame_provider:
			current_results = pose_estimate(frame, net)
			current_results = pose_track(previous_poses, current_results)
			cv2.imshow('FSDGame',frame)
			# wait space to start game
			if cv2.waitKey(1) & 0xff == 32:
				break

		time_start = time.time()

		count_beat   = 1
		count_iter   = 0
		ponit_cord   = [(10,100)]
		point_size   = 6
		point_color  = (0, 0, 255)
		# For show beat position
		beat_point_x = 0
		beat_point_y = 0
		# For print text
		beat_text    = ""
		beat_color   = ()
		thickness    = 8

		for frame in frame_provider:				
			# track pose and genetate action position
			current_results = pose_estimate(frame, net)
			current_results = pose_track(previous_poses, current_results)
			previous_poses  = current_results
			if len(current_results) == 0:
				frame = cv2.flip(frame, 1)
				cv2.waitKey(1)
				cv2.imshow('FDGame',frame)
				continue
			# for pose in current_results:
			# 	print("dram pose points {}".format(pose))
			# 	# pose.draw(frame)
			# 	[beat_point_x, beat_point_y], beat_text, beat_color = pose.get_beat_point()
			if count_iter == 0:
				time_start=time.time()
				pygame.mixer.music.play()
			count_iter += 1

			## write text
			# font = cv2.FONT_HERSHEY_SIMPLEX
			# cv2.putText(frame,'Beat',ponit_cord, cv2.FONT_HERSHEY_SIMPLEX, 2,( 0,255,0),2,cv2.LINE_AA)
			
			frame = cv2.flip(frame, 1)
			time_end=time.time()
			if time_end - time_start > beat_nums[count_beat] - 0.5:
				for pose in current_results:
					[beat_point_x, beat_point_y], beat_text, beat_color = pose.get_beat_point(count_beat)
				
				## circal a point
				# cv2.circle(frame, (beat_point_x + (-1)**count_beat*move_dis, beat_point_y), point_size, point_color, thickness)
				count_beat += 1
				print('beat !!')

			cv2.putText(frame, beat_text, (beat_point_x , beat_point_y), \
										cv2.FONT_HERSHEY_SIMPLEX, 0.8, beat_color, 2, cv2.LINE_AA)
			
			cv2.waitKey(1)
			cv2.imshow('FDGame',frame)
	
if __name__ == '__main__':
	parser = argparse.ArgumentParser()
	parser.add_argument("--beat-file", type=str, required=True,
                        help='path to the beat file')
	parser.add_argument("--music-file", type=str, required=True,
                        help='path to the music file')
	parser.add_argument("--camera-id", type=int, default=0,
                        help='camera id')
	args = parser.parse_args()

	game = FDGame(args.beat_file, args.music_file, args.camera_id)
	game.play()
