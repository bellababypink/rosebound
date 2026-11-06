"""Run the existing API journeys against Waitress and verify hosting headers."""
import threading
import urllib.request
from waitress import create_server
from test_journeys import Journeys
from wsgi import application

class ProductionJourneys(Journeys):
 @classmethod
 def setUpClass(cls):
  cls.server=create_server(application,host='127.0.0.1',port=0,threads=4,max_request_body_size=24000)
  cls.base='http://127.0.0.1:'+str(cls.server.effective_port)
  threading.Thread(target=cls.server.run,daemon=True).start()
 @classmethod
 def tearDownClass(cls):
  cls.server.close();cls.server.task_dispatcher.shutdown()
 def test_04_health_and_headers(self):
  c=self.client()
  self.assertEqual(self.call(c,'health')[1],{'status':'ok'})
  with c.open(self.base+'/') as r:
   self.assertIn("default-src 'self'",r.headers['Content-Security-Policy'])
   self.assertEqual(r.headers['Referrer-Policy'],'strict-origin-when-cross-origin')
  req=urllib.request.Request(self.base+'/',method='HEAD')
  with c.open(req) as r:self.assertEqual(r.read(),b'')
 def test_05_secure_cookie(self):
  import os,json
  os.environ['ROSEBOUND_SECURE_COOKIE']='1'
  try:
   req=urllib.request.Request(self.base+'/api/signup',data=json.dumps({'email':'secure@example.test','name':'Secure','password':'Secure-password-123'}).encode(),headers={'Content-Type':'application/json'})
   with urllib.request.urlopen(req) as r:
    self.assertIn('Secure',r.headers['Set-Cookie'])
    self.assertIn('HttpOnly',r.headers['Set-Cookie'])
    self.assertEqual(r.headers['Strict-Transport-Security'],'max-age=31536000')
  finally:os.environ.pop('ROSEBOUND_SECURE_COOKIE',None)

if __name__=='__main__':
 import unittest
 suite=unittest.defaultTestLoader.loadTestsFromTestCase(ProductionJourneys)
 result=unittest.TextTestRunner(verbosity=2).run(suite)
 raise SystemExit(not result.wasSuccessful())
