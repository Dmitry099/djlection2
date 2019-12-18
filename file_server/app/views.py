import datetime
import os

from django.shortcuts import render
from django.conf import settings
from django.http import HttpResponseNotFound


def create_path():
    settings_path = settings.FILES_PATH
    files = os.listdir(settings_path)
    return files


def create_file_list(files):
    file_info_list = []
    for file in files:
        file_path = 'files/' + file
        stat_info_dict = {}
        stat_info = os.stat(file_path)
        stat_info_dict['name'] = file
        stat_info_dict['ctime'] = datetime.datetime.fromtimestamp(stat_info.st_ctime)
        stat_info_dict['mtime'] = datetime.datetime.fromtimestamp(stat_info.st_mtime)
        file_info_list.append(stat_info_dict)
    return file_info_list


def create_file_context(files, file_name):
    for file in files:
        if file == file_name:
            file_path = 'files/' + file
            stat_info_dict = {'name': file}
            with open(file_path, encoding='utf-8') as readfile:
                content = readfile.read()
                stat_info_dict['file_content'] = content
            return stat_info_dict
    else:
        return False


def file_list(request, date=None):
    template_name = 'index.html'

    files = create_path()
    file_info_list = create_file_list(files)
    files_to_view = []
    if date:
        date = date.date()
        for file in file_info_list:
            file_create_time = file['ctime'].date()
            file_modify_time = file['mtime'].date()
            if file_create_time == date or file_modify_time == date:
                files_to_view.append(file)
    else:
        files_to_view = file_info_list

    context = {
        'files': files_to_view,
        'date': date
    }

    return render(request, template_name, context=context)


def file_content(request, name):
    template_name = 'file_content.html'

    files = create_path()
    stat_info_dict = create_file_context(files, name)

    if stat_info_dict:
        context = {
            'file_name': stat_info_dict['name'],
            'file_content': stat_info_dict['file_content']
        }

        return render(request, template_name, context=context)
    else:
        return HttpResponseNotFound(f'File with name {name} '
                                    'has not been found in our library')
