import sys
import os
import subprocess

def main():
    timecode = sys.argv[1]
    files = sys.argv[2:]

    for file_ in files:
        extract_frame_at(file_, timecode)


def extract_frame_at(video_filename, timecode, output_folder, extention="png"):
    if not os.path.exists(output_folder):
        msg = "The output directory {} don't exists anymore !".format(output_folder)
        return msg

    elif os.path.exists(video_filename):
        #folderpath = os.path.dirname(video_filename)
        filename = os.path.basename(video_filename)

        output_filename = timecode.replace(":", ".") + "_" + filename + "." + extention
        output_filepath = os.path.join(output_folder, output_filename)

        # https://stackoverflow.com/questions/27568254/how-to-extract-1-screenshot-for-a-video-with-ffmpeg-at-a-given-time
        cmd = ["ffmpeg", "-loglevel", "panic", "-ss", timecode, "-i", video_filename, "-vframes", "1", "-q:v", "1",
               output_filepath, "-y"]

        print(" ".join(cmd))
        subprocess.call(cmd)

        return output_filepath

    else:
        msg = "The file {} don't exists anymore !".format(video_filename)
        return msg
