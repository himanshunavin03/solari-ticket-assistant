import {test, expect} from '@playwright/test';

test('real backend known match, evidence, reset and no match', async ({page}) => {
  await page.goto('/');
  await expect(page.locator('.connection')).toContainText('Connected');
  await page.getByLabel('Try an example').selectOption('NT-3');
  await page.getByRole('button', {name:'Find similar tickets'}).click();
  await expect(page.getByRole('heading', {name:'Charged twice for the same billing cycle'})).toBeVisible();
  await expect(page.getByText('ORIGINAL RESOLUTION', {exact:true}).first()).toBeVisible();
  await page.getByText('Relevance evidence & technical details').first().click();
  await expect(page.getByText(/Semantic cosine:/).first()).toBeVisible();
  await page.screenshot({path:'../artifacts/ui-desktop.png',fullPage:true});
  await page.getByRole('button', {name:'Clear',exact:true}).click();
  await expect(page.getByLabel('Subject',{exact:true})).toHaveValue('');
  // Keep an unrelated no-match check as well as issue-level regression tests below.
  await page.getByLabel('Subject',{exact:true}).fill('Office delivery');
  await page.getByLabel('Description',{exact:true}).fill('A parcel containing a desk lamp was delivered to the wrong building.');
  await page.getByRole('button', {name:'Find similar tickets'}).click();
  await expect(page.getByRole('heading', {name:'No relevant history'})).toBeVisible();
  await page.setViewportSize({width:390,height:844});
  expect(await page.evaluate(()=>document.documentElement.scrollWidth <= window.innerWidth)).toBeTruthy();
  await page.screenshot({path:'../artifacts/ui-mobile.png',fullPage:true});
});

test('validation and failed backend request', async ({page}) => {
  await page.goto('/');
  await page.getByRole('button', {name:'Find similar tickets'}).click();
  await expect(page.getByRole('alert')).toHaveText('Enter both a subject and a description.');
  await page.getByLabel('Subject',{exact:true}).fill('A real issue');
  await page.getByLabel('Description',{exact:true}).fill('The customer cannot access the dashboard.');
  await page.route('**/api/search', route=>route.abort('failed'));
  await page.getByRole('button', {name:'Find similar tickets'}).click();
  await expect(page.getByRole('alert')).toBeVisible();
  await expect(page.getByRole('heading',{name:'Relevant history'})).toBeVisible();
});

test('an older response cannot overwrite the next search', async ({page}) => {
  let calls=0;
  await page.route('**/api/search', async route=>{
    const first=++calls===1;
    if(first) await new Promise(resolve=>setTimeout(resolve,800));
    try {await route.fulfill({json:{outcome:first?'historical_precedents':'no_relevant_history',active_mode:'hybrid',degraded:false,
      matches:first?[{ticket:{ticket_id:'OLD',subject:'Stale result',description:'Old',category:'test',tags:[],resolution_notes:'Old'},keyword_score:1,semantic_score:1,fusion_score:1}]:[]}});} catch { /* Aborted requests may close before the delayed handler completes. */ }
  });
  await page.goto('/');
  await page.getByLabel('Subject',{exact:true}).fill('First');
  await page.getByLabel('Description',{exact:true}).fill('First issue');
  await page.getByRole('button', {name:'Find similar tickets'}).click();
  await expect.poll(()=>calls).toBe(1);
  await page.getByLabel('Subject',{exact:true}).fill('Second');
  await page.getByRole('button', {name:'Find similar tickets'}).click();
  await expect(page.getByRole('heading',{name:'No relevant history'})).toBeVisible();
  await page.waitForTimeout(1000);
  await expect(page.getByRole('heading',{name:'Stale result'})).toHaveCount(0);
});

test('real keyword-only degraded service returns unverified billing precedent', async ({page}) => {
  await page.route('**/api/**',async route=>{
    const path=new URL(route.request().url()).pathname;
    const response=await route.fetch({url:'http://127.0.0.1:8001'+path});
    await route.fulfill({response});
  });
  await page.goto('/');
  await expect(page.locator('.connection')).toContainText('Keyword only');
  await expect(page.getByLabel('Search approach')).toHaveValue('keyword');
  await expect(page.getByText(/Semantic search is unavailable/)).toBeVisible();
  await page.getByLabel('Try an example').selectOption('NT-3');
  const result=page.waitForResponse(response=>response.url().endsWith('/api/search'));
  await page.getByRole('button',{name:'Find similar tickets'}).click();
  const body=await (await result).json();
  expect(body.degraded).toBe(true);
  expect(body.matches[0].applicability).toBe('unverified');
  await expect(page.getByRole('heading',{name:'Charged twice for the same billing cycle'})).toBeVisible();
  await expect(page.getByText('ORIGINAL RESOLUTION',{exact:true})).toBeVisible();
  await expect(page.getByText('Applicability unverified',{exact:true}).first()).toBeVisible();
  await page.getByLabel('Search approach').selectOption('hybrid');
  await page.getByRole('button',{name:'Find similar tickets'}).click();
  await expect(page.getByRole('alert')).toContainText('Semantic retrieval unavailable');
});

test('unsupported integration and missing reset delivery withhold resolutions', async ({page}) => {
  await page.goto('/');
  await expect(page.locator('.connection')).toContainText('Connected');
  for (const example of ['NT-4','NT-1']) {
    await page.getByLabel('Try an example').selectOption(example);
    await page.getByRole('button',{name:'Find similar tickets'}).click();
    await expect(page.getByRole('heading',{name:'Related history only'})).toBeVisible();
    await expect(page.getByText('ORIGINAL RESOLUTION',{exact:true})).toHaveCount(0);
    await expect(page.getByText('Weak or conflicting related history',{exact:true})).toBeVisible();
  }
});

test('HTTP 429 retrieves historical resolution with unverified applicability', async ({page}) => {
  await page.goto('/');
  await page.getByLabel('Subject',{exact:true}).fill('429 errors on integration');
  await page.getByLabel('Description',{exact:true}).fill('Normal integration traffic is now being rejected with HTTP 429 even though usage did not increase.');
  await page.getByRole('button',{name:'Find similar tickets'}).click();
  await expect(page.getByRole('heading',{name:'API rate limit reached during normal usage'})).toBeVisible();
  await expect(page.getByText('ORIGINAL RESOLUTION',{exact:true})).toBeVisible();
});

test('short contradictory symptom is retained and its resolution withheld',async ({page})=>{
  await page.goto('/');
  for(const mode of ['hybrid','keyword']) {
    await page.getByLabel('Search approach').selectOption(mode);
    await page.getByLabel('Subject',{exact:true}).fill('Password reset issue');
    await page.getByLabel('Description',{exact:true}).fill('The customer completed the password reset successfully but email never arrives.');
    await page.getByRole('button',{name:'Find similar tickets'}).click();
    await expect(page.getByRole('heading',{name:'Related history only'})).toBeVisible();
    await expect(page.getByText('ORIGINAL RESOLUTION',{exact:true})).toHaveCount(0);
  }
});
