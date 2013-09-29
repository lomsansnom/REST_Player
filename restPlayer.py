#!/usr/bin/python
# -*- coding: utf-8 -*-

import cherrypy
from cherrypy import expose
import json
import os

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
            
            for i in range(0,len(mainDir)-1):
                chemin = params["chemin"] + '/' + mainDir[i]
                if os.path.isdir(chemin):
                    subDir.insert(i, os.listdir(chemin))
                elif chemin[len(chemin)-4:] != ".mp3":
                        mainDir[j][jj] = ""
            
            
            for j in range(0,len(mainDir)-1):
                subSubDir.insert(j,[])
                for jj in range(0,len(subDir[j])-1):
                    chemin = params["chemin"] + '/' + mainDir[j] + '/' + subDir[j][jj]
                    if os.path.isdir(chemin):
                        subSubDir[j].insert(jj, os.listdir(chemin))
                    elif chemin[len(chemin)-4:] != ".mp3":
                        subDir[j][jj] = ""

            for k in range(0,len(mainDir)-1):
                for kk in range(0,len(subDir[k])-1):
                    for kkk in range(0,len(subSubDir[k][kk])-1):
                        chemin = params["chemin"] + '/' + mainDir[k] + '/' + subDir[k][kk] + '/' + subSubDir[k][kk][kkk]
                        if chemin[len(chemin)-4:] != ".mp3":
                            subSubDir[k][kk][kkk] = ""
            
            ret = {"OK" : True, "parent" : mainDir, "sousDossier" : subDir, "sousSousDossier" : subSubDir}
        else:
            ret = {"OK" : False}
            ret["Erreur"] = "chemin est obligatoire"
        
        return json.dumps(ret)
        
conf={  
        'global':{
                  'server.socket_host' : '0.0.0.0',
                  'server.socket_port' : 8282,
                  'log.screen' : True
        },
        '/' : {
               'tools.encode.on':True,
               'tools.encode.encoding':'utf-8'
        }
}


cherrypy.config.update(conf)
cherrypy.quickstart(restPlayer(),"/", conf)
