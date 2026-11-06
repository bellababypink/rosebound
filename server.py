"""Rosebound development server. Python 3.12+, no third-party dependencies."""
import hashlib, hmac, http.cookies, json, os, secrets, sqlite3, time, urllib.request, urllib.parse
from http.server import ThreadingHTTPServer, BaseHTTPRequestHandler
from pathlib import Path

ROOT = Path(__file__).resolve().parent
DATA = Path(os.environ.get('ROSEBOUND_DATA', str(ROOT / '.data')))
DATA.mkdir(parents=True, exist_ok=True, mode=0o700)
DB = DATA / 'rosebound.sqlite3'

def connect():
    db = sqlite3.connect(DB, timeout=15)
    db.row_factory = sqlite3.Row
    db.execute('PRAGMA foreign_keys=ON')
    return db

with connect() as db:
    db.executescript('''
    CREATE TABLE IF NOT EXISTS users(id INTEGER PRIMARY KEY, email TEXT UNIQUE NOT NULL, password TEXT NOT NULL, salt TEXT NOT NULL, name TEXT NOT NULL, profile TEXT NOT NULL DEFAULT '{}');
    CREATE TABLE IF NOT EXISTS sessions(token TEXT PRIMARY KEY, user_id INTEGER NOT NULL REFERENCES users(id), expires INTEGER NOT NULL);
    CREATE TABLE IF NOT EXISTS shelves(user_id INTEGER NOT NULL REFERENCES users(id), book_id TEXT NOT NULL, book TEXT NOT NULL, status TEXT NOT NULL, page INTEGER NOT NULL DEFAULT 0, rating REAL NOT NULL DEFAULT 0, review TEXT NOT NULL DEFAULT '', PRIMARY KEY(user_id,book_id));
    CREATE TABLE IF NOT EXISTS attempts(ip TEXT PRIMARY KEY, count INTEGER NOT NULL, expires INTEGER NOT NULL);
    ''')
os.chmod(DB, 0o600)

CATALOG = [
 {'id':'9780385547345','title':'Tomorrow, and Tomorrow, and Tomorrow','author':'Gabrielle Zevin','genre':'Literary fiction','pages':416,'color':'#315f70','accent':'#f5b850','motif':'✳','label':'TOMORROW,\nAND TOMORROW,\nAND TOMORROW'},
 {'id':'9780593441275','title':'Book Lovers','author':'Emily Henry','genre':'Romance','pages':384,'color':'#bf594d','accent':'#ffe9b2','motif':'❧','label':'BOOK\nLOVERS'},
 {'id':'9781635577020','title':'A Court of Silver Flames','author':'Sarah J. Maas','genre':'Fantasy','pages':768,'color':'#4d6657','accent':'#e5dba6','motif':'☾','label':'A COURT\nOF SILVER\nFLAMES'},
 {'id':'9780593321201','title':'The Secret History','author':'Donna Tartt','genre':'Literary fiction','pages':576,'color':'#514539','accent':'#e7d4b3','motif':'❦','label':'THE\nSECRET\nHISTORY'},
 {'id':'9781250080400','title':'The Invisible Life of Addie LaRue','author':'V. E. Schwab','genre':'Fantasy','pages':448,'color':'#283944','accent':'#d4bf85','motif':'✧','label':'THE INVISIBLE\nLIFE OF\nADDIE LARUE'},
 {'id':'9780593101190','title':'The House in the Cerulean Sea','author':'TJ Klune','genre':'Fantasy','pages':400,'color':'#608f91','accent':'#fff1b7','motif':'⌂','label':'THE HOUSE IN\nTHE CERULEAN\nSEA'},
 {'id':'9780593334836','title':'Legends & Lattes','author':'Travis Baldree','genre':'Fantasy','pages':304,'color':'#786b52','accent':'#fae5bd','motif':'☕','label':'LEGENDS\n& LATTES'},
 {'id':'9780593336823','title':'Love and Other Words','author':'Christina Lauren','genre':'Romance','pages':432,'color':'#be788c','accent':'#fff1dc','motif':'♡','label':'LOVE AND\nOTHER\nWORDS'}
]

