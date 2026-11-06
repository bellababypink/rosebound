"""Integration tests use an isolated database and an ephemeral local server."""
import importlib.util, os, tempfile, threading, unittest, urllib.request, urllib.error, json, http.cookiejar
os.environ['ROSEBOUND_DATA']=tempfile.mkdtemp(prefix='rosebound-test-')
spec=importlib.util.spec_from_file_location('app','/workspace/rosebound/server.py'); app=importlib.util.module_from_spec(spec); spec.loader.exec_module(app)
class Journeys(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  cls.server=app.ThreadingHTTPServer(('127.0.0.1',0),app.Handler);cls.base='http://127.0.0.1:'+str(cls.server.server_port)
  threading.Thread(target=cls.server.serve_forever,daemon=True).start()
 @classmethod
 def tearDownClass(cls): cls.server.shutdown();cls.server.server_close()
 def client(self):return urllib.request.build_opener(urllib.request.HTTPCookieProcessor(http.cookiejar.CookieJar()))
 def call(self,c,path,data=None,origin=None):
  headers={'Content-Type':'application/json'}
  if origin:headers['Origin']=origin
  r=urllib.request.Request(self.base+'/api/'+path,data=json.dumps(data).encode() if data is not None else None,headers=headers)
  try:
   with c.open(r) as resp:return resp.status,json.load(resp)
  except urllib.error.HTTPError as e:return e.code,json.load(e)
 def signup(self,c,email):return self.call(c,'signup',{'email':email,'password':'Test-password-123','name':'Test Reader'})
 def test_01_reading_journey_and_isolation(self):
  a,b=self.client(),self.client()
  self.assertEqual(self.call(a,'library')[0],401)
  self.assertEqual(self.signup(a,'a@example.test')[0],200)
  self.assertEqual(self.signup(b,'b@example.test')[0],200)
  p={'genres':['Fantasy'],'goal':20,'mood':'Cozy','theme':'sage'}
  self.assertEqual(self.call(a,'profile',{'profile':p})[1]['user']['profile']['genres'],['Fantasy'])
  book=self.call(a,'catalog')[1]['books'][0]
  self.assertEqual(self.call(a,'shelf',{'book':book,'status':'Reading','page':100,'rating':4.5,'review':'A thoughtful story.'})[0],200)
  shelf=self.call(a,'library')[1]['books'];self.assertEqual(len(shelf),1);self.assertEqual(shelf[0]['page'],100);self.assertEqual(shelf[0]['rating'],4.5)
  self.assertEqual(self.call(b,'library')[1]['books'],[])
  self.assertEqual(self.call(a,'signout',{})[0],200)
  self.assertEqual(self.call(a,'library')[0],401)
  self.assertEqual(self.call(a,'signin',{'email':'a@example.test','password':'Test-password-123'})[0],200)
  self.assertEqual(self.call(a,'library')[1]['books'][0]['review'],'A thoughtful story.')
  self.assertEqual(self.call(a,'shelf',{'book':book,'status':'Finished','page':book['pages']})[0],200)
  self.assertEqual(self.call(a,'library')[1]['books'][0]['status'],'Finished')
  self.call(a,'shelf',{'book':book,'remove':True});self.assertEqual(self.call(a,'library')[1]['books'],[])
 def test_02_validation_and_csrf(self):
  c=self.client();self.signup(c,'c@example.test')
  self.assertEqual(self.call(c,'profile',{'profile':{'genres':'invalid'}})[0],400)
  self.assertEqual(self.call(c,'profile',{'profile':{}},'https://attacker.test')[0],403)
  book=self.call(c,'catalog')[1]['books'][0]
  self.assertEqual(self.call(c,'shelf',{'book':book,'rating':4.3})[0],400)
  self.assertEqual(self.call(c,'shelf',{'book':book,'status':'Unknown'})[0],400)
 def test_03_credentials(self):
  c=self.client();self.signup(c,'d@example.test')
  self.assertEqual(self.signup(c,'d@example.test')[0],409)
  self.assertEqual(self.call(c,'signin',{'email':'d@example.test','password':'wrong-password'})[0],401)
  with app.connect() as db:
   u=db.execute('select * from users where email=?',('d@example.test',)).fetchone()
   self.assertNotEqual(u['password'],'Test-password-123');self.assertEqual(len(u['password']),128)
if __name__=='__main__':unittest.main(verbosity=2)
