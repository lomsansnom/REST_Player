#!/usr/bin/python
# -*- coding: utf-8 -*-

import cherrypy
from cherrypy import expose
import json
import os
import mimetypes

class restPlayer:
    
    __contentType = "application/json;charset=utf-8"

    def __init__(self):
        cherrypy.response.headers['Content-Type'] = self.__contentType
        
    @expose
    def getListeMusiques(self):
        try:
            params = json.loads(cherrypy.request.body.readline())
        except Exception as e:
            ret = {"OK" : False}
            ret['Erreur'] = "Paramètres invalides"
            cherrypy.log(str(e))
            return json.dumps(ret)
        
        if "chemin" in params:
            cherrypy.log(params["chemin"])
            mainDir = os.listdir(params["chemin"])
            cherrypy.log(str(mainDir))
            subDir = []
            subSubDir =[]            
            
            for i in range(0,len(mainDir)):
                chemin = params["chemin"] + '/' + mainDir[i]
                if os.path.isdir(chemin):
                    subDir.insert(i, os.listdir(chemin))
                elif chemin[len(chemin)-4:] != ".mp3":
                        mainDir[j][jj] = ""
                        
                if not os.path.isdir(chemin):
                    subDir.insert(i, "")
            
            
            for j in range(0,len(mainDir)):
                subSubDir.insert(j,[])
                for jj in range(0,len(subDir[j])):
                    chemin = params["chemin"] + '/' + mainDir[j] + '/' + subDir[j][jj]
                    if os.path.isdir(chemin):
                        subSubDir[j].insert(jj, os.listdir(chemin))
                    elif chemin[len(chemin)-4:] != ".mp3":
                        subDir[j][jj] = ""
                    
                    if not os.path.isdir(chemin):
                        subSubDir[j].insert(jj, "")
                        
            for k in range(0,len(mainDir)):
                for kk in range(0,len(subDir[k])):
                    for kkk in range(0,len(subSubDir[k][kk])):
                        chemin = params["chemin"] + '/' + mainDir[k] + '/' + subDir[k][kk] + '/' + subSubDir[k][kk][kkk]
                        if subSubDir[k][kk][kkk][len(subSubDir[k][kk][kkk])-4:] != ".mp3":
                            subSubDir[k][kk][kkk] = ""
            
            ret = {"OK" : True, "parent" : mainDir, "sousDossier" : subDir, "sousSousDossier" : subSubDir}
        else:
            ret = {"OK" : False}
            ret["Erreur"] = "chemin est obligatoire"
        
        return json.dumps(ret)
    
    @expose
    def getMusique(self):
        try:
            params = json.loads(cherrypy.request.body.readline())
        except Exception as e:
            ret = {"OK" : False}
            ret['Erreur'] = "Paramètres invalides"
            cherrypy.log(str(e))
            return json.dumps(ret)
        
        if "musique" in params:
            if params["musique"] == None:
                return "no file specified!"
            if not os.path.exists(params["musique"]):
                return "file not found!"
            f = open(params["musique"], 'rb')
            size = os.path.getsize(params["musique"])
            mime = mimetypes.guess_type(params["musique"])[0]
            cherrypy.log(mime)
            cherrypy.response.headers["Content-Type"] = mime
            cherrypy.response.headers["Content-Disposition"] = 'attachment; filename="%s"' % os.path.basename(params["musique"])
            cherrypy.response.headers["Content-Length"] = size
        
            BUF_SIZE = 1024 * 5
    
            def stream():
                data = f.read(BUF_SIZE)
                while len(data) > 0:
                    yield data
                    data = f.read(BUF_SIZE)
    
            stream()
        return json.dumps({"ok":True})
    getMusique._cp_config = {'response.stream': True}

        
conf={  
        'global':{
                  'server.socket_host' : '0.0.0.0',
                  'server.socket_port' : 9090,
                  'log.screen' : True
        },
        '/' : {
               'tools.encode.on':True,
               'tools.encode.encoding':'utf-8'
        }
}


cherrypy.config.update(conf)
cherrypy.quickstart(restPlayer(),"/", conf)
