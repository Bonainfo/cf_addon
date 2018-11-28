# import xmlrpclib
# import sys

# url			= "http://mohitg:8010/";
# dbname    	= "mobikul";
# username    = "admin";
# pwd    		= "webkul";

# sock_common = xmlrpclib.ServerProxy(url+'xmlrpc/common')
# sock = xmlrpclib.ServerProxy(url+'xmlrpc/object')
# try:
# 	uid = sock_common.login(dbname, username, pwd)
# 	print uid
# except Exception as e:
# 	print "Error in Connection %r"%e
# 	sys.exit()

# def sync_w2m():
# 	wc_ids = sock.execute(dbname, uid, pwd, 'product.public.category', 'search_read', [],['name','image','parent_id'])
# 	mapping = {}
# 	#creating categories without child/parent
# 	for wc in wc_ids:
# 		try:
# 			mc = sock.execute(dbname, uid, pwd, 'mobikul.category', 'create',{'name':wc['name'],'image':wc['image']})
# 			mapping[wc['id']]=mc
# 		except Exception,e:
# 			print "1) Error in WC-ID:%r"%wc['id']
# 			print "Detail:%r"%e
# 	#updating categories with child/parent
# 	for wc in wc_ids:
# 		if wc.get('parent_id'):
# 			try:
# 				sock.execute(dbname, uid, pwd, 'mobikul.category', 'write',mapping.get(wc['id']), {'parent_id':mapping.get(wc['parent_id'][0])})
# 			except Exception,e:
# 				print "2) Error in WC-ID:%r"%wc['parent_id']
# 				print "Detail:%r"%e
# 	#linking products with categories
# 	p_ids = sock.execute(dbname, uid, pwd, 'product.template', 'search_read', [],['public_categ_ids'])
# 	for p in p_ids:
# 		mcids = [mapping.get(a) for a in p['public_categ_ids']]
# 		if mcids:
# 			try:
# 				sock.execute(dbname, uid, pwd, 'product.template', 'write',p['id'],{'mobikul_categ_ids':[[6,0,mcids]]})
# 			except Exception,e:
# 				print "3) Error in P-ID:%r"%p['id']
# 				print "Detail:%r"%e
# 		# break

def getBase64(key,pwd):
	cred = {'login' : key, 'pwd' : pwd}
	encoded_cred = str(cred).encode('base64','strict')
	print encoded_cred
	from base64 import b64decode
	decoded_cred = b64decode(encoded_cred)
	print decoded_cred

if __name__=='__main__':
# 	print "Start"
# 	print sock.execute(dbname, uid, pwd, 'res.users', 'search_read', [('id','=',36)],['name','password','new_password'])
# 	print sock.execute(dbname, uid, pwd, 'res.users', 'write', 36,{'password':'webkul'})
# 	print sock.execute(dbname, uid, pwd, 'res.users', 'search_read', [('id','=',36)],['name','password','new_password'])
# 	# print sync_w2m()
	# getBase64("admin","AuWmGgG1312")
	# getBase64("admin","AuWmGgG1312")
	getBase64("test@testing.com","123")
#
# to_data = {
# 	"to":"False"
# }
#
# if not to_data.get("to",False) and not to_data.get("registration_ids",False):
# 	print True
# else:
# 	print False
#


##########################################################
## xmlrpclib code ###
##########################################################


# import xmlrpclib
# db="client_ticom"
# username="admin"
# password="admin"
# url = 'http://192.168.1.71:8010'
# common = xmlrpclib.ServerProxy('{}/xmlrpc/2/common'.format(url))
# print common.version()
# uid = common.authenticate(db, username, password, {})
# print uid
# models = xmlrpclib.ServerProxy('{}/xmlrpc/2/object'.format(url))
# result = models.execute_kw(db, uid, password,'product.template', 'get_stock_qty',[30])
# print result
# eydsb2dpbic6ICdhbG11c3RhZmFnb0BnbWFpbC5jb20nLCAncHdkJzogJ3Blcm83MDA3J30=
# eydsb2dpbic6ICdpZGVhQGkuY29tJywgJ3B3ZCc6ICcxMjMnfQ==
