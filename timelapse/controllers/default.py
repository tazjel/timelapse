# -*- coding: utf-8 -*-
# this file is released under public domain and you can use without limitations

#########################################################################
## This is a sample controller
## - index is the default action of any application
## - user is required for authentication and authorization
## - download is for downloading files uploaded in the db (does streaming)
## - call exposes all registered services (none by default)
#########################################################################


def index():
    if len(request.args): page=int(request.args[0])
    else: page=0

    items_per_page=15
    limitby=(page*items_per_page,(page+1)*items_per_page+1)
    rows=db(db.image.image_type == 'camera').select(orderby=~db.image.upload_date, limitby=limitby)
    return dict(rows=rows,page=page,items_per_page=items_per_page)


def gifs():
    if len(request.args): page=int(request.args[0])
    else: page=0

    items_per_page=15
    limitby=(page*items_per_page,(page+1)*items_per_page+1)
    rows=db(db.image.image_type == 'gif').select(limitby=limitby)
    return dict(rows=rows,page=page,items_per_page=items_per_page)



@request.restful()
def api():
    response.view = 'generic.json'
    def GET(tablename,id):
        if not tablename=='image': raise HTTP(400)
        return dict(image = db.image(id))
    def POST(tablename,**fields):
        if not tablename=='image': raise HTTP(400)
        return db.image.validate_and_insert(**fields)
    return locals()


def user():
    """
    exposes:
    http://..../[app]/default/user/login
    http://..../[app]/default/user/logout
    http://..../[app]/default/user/register
    http://..../[app]/default/user/profile
    http://..../[app]/default/user/retrieve_password
    http://..../[app]/default/user/change_password
    http://..../[app]/default/user/manage_users (requires membership in
    use @auth.requires_login()
        @auth.requires_membership('group name')
        @auth.requires_permission('read','table name',record_id)
    to decorate functions that need access control
    """
    return dict(form=auth())

@cache.action()
def download():
    """
    allows downloading of uploaded files
    http://..../[app]/default/download/[filename]
    """
    return response.download(request, db)


def call():
    """
    exposes services. for example:
    http://..../[app]/default/call/jsonrpc
    decorate with @services.jsonrpc the functions to expose
    supports xml, json, xmlrpc, jsonrpc, amfrpc, rss, csv
    """
    return service()


@auth.requires_signature()
def data():
    """
    http://..../[app]/default/data/tables
    http://..../[app]/default/data/create/[table]
    http://..../[app]/default/data/read/[table]/[id]
    http://..../[app]/default/data/update/[table]/[id]
    http://..../[app]/default/data/delete/[table]/[id]
    http://..../[app]/default/data/select/[table]
    http://..../[app]/default/data/search/[table]
    but URLs must be signed, i.e. linked with
      A('table',_href=URL('data/tables',user_signature=True))
    or with the signed load operator
      LOAD('default','data.load',args='tables',ajax=True,user_signature=True)
    """
    return dict(form=crud())
