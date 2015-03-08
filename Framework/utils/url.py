'''
Created on 6. juli 2012

@author: Joakim
'''

### Remember to update the app.yaml file too!
url = {
       # General
       r'flush':'blog/flush',
       
       #Wiki stuff
       r'wiki':'/wiki',
       r'wikiedit':'/wiki/edit',
       r'wikihistory':'/wiki/history',
       
       
       #blog stuff
       r'blog':'/blog',
       r'newpost':'/blog/newpost',
       
       #User stuff
       r'login':'/user/login',
       r'signup':'/user/signup',
       r'welcome':'/user/welcome',
       r'logout':'/user/logout',
       
       #misc
       r'rot13':'/rot13'
       
       }

#print ''.join([url['rot13'],'/?'])
#print url['rot13']+'/?'
