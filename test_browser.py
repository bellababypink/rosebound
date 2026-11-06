from playwright.sync_api import sync_playwright
import time
with sync_playwright() as p:
 browser=p.chromium.launch(executable_path='/usr/bin/chromium',headless=True,args=['--no-sandbox'])
 page=browser.new_page(viewport={'width':1440,'height':1100},device_scale_factor=1)
 errors=[]
 page.on('pageerror',lambda e:errors.append(str(e)))
 page.goto('http://127.0.0.1:5001');page.get_by_role('heading',name='Some stories stay').wait_for()
 page.screenshot(path='/workspace/rosebound/docs/home-desktop.png',full_page=True)
 page.locator('.sidebar .nav-item[data-go=profile]').click();page.locator('#join').click()
 page.locator('input[name=name]').fill('Alex Rose');page.locator('input[name=email]').fill(f'browser-{time.time_ns()}@example.test');page.locator('input[name=password]').fill('Browser-test-password-123')
 page.get_by_role('button',name='Create my account').click()
 page.get_by_text('Fantasy',exact=True).last.click();page.get_by_role('button',name='Continue').click();page.get_by_role('button',name='Continue').click();page.get_by_role('button',name='Make myself at home').click()
 page.locator('.sidebar [data-go=discover]').click();page.locator('.save-book').first.click()
 page.locator('select[name=status]').select_option('Reading');page.locator('input[name=page]').fill('80');page.locator('select[name=rating]').select_option('4.5');page.locator('textarea[name=review]').fill('A lovely reading experience.');page.get_by_role('button',name='Save to my bookshelf').click()
 page.locator('.sidebar [data-go=library]').click();page.locator('.book-card').first.wait_for();page.reload();page.locator('.book-card').first.wait_for()
 page.locator('.sidebar [data-go=home]').click();page.get_by_text('Page 80 of',exact=False).wait_for()
 page.set_viewport_size({'width':390,'height':844});page.screenshot(path='/workspace/rosebound/docs/home-mobile.png',full_page=True)
 for route in ['home','discover','library','profile']:
  page.goto('http://127.0.0.1:5001/#'+route);page.locator('main h1').wait_for()
  assert page.evaluate('document.documentElement.scrollWidth <= innerWidth'),f'Overflow on {route}'
 page.locator('.mobile-nav [data-go=profile]').click();page.locator('#signout').click();page.locator('#signin').wait_for()
 assert not errors, errors
 browser.close()
 print('Browser journeys passed: onboarding, save, progress, reload, four mobile routes, signout. No page errors or mobile overflow.')
