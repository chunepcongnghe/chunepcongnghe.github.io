(()=> {
  const q=(s,c=document)=>c.querySelector(s), qa=(s,c=document)=>[...c.querySelectorAll(s)];
  const menu=q('[data-menu]'), mobile=q('[data-mobile-nav]');
  if(menu&&mobile) menu.addEventListener('click',()=>{const open=mobile.classList.toggle('open');menu.setAttribute('aria-expanded',String(open));});
  const search=q('[data-site-search]');
  if(search) search.addEventListener('input',e=>{const term=e.target.value.trim().toLowerCase();qa('[data-search-item]').forEach(el=>{const hay=(el.dataset.search||el.innerText).toLowerCase();el.classList.toggle('search-hidden',term&&!hay.includes(term));});});
  qa('[data-filter]').forEach(btn=>btn.addEventListener('click',()=>{const value=btn.dataset.filter;qa('[data-filter]').forEach(b=>b.classList.toggle('active',b===btn));qa('[data-category]').forEach(card=>card.classList.toggle('search-hidden',value!=='all'&&card.dataset.category!==value));}));
  const back=q('[data-backtop]');if(back){const sync=()=>back.classList.toggle('show',scrollY>600);addEventListener('scroll',sync,{passive:true});sync();back.addEventListener('click',()=>scrollTo({top:0,behavior:'smooth'}));}
  const content=q('.article-content'), toc=q('[data-toc]');if(content&&toc){const hs=qa('h2,h3',content);if(hs.length){hs.forEach((h,i)=>{if(!h.id)h.id='muc-'+(i+1);const a=document.createElement('a');a.href='#'+h.id;a.textContent=h.textContent;a.style.paddingLeft=h.tagName==='H3'?'12px':'0';toc.appendChild(a);});}else toc.closest('.toc')?.remove();}

  // Editorial thumbnail art direction approved on 19/08/2026:
  // real/product photography, cinematic depth, no flat vector mockups.
  const editorialThumbs={
    'galaxy-z-2026.svg':'https://etf-rebalancing.com/images/phone-preorder/galaxy-z-fold8-flip8-hero.webp',
    'galaxy-z-flip8-review.svg':'https://img.tamindir.com/resize/1200x675/2025/12/470608/samsung-galaxy-z-flip-8-islemcisi-sizinti-1.jpg',
    'macbook-air-m5-moi.svg':'https://s.yimg.com/ny/api/res/1.2/oiOFMCzS4EZ6ucpQQ3ULcA--/YXBwaWQ9aGlnaGxhbmRlcjt3PTEyNDI7aD02OTg-/https%3A/media.zenfs.com/en/pc_mag_263/b02f90f2dd8eaca3838e77da502b307b',
    'macbook-m5-vs-m4.svg':'https://s.yimg.com/ny/api/res/1.2/oiOFMCzS4EZ6ucpQQ3ULcA--/YXBwaWQ9aGlnaGxhbmRlcjt3PTEyNDI7aD02OTg-/https%3A/media.zenfs.com/en/pc_mag_263/b02f90f2dd8eaca3838e77da502b307b',
    'macbook-m5-ram.svg':'https://img.evetech.co.za/repository/ez/How-Much-RAM-Do-You-Really-Need-for-Gaming-in-2025-banner.webp?width=1200',
    'ram-16gb-2026.svg':'https://img.evetech.co.za/repository/ez/How-Much-RAM-Do-You-Really-Need-for-Gaming-in-2025-banner.webp?width=1200',
    'macbook-m5-creator.svg':'https://miro.medium.com/0%2Akv7PnwnJj_OTRxAv',
    'ai-device-value.svg':'https://futureforwardit.in/images/uploaded/generated-image-3.jpg',
    'action6-review.svg':'https://www.gadgetmatch.com/wp-content/uploads/2025/11/gadgetmatch-20251122-dji-osmo-action-6-1.jpg',
    'action6-roadtrip.svg':'https://cdn.shopify.com/s/files/1/0108/1062/files/CS0124_CAR__QLA-ACA_-QLP-360-SB_-QLP-360-SPA__MG_0015.jpg?v=1723081972',
    'action6-or-5pro.svg':'https://camerajabber.com/wp-content/uploads/2025/11/DJI-Osmo-Action-6-09.jpg',
    'action6-vs-5pro.svg':'https://cdn.mos.cms.futurecdn.net/QuzDN6VcKi5eX9WDT46dpU.jpg'
  };
  qa('img').forEach(img=>{
    const raw=img.getAttribute('src')||'';
    const key=raw.split('?')[0].split('/').pop();
    const replacement=editorialThumbs[key];
    if(!replacement) return;
    const original=raw;
    img.referrerPolicy='no-referrer';
    img.decoding='async';
    img.addEventListener('error',()=>{if(img.src!==original) img.src=original;},{once:true});
    img.src=replacement;
  });

  const avatar='/assets/chunep-canonical.webp?v=20260820-sharp';
  qa('img[data-chunep]').forEach(img=>{img.src=avatar;img.removeAttribute('data-chunep');});
})();
