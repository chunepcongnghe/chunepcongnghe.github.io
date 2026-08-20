(()=> {
  const q=(selector,context=document)=>context.querySelector(selector);
  const qa=(selector,context=document)=>[...context.querySelectorAll(selector)];
  const normalize=value=>(value||'').toString().normalize('NFD').replace(/[\u0300-\u036f]/g,'').toLowerCase();

  const menu=q('[data-menu]');
  const mobile=q('[data-mobile-nav]');
  if(menu&&mobile){
    menu.addEventListener('click',()=>{
      const open=mobile.classList.toggle('open');
      menu.setAttribute('aria-expanded',String(open));
    });
    qa('a',mobile).forEach(link=>link.addEventListener('click',()=>{
      mobile.classList.remove('open');
      menu.setAttribute('aria-expanded','false');
    }));
  }

  const currentPath=location.pathname.replace(/\/$/,'')||'/';
  qa('.main-nav a,.mobile-nav>a,.section-shortcuts a').forEach(link=>{
    const linkPath=new URL(link.href,location.origin).pathname.replace(/\/$/,'')||'/';
    if(linkPath===currentPath) link.setAttribute('aria-current','page');
  });

  let searchData=[];
  const searchSource=q('#site-search-data');
  if(searchSource){
    try{searchData=JSON.parse(searchSource.textContent||'[]');}catch(error){searchData=[];}
  }
  const closeSearchResults=()=>qa('[data-search-results]').forEach(box=>{box.hidden=true;box.innerHTML='';});
  qa('[data-site-search]').forEach(input=>{
    const wrapper=input.closest('.search-box,.mobile-search');
    const results=wrapper?q('[data-search-results]',wrapper):null;
    if(!results)return;
    input.addEventListener('input',()=>{
      const raw=input.value.trim();
      const term=normalize(raw);
      if(term.length<2){results.hidden=true;results.innerHTML='';return;}
      const matches=searchData.filter(item=>normalize([item.title,item.description,item.category].join(' ')).includes(term)).slice(0,7);
      results.innerHTML='';
      const heading=document.createElement('div');
      heading.className='search-result-heading';
      heading.textContent=matches.length?(matches.length+' kết quả phù hợp'):'Chưa tìm thấy bài phù hợp';
      results.appendChild(heading);
      matches.forEach(item=>{
        const link=document.createElement('a');
        link.href=item.url;
        const meta=document.createElement('span');
        meta.textContent=(item.category||'Công nghệ')+' · '+(item.date||'');
        const title=document.createElement('b');
        title.textContent=item.title;
        link.append(meta,title);
        results.appendChild(link);
      });
      results.hidden=false;
    });
    input.addEventListener('keydown',event=>{if(event.key==='Escape'){input.value='';closeSearchResults();input.blur();}});
  });
  document.addEventListener('click',event=>{if(!event.target.closest('.search-box,.mobile-search'))closeSearchResults();});

  qa('[data-filter]').forEach(button=>button.addEventListener('click',()=>{
    const value=button.dataset.filter;
    qa('[data-filter]').forEach(item=>item.classList.toggle('active',item===button));
    qa('[data-category]').forEach(card=>card.classList.toggle('search-hidden',value!=='all'&&card.dataset.category!==value));
  }));

  const back=q('[data-backtop]');
  if(back){
    const sync=()=>back.classList.toggle('show',scrollY>600);
    addEventListener('scroll',sync,{passive:true});
    sync();
    back.addEventListener('click',()=>scrollTo({top:0,behavior:'smooth'}));
  }

  const content=q('.article-content');
  const toc=q('[data-toc]');
  if(content&&toc){
    const headings=qa('h2,h3',content);
    if(headings.length){
      headings.forEach((heading,index)=>{
        if(!heading.id)heading.id='muc-'+(index+1);
        const link=document.createElement('a');
        link.href='#'+heading.id;
        link.textContent=heading.textContent;
        if(heading.tagName==='H3')link.classList.add('toc-sub');
        toc.appendChild(link);
      });
      if('IntersectionObserver' in window){
        const links=qa('a',toc);
        const observer=new IntersectionObserver(entries=>{
          entries.forEach(entry=>{
            if(!entry.isIntersecting)return;
            links.forEach(link=>link.classList.toggle('active',link.getAttribute('href')==='#'+entry.target.id));
          });
        },{rootMargin:'-110px 0px -70% 0px'});
        headings.forEach(heading=>observer.observe(heading));
      }
    }else toc.closest('.toc')?.remove();
  }

  const avatar='/assets/chunep-canonical.webp?v=20260820-sharp';
  qa('img[data-chunep]').forEach(img=>{img.src=avatar;img.removeAttribute('data-chunep');});
})();
