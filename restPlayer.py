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
            ret = os.listdir(params["chemin"])
            cherrypy.log(str(ret))
            
            j = 0
            for i in ret:
                ret[int(i)][j] = os.listdir(params["chemin"])
                j += 1
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
