__author__ = 'yan.cui'

import os
import sys

def get_name_without_ext(name):
    index = name.rfind(".")
    return name[0:index]

def convert_one_video(videoname, frames):
    path = os.path.dirname(os.path.abspath(__file__))
    video_path = path + "/static/original/" + videoname
    name_no_ext = get_name_without_ext(videoname)
    cmd_path = path + "/static/tool/converter"
    files = [video_path, cmd_path]
    for f in files:
        if not os.path.isfile(f):
            raise Exception("%s: invalid file" % f)

    base_path = path + "/static/videos/"
    if not os.path.isdir(base_path):
        raise Exception("%s: invalid dir")
    base_path += name_no_ext + "_"
    modes = ["sketch", "3d", "evil", "cartoon"]
    for mode in modes:
        generate_file = base_path + mode + ".mp4"
        if os.path.isfile(generate_file):
            continue
        cmd_str = " ".join([cmd_path, video_path, generate_file, str(frames), mode])
        os.system(cmd_str)
    return 0

def publish_one_video(videoname):
    path = os.path.dirname(os.path.abspath(__file__))
    name_no_ext = get_name_without_ext(videoname)
    poster_path = path + "/static/posters/" + name_no_ext + ".jpg"
    if not os.path.isfile(poster_path):
        raise Exception("%s: invalid poster" % poster_path)


    os.system(" ".join(["mv", path + "/templates/index.html", path + "/templates/index.html.previous"]))
    previous = open(path + "/templates/index.html.previous", "r")
    index = open(path + "/templates/index.html", "w")
    no_br = 0
    existing_handler = False
    existing_call = False
    for line in previous:
        if line.find("<img") == -1 and line.find(name_no_ext + "_click()") != -1:
            existing_handler = True
            index.write(line)
            continue
        if line.find("</script>") != -1:
            if existing_handler == False:
                index.write("\n")
                index.write("function " + name_no_ext + "_click() {\n")
                index.write("     var video = document.getElementById(\"videoid\")\n")
                index.write("     path = \"/static/videos/" + name_no_ext + "_\"\n")
                index.write("     document.getElementById(\"mp4_src\").src = \"/static/videos/" + name_no_ext + "_3d.mp4\"\n")
                index.write("     document.getElementById(\"ogg_src\").src = \"/static/videos/" + name_no_ext + "_3d.ogg\"\n")
                index.write("     video.load()\n")
                index.write("}\n")
        if line.find("<img") != -1:
            no_br = 0 if line.find("<br>") != -1 else no_br + 1
            if line.find(name_no_ext + "_click()") != -1:
                existing_call = True
                index.write(line)
                continue
        if line.find("</body>") != -1:
            if existing_call == False:
                str = "<img id=\"" + name_no_ext + "\" src=\"/static/posters/" + name_no_ext + ".jpg\" onclick=\"" + name_no_ext + "_click()\" style=\"width:200px;height:280px;\"/>"
                print no_br
                if no_br == 2:
                    str = str + "<br>\n"
                index.write(str + "\n")
        index.write(line)
    previous.close()
    index.close()
    return 0