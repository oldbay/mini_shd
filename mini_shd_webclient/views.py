# -*- coding: UTF-8 -*-

import StringIO
from flask import (
    render_template,
    send_file,
    request,
    redirect,
    session,
    flash
)
from forms import AuthForm, RegForm, MyfilesForm, MyfilesList
from mini_shd_webclient import app
from mini_shd_server.cmd_interface import User
from werkzeug.utils import secure_filename

@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
def index():
    form = AuthForm()
    session['user'] = False
    if form.button.data:
        user = User(form.login.data, form.passwd.data)
        if user.auth():
            session['user'] = {
                'login': user.name,
                'passwd': user.passwd,
            }
            flash(u'Вход выполнен')
            return redirect('/myfiles')
        else:
            session['user'] = False
            flash(u'Пароль или логин неверен')
    return render_template('index.html', form=form)


@app.route('/reg', methods=['GET', 'POST'])
def reg():
    form = RegForm()
    if session['user']:
        regmenu = False
    else:
        regmenu = True
    if form.button.data:
        if form.passwd.data != form.passwd_verifi.data:
            flash(u'Пароли не совпадают')
        else:
            if regmenu:
                # user reg
                reguser = User(form.genlogin.data, form.passwd.data)
                if reguser.useradd():
                    flash(u'Пользователь создан')
                    return redirect('/')
                else:
                    flash(u'Пользователь не создан')
            else:
                # modify passwd
                reguser = User(
                    session['user']['login'],
                    session['user']['passwd']
                )
                if reguser.usermod(form.passwd.data):
                    session['user'] = {
                        'login': reguser.name,
                        'passwd': reguser.passwd,
                    }
                    flash(u'Пароль пользователя изменён')
                    return redirect('/myfiles')
                else:
                    flash(u'Пароль пользователя не изменён')

    if form.rbutton.data:
        # user del
        reguser = User(
            session['user']['login'],
            session['user']['passwd']
        )
        if reguser.userdel():
            flash(u'Пользователь %s удалён'%session['user']['login'])
            return redirect('/')
        else:
            flash(u'Пользователь %s не удалён'%session['user']['login'])

    return render_template('reg.html', form=form, regmenu=regmenu)


@app.route('/myfiles', methods=['GET', 'POST'])
def myfiles():
    fileslist = MyfilesList()
    outfileslist = []
    if session['user']:
        menu = True
        key_download = True
        fuser = User(
            session['user']['login'],
            session['user']['passwd']
        )

        # create table
        if fileslist.fileslist.last_index == -1:
            outfileslist = fuser.list_file()
            for _outfile in outfileslist:
                _form = MyfilesForm()
                _form.fname = _outfile
                fileslist.fileslist.append_entry(_form)

        # file operations
        upload = [my for my in fileslist.fileslist if my.down.data == True]
        remove = [my for my in fileslist.fileslist if my.delit.data == True]

        # upload file
        if len(upload) == 1 and len(remove) == 0:
            key_download = False
            _filename = upload[0].fname.data
            _obj = fuser.get_file(_filename)
            strIO = StringIO.StringIO()
            strIO.write(_obj)
            strIO.seek(0)
            return send_file(strIO,
                             attachment_filename=_filename,
                             as_attachment=True)

        # remove faile
        if len(upload) == 0 and len(remove) == 1:
            key_download = False
            _filename = remove[0].fname.data
            if fuser.del_file(_filename):
                outfileslist = fuser.list_file()
                flash(u"Файл %s удалён"%_filename)
                return redirect('/myfiles')
            else:
                flash(u"Файл %s не удалён"%_filename)

        # download file
        if request.method == 'POST' and key_download:
            _file = request.files['file']
            filename = secure_filename(_file.filename)
            if fuser.put_file(filename, _file.read()):
                outfileslist = fuser.list_file()
                flash(u"Файл %s сохранён"%filename)
                return redirect('/myfiles')
            else:
                flash(u"Файл %s не сохранён"%filename)
            _file.close()
    else:
        menu = False
    return render_template(
        'myfiles.html',
        fileslist=fileslist,
        menu=menu,
    )
