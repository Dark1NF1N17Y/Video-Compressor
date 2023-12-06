import os, ffmpeg, time

def compress_video(video_full_path, output_file_name, target_size):
    min_audio_bitrate = 32000
    max_audio_bitrate = 256000
    probe = ffmpeg.probe(video_full_path)
    duration = float(probe['format']['duration'])
    audio_bitrate = float(next((s for s in probe['streams'] if s['codec_type'] == 'audio'), None)['bit_rate'])
    target_total_bitrate = (target_size * 1024 * 8) / (1.073741824 * duration)

    if 10 * audio_bitrate > target_total_bitrate:
        audio_bitrate = target_total_bitrate / 10
        if audio_bitrate < min_audio_bitrate < target_total_bitrate:
            audio_bitrate = min_audio_bitrate
        elif audio_bitrate > max_audio_bitrate:
            audio_bitrate = max_audio_bitrate
    video_bitrate = target_total_bitrate - audio_bitrate

    i = ffmpeg.input(video_full_path)
    ffmpeg.output(i, os.devnull,
                  **{'c:v': 'libx264', 'b:v': video_bitrate, 'pass': 1, 'f': 'mp4'}
                  ).overwrite_output().run()
    ffmpeg.output(i, output_file_name,
                  **{'c:v': 'libx264', 'b:v': video_bitrate, 'pass': 2, 'c:a': 'aac', 'b:a': audio_bitrate}
                  ).overwrite_output().run()

def input_part():
    os.system('cls||clear')
    print("=" * 50)
    input1 = input("Enter Video Name : ")
    if input1.endswith('.mp4'):
        filename = (input1)
    else:
        filename = (input1 + ".mp4")
    if os.path.isfile(filename):
        input2 = input("Enter Output Name : ")
        print("=" * 50)
        if input2.endswith('.mp4'):
            outputname = (input2)
        else:
            outputname = (input2 + ".mp4")
        compress_video(filename, outputname, 50 * 1000)
    else:
        os.system('cls||clear')
        print("=" * 50)
        print("Video Not Found! Try Again _/(^ ^)\_")
        print("=" * 50)
        time.sleep(0.7)
        os.system('cls||clear')
        input_part()

input_part()
