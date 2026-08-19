(()=> {
  const q = (s,c=document) => c.querySelector(s);
  const qa = (s,c=document) => [...c.querySelectorAll(s)];

  const menu = q('[data-menu]');
  const mobile = q('[data-mobile-nav]');
  if (menu && mobile) {
    menu.addEventListener('click', () => {
      const open = mobile.classList.toggle('open');
      menu.setAttribute('aria-expanded', String(open));
    });
  }

  const search = q('[data-site-search]');
  if (search) {
    search.addEventListener('input', e => {
      const term = e.target.value.trim().toLowerCase();
      qa('[data-search-item]').forEach(el => {
        const hay = (el.dataset.search || el.innerText).toLowerCase();
        el.classList.toggle('search-hidden', term && !hay.includes(term));
      });
    });
  }

  qa('[data-filter]').forEach(btn => btn.addEventListener('click', () => {
    const value = btn.dataset.filter;
    qa('[data-filter]').forEach(b => b.classList.toggle('active', b === btn));
    qa('[data-category]').forEach(card => {
      card.classList.toggle('search-hidden', value !== 'all' && card.dataset.category !== value);
    });
  }));

  const back = q('[data-backtop]');
  if (back) {
    const sync = () => back.classList.toggle('show', scrollY > 600);
    addEventListener('scroll', sync, {passive:true});
    sync();
    back.addEventListener('click', () => scrollTo({top:0, behavior:'smooth'}));
  }

  const content = q('.article-content');
  const toc = q('[data-toc]');
  if (content && toc) {
    const hs = qa('h2,h3', content);
    if (hs.length) {
      hs.forEach((h,i) => {
        if (!h.id) h.id = 'muc-' + (i+1);
        const a = document.createElement('a');
        a.href = '#' + h.id;
        a.textContent = h.textContent;
        a.style.paddingLeft = h.tagName === 'H3' ? '12px' : '0';
        toc.appendChild(a);
      });
    } else {
      const box = toc.closest('.toc');
      if (box) box.remove();
    }
  }

  qa('img[data-chunep]').forEach(img => {
    img.src = '/assets/chunep-canonical.webp?v=20260819-4';
    img.removeAttribute('data-chunep');
  });
})();