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
            
            for i in range(0,len(mainDir)):
                subDir.insert(i, os.listdir(params["chemin"] + '/' + mainDir[i]))
            cherrypy.log(str(subDir))
            
            for i in range(0,len(subDir)):
                subSubDir.insert(i, os.listdir(params["chemin"] + '/' + subDir[i]))
            cherrypy.log(str(subSubDir))
            
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
