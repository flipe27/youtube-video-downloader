import PySimpleGUI as sg
from sys import exit
from pytube import YouTube
import urllib.request

def download(path, url, formats):
    if len(path.strip()) != 0 and len(url.strip()) != 0:
        audio = False
        if formats[1]:
            audio = True

        try:
            urllib.request.urlopen(url)
        except Exception as error:
            print(f'Error: {error}')
            return False
        else:
            yt = YouTube(url)
            resolution = yt.streams.get_highest_resolution().resolution
            yt.streams.filter(file_extension='mp4', only_audio=audio, resolution=resolution).first().download(path)

            return True

sg.theme('Black')

layout = [
    [sg.Text('Youtube Video Downloader')],
    [sg.Text('Folder to save: '), sg.InputText(key='path'), sg.FolderBrowse()],
    [sg.Text('Video URL: '), sg.InputText(key='url')],
    [sg.Radio('Video', 'format', default=True, key='video'), sg.Radio('Audio', 'format', key='audio')],
    [sg.Text('', key='success', visible=False)],
    [sg.OK('Submit'), sg.Cancel()]
]

window = sg.Window('Youtube Video Downloader', layout)

while True:
    event, values = window.read()
    if event in (sg.WIN_CLOSED, 'Cancel'):
        break
    if event == 'Submit':
        savePath = values['path']
        linkUrl = values['url']
        dwFormats = [values['video'], values['audio']]
        downloaded = download(savePath, linkUrl, dwFormats)

        if downloaded:
            window['success'].update(f'"{YouTube(linkUrl).title}" has been successfully downloaded!', visible=True)
        else:
            window['success'].update('Something is wrong! :(', visible=True)

window.close()
exit()
