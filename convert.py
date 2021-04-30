import os
import subprocess
import csv
from colorama import init
from datetime import datetime

fileToSearch = (".avi", ".mp4", ".mkv", ".wmv", "mpeg", "m4v", "mov","ts")
sourceDir = "D:\\_TORRENT\\A_CONVERTIR"
destDir = "D:\\_TORRENT\\VIDEOS\\"
dir_to_create = ""
totalFileSizeBefore = 0
totalFileSizeAfter = 0
totalFile = 0
totalFileIgnore = 0


def set_csv_file_name():
    datetimeofday = datetime.now()
    return "report_" + datetimeofday.strftime("%d_%m_%Y_%H_%M_%S")+".csv"


def getdestdir(src):
    startdir = sourceDir.split("\\")
    long = len(startdir)
    cutdir = src.split("\\")
    return destDir + "\\".join(cutdir[long:])


def showdestdir(src):
    startdir = destDir.split("\\")
    long = len(startdir)
    cutdir = src.split("\\")
    return "\\".join(cutdir[long-1:])


def makefulldir(src):
    if not os.path.exists(src):
        os.makedirs(src)


def showduration(src):
    command_line = f'U:\\Users\\benoit\\Tools\\ffprobe -i "{src}" -show_entries format=duration -v quiet -of csv="p=0" -sexagesimal'
    metadata = subprocess.check_output(command_line)
    duration_time = metadata.decode("utf-8")[0:-2]
    return duration_time


def getfilesize(src):
    file_stats = os.stat(src)
    return file_stats.st_size / (1024 * 1024)


def taille_avant(value):
    print("Taille avant : \033[32m {0:8.2f} MB".format(value))


def taille_apres(value):
    print("Taille aprés : \033[32m {0:8.2f} MB".format(value))


def showpourcent(before, after):
    if before > 0:
        pourcentage = 100 - ((after / before) * 100)
        if pourcentage > 0:
            print("Pourcentage réduction : \033[32m{0:3.2f}%".format(pourcentage))
        else:
            print("Pourcentage réduction : \033[31m{0:3.2f}%".format(pourcentage))
        return pourcentage


def showfiles(totalfiles, totalfilesignore):
    print("Nombre de fichiers traités : \033[32m{}".format(totalfiles))
    if totalfilesignore > 0:
        print("Nombre de fichiers ignorés : \033[31m{}".format(totalfilesignore))


def format_datetime(str_datetime):
    return str_datetime.strftime("%d/%m/%Y %H:%M:%S")


init(autoreset=True)
csvReportName = set_csv_file_name()
heure_debut = datetime.now()

for root, dirs, files in os.walk(sourceDir):
    for file in files:
        if file.endswith(fileToSearch):
            fullDestDir = getdestdir(root)

            if dir_to_create != fullDestDir:
                makefulldir(fullDestDir)
                dir_to_create = fullDestDir

            fullSourceFile = os.path.join(root, file)
            fullfilename = os.path.splitext(file)
            fullDestinationFile = fullDestDir.strip() + "\\" + fullfilename[0].strip() + ".mp4"
            showfile = showdestdir(fullDestinationFile)
            sizeFileBefore = getfilesize(fullSourceFile)
            totalFileSizeBefore = totalFileSizeBefore + sizeFileBefore
            duration = showduration(fullSourceFile)
            start = datetime.now()
            print("Heure début : \033[33m{}".format(format_datetime(start)))
            command = 'ffmpeg -i "{}" -v quiet -stats -vcodec libx264 -acodec aac "{}"'
            print("\033[33m{} \033[39m ".format(showfile))
            print("Durée : \033[32m {}".format(duration))
            taille_avant(sizeFileBefore)

            if not os.path.exists(fullDestinationFile):
                os.system(command.format(fullSourceFile, fullDestinationFile))
                totalFile += 1
            else:
                totalFileIgnore += 1
                print("\033[31mFichier déjà existant".format(showfile))

            sizeFileAfter = getfilesize(fullDestinationFile)
            totalFileSizeAfter = totalFileSizeAfter + sizeFileAfter
            taille_apres(sizeFileAfter)

            end = datetime.now()

            pourcent = showpourcent(sizeFileBefore, sizeFileAfter)

            with open(csvReportName, 'a', newline='') as filecsv:
                writer = csv.writer(filecsv, delimiter=';')
                writer.writerow([fullDestDir, file, duration, format_datetime(start), format_datetime(end), sizeFileBefore, sizeFileAfter, pourcent])

            print("Heure fin : \033[33m{}".format(format_datetime(end)))
            print("="*150)

print('*'*150)
heure_fin = datetime.now()
print("Fin de la conversion :")
print("Heure de début de la conversion : \033[33m{}".format(format_datetime(heure_debut)))
print("Heure de fin de la conversion   : \033[33m{}".format(format_datetime(heure_fin)))
taille_avant(totalFileSizeBefore)
taille_apres(totalFileSizeAfter)
pourcent = showpourcent(totalFileSizeBefore, totalFileSizeAfter)
showfiles(totalFile, totalFileIgnore)
print('*'*150)