class Handler(BaseHTTPRequestHandler):
    def log_message(self, fmt, *args):
        # Never log payloads, session tokens, or search queries.
        pass
    def send(self, status, data, cookie=None):
        payload = json.dumps(data).encode()
        self.send_response(status)
        self.send_header('Content-Type','application/json')
        self.send_header('Cache-Control','no-store')
        self.send_header('X-Content-Type-Options','nosniff')
        if cookie: self.send_header('Set-Cookie', cookie)
        self.end_headers()
        self.wfile.write(payload)
    def user(self, db):
        c = http.cookies.SimpleCookie()
        try: c.load(self.headers.get('Cookie',''))
        except http.cookies.CookieError: return None
        token = c.get('rose_session')
        if not token: return None
        return db.execute('SELECT u.* FROM users u JOIN sessions s ON u.id=s.user_id WHERE s.token=? AND s.expires>?',(hashlib.sha256(token.value.encode()).hexdigest(),time.time())).fetchone()
    def public_user(self, u):
        return {'id':u['id'],'name':u['name'],'email':u['email'],'profile':json.loads(u['profile'])}
    def do_GET(self):
        path = urllib.parse.urlsplit(self.path)
        if path.path.startswith('/api/'):
            with connect() as db:
                if path.path == '/api/catalog': return self.send(200, {'books':CATALOG})
                if path.path == '/api/search':
                    q = urllib.parse.parse_qs(path.query).get('q',[''])[0].strip()[:160]
                    if len(q)<2: return self.send(400,{'error':'Enter at least two characters.'})
                    try:
                        url = 'https://openlibrary.org/search.json?' + urllib.parse.urlencode({'q':q,'limit':18,'fields':'key,title,author_name,cover_i,edition_key,number_of_pages_median'})
                        req = urllib.request.Request(url,headers={'User-Agent':'RoseboundDevelopment/0.1'})
                        with urllib.request.urlopen(req,timeout=12) as r: data=json.load(r)
                        books=[{'id':d['key'],'title':d['title'],'author':', '.join(d.get('author_name', ['Unknown author'])),'pages':d.get('number_of_pages_median') or 300,'genre':'From Open Library','color':'#63776b','accent':'#fff0cf','motif':'❦','label':d['title'],'source':'https://openlibrary.org'+d['key']} for d in data.get('docs',[])]
                        return self.send(200,{'books':books,'source':'Open Library'})
                    except Exception: return self.send(503,{'error':'Live search cannot reach Open Library right now. You can still explore our starter collection. Please try again later.'})
                u = self.user(db)
                if not u: return self.send(401,{'error':'Please sign in to save your reading life.'})
                if path.path == '/api/me': return self.send(200,{'user':self.public_user(u)})
                if path.path == '/api/library':
                    rows=db.execute('SELECT * FROM shelves WHERE user_id=?',(u['id'],)).fetchall()
                    return self.send(200,{'books':[dict(json.loads(r['book']),status=r['status'],page=r['page'],rating=r['rating'],review=r['review']) for r in rows]})
                return self.send(404,{'error':'Not found'})
        file = {'/app.js':'app.js','/style.css':'style.css'}.get(path.path,'index.html')
        content=(ROOT/'public'/file).read_bytes()
        self.send_response(200)
        self.send_header('Content-Type',{'app.js':'text/javascript','style.css':'text/css','index.html':'text/html'}[file]+'; charset=utf-8')
        self.send_header('X-Content-Type-Options','nosniff')
        self.send_header('Content-Security-Policy',"default-src 'self'; style-src 'self'; script-src 'self'; img-src 'self' data:; connect-src 'self'; frame-ancestors 'none'; base-uri 'self'; form-action 'self'")
        self.end_headers(); self.wfile.write(content)
    def do_POST(self):
        # Same-origin JSON only. No CORS; browsers cannot submit cross-origin JSON.
        origin=self.headers.get('Origin')
        if origin and urllib.parse.urlsplit(origin).netloc != self.headers.get('Host'): return self.send(403,{'error':'Invalid request origin'})
        if self.headers.get('Content-Type','').split(';')[0] != 'application/json': return self.send(415,{'error':'JSON required'})
        try:
            size=int(self.headers.get('Content-Length',0))
            if size<0 or size>24000: return self.send(413,{'error':'Request too large'})
            body=json.loads(self.rfile.read(size))
            if not isinstance(body,dict): raise ValueError()
            self.post(body)
        except (ValueError,TypeError,KeyError): self.send(400,{'error':'Please check the form fields.'})
        except sqlite3.IntegrityError: self.send(409,{'error':'An account with that email already exists. Please sign in.'})
        except Exception: self.send(500,{'error':'Something went wrong. Please try again.'})
    def post(self,b):
        with connect() as db:
            if self.path in ['/api/signup','/api/signin']:
                ip=self.client_address[0]; now=time.time()
                attempt=db.execute('SELECT * FROM attempts WHERE ip=?',(ip,)).fetchone()
                if attempt and attempt['expires']>now and attempt['count']>=20: return self.send(429,{'error':'Too many attempts. Try again in 15 minutes.'})
                db.execute('INSERT INTO attempts VALUES(?,1,?) ON CONFLICT(ip) DO UPDATE SET count=CASE WHEN expires<? THEN 1 ELSE count+1 END, expires=CASE WHEN expires<? THEN excluded.expires ELSE expires END',(ip,now+900,now,now)); db.commit()
                email=str(b.get('email','')).strip().lower(); password=str(b.get('password',''))
                if '@' not in email or len(email)>254 or not 10<=len(password)<=200: return self.send(400,{'error':'Use a valid email and a password of 10–200 characters.'})
                if self.path=='/api/signup':
                    name=str(b.get('name','')).strip()[:60]
                    if not name: return self.send(400,{'error':'What should we call you?'})
                    salt=secrets.token_hex(16); hashed=hashlib.scrypt(password.encode(),salt=salt.encode(),n=16384,r=8,p=1).hex()
                    db.execute('INSERT INTO users(email,password,salt,name) VALUES(?,?,?,?)',(email,hashed,salt,name))
                u=db.execute('SELECT * FROM users WHERE email=?',(email,)).fetchone()
                salt=u['salt'] if u else 'unmatched-account'
                hashed=hashlib.scrypt(password.encode(),salt=salt.encode(),n=16384,r=8,p=1).hex()
                if not u or not hmac.compare_digest(hashed,u['password']): return self.send(401,{'error':'Email or password is incorrect.'})
                token=secrets.token_urlsafe(32)
                db.execute('DELETE FROM sessions WHERE expires<?',(now,))
                db.execute('INSERT INTO sessions VALUES(?,?,?)',(hashlib.sha256(token.encode()).hexdigest(),u['id'],now+604800))
                db.commit()
                secure='; Secure' if os.environ.get('ROSEBOUND_SECURE_COOKIE')=='1' else ''
                return self.send(200,{'user':self.public_user(u)},'rose_session='+token+'; HttpOnly; SameSite=Lax; Path=/; Max-Age=604800'+secure)
            u=self.user(db)
            if not u: return self.send(401,{'error':'Please sign in first.'})
            if self.path=='/api/signout':
                db.execute('DELETE FROM sessions WHERE user_id=?',(u['id'],)); db.commit()
                return self.send(200,{'ok':True},'rose_session=; HttpOnly; SameSite=Lax; Path=/; Max-Age=0')
            if self.path=='/api/profile':
                p=b.get('profile',{}); genres=p.get('genres',[])
                if not isinstance(genres,list) or len(genres)>12 or any(not isinstance(g,str) or len(g)>40 for g in genres): raise ValueError()
                profile={'genres':genres,'mood':str(p.get('mood',''))[:80],'social':str(p.get('social',''))[:80],'goal':max(1,min(1000,int(p.get('goal',12)))),'bio':str(p.get('bio',''))[:400],'theme':p.get('theme') if p.get('theme') in ['rose','sage'] else 'rose','onboarded':True}
                name=str(b.get('name',u['name'])).strip()[:60]
                if not name: raise ValueError()
                db.execute('UPDATE users SET name=?,profile=? WHERE id=?',(name,json.dumps(profile),u['id'])); db.commit()
                u=db.execute('SELECT * FROM users WHERE id=?',(u['id'],)).fetchone()
                return self.send(200,{'user':self.public_user(u)})
            if self.path=='/api/shelf':
                book=b['book']; bookid=str(book['id'])[:120]
                if not bookid: raise ValueError()
                if b.get('remove'):
                    db.execute('DELETE FROM shelves WHERE user_id=? AND book_id=?',(u['id'],bookid)); db.commit(); return self.send(200,{'ok':True})
                status=b.get('status','Want to read')
                if status not in ['Want to read','Reading','Finished','DNF','Favourites']: raise ValueError()
                pages=max(1,min(100000,int(book.get('pages',300))))
                clean={k:str(book.get(k,''))[:500] for k in ['id','title','author','genre','color','accent','motif','label','source']}; clean['pages']=pages
                if not clean['title']: raise ValueError()
                page=max(0,min(pages,int(b.get('page',0)))); rating=float(b.get('rating',0))
                if rating not in [i/2 for i in range(11)]: raise ValueError()
                review=str(b.get('review',''))[:3000]
                db.execute('INSERT INTO shelves VALUES(?,?,?,?,?,?,?) ON CONFLICT(user_id,book_id) DO UPDATE SET book=excluded.book,status=excluded.status,page=excluded.page,rating=excluded.rating,review=excluded.review',(u['id'],bookid,json.dumps(clean),status,page,rating,review)); db.commit()
                return self.send(200,{'ok':True})
            self.send(404,{'error':'Not found'})

if __name__=='__main__':
    port=int(os.environ.get('PORT','5001'))
    print(f'Rosebound serving on port {port}',flush=True)
    ThreadingHTTPServer(('0.0.0.0',port),Handler).serve_forever()
