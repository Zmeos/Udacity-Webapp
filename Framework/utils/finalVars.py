'''
Created on 1. juli 2012

@author: Joakim
'''

class finalVars:
    ### Memcache keys:
    mc_blogkey = 'blogfront'
    
    
    ### hmac secret
    hmacSECRET = 'yolololoMehehe'
    
    ### hidden inputs to avoid CSRF attacks ##nvm these need to be randomly generated
    newpostHiddenInput = 'This webapp stuff is awesome!'
    signupHiddenInput = 'flutefluteTuba!'
