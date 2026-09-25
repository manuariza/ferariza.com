(() => {
  'use strict';
  const books = [...document.querySelectorAll('.book')];
  const shelf = document.querySelector('.bookshelf');
  const category = document.querySelector('#shelf-category');
  const reduced = window.matchMedia('(prefers-reduced-motion: reduce)');
  const mobile = window.matchMedia('(max-width: 700px)');
  let selected = books[0];
  const visibleBooks = () => books.filter(book => !book.hidden);
  function selectBook(book, {url = true, scroll = false} = {}) {
    if (!book) return;
    if (book.hidden) { category.value = 'all'; books.forEach(b => b.hidden = false); }
    books.forEach(b => {
      const open = b === book;
      b.classList.toggle('is-open', open);
      b.querySelector('.spine').setAttribute('aria-expanded', String(open));
      b.querySelector('.book-panel').hidden = !open;
    });
    selected = book;
    if (url && location.hash !== '#libro-' + book.dataset.id) history.pushState(null, '', '#libro-' + book.dataset.id);
    const visible = visibleBooks();
    document.querySelector('.shelf-status').textContent = `${visible.indexOf(book) + 1} / ${visible.length} — ${book.querySelector('.spine-title').textContent}`;
    if (scroll) {
      if (mobile.matches) book.scrollIntoView({behavior: reduced.matches ? 'instant' : 'smooth', block:'start'});
      else {
        document.querySelector('#biblioteca').scrollIntoView({behavior: reduced.matches ? 'instant' : 'smooth', block:'start'});
        shelf.scrollTo({left: book.offsetLeft - shelf.offsetLeft, behavior: reduced.matches ? 'instant' : 'smooth'});
      }
    }
  }
  books.forEach(book => book.querySelector('.spine').addEventListener('click', () => selectBook(book, {scroll:mobile.matches}))); 
  category.addEventListener('change', () => {
    books.forEach(book => book.hidden = category.value !== 'all' && book.dataset.category !== category.value);
    selectBook(visibleBooks()[0], {url:true}); shelf.scrollLeft = 0;
  });
  function step(direction, focus = false) {
    const list = visibleBooks(); const book = list[(list.indexOf(selected) + direction + list.length) % list.length];
    selectBook(book);
    if (focus) book.querySelector('.spine').focus({preventScroll:true});
    if (!mobile.matches) shelf.scrollTo({left:book.offsetLeft - shelf.offsetLeft, behavior:reduced.matches ? 'instant':'smooth'});
    else if (focus) book.scrollIntoView({block:'nearest'});
  }
  document.querySelector('#previous-book').addEventListener('click', () => step(-1));
  document.querySelector('#next-book').addEventListener('click', () => step(1));
  shelf.addEventListener('keydown', event => {
    if (!event.target.matches('.spine')) return;
    if (['ArrowRight','ArrowDown','ArrowLeft','ArrowUp'].includes(event.key)) {event.preventDefault();step(['ArrowRight','ArrowDown'].includes(event.key)?1:-1,true);}
    if (event.key === 'Home' || event.key === 'End') {event.preventDefault(); const list=visibleBooks(); const b=event.key==='Home'?list[0]:list.at(-1);selectBook(b);b.querySelector('.spine').focus();}
  });
  const restoreHash = () => {
    const id = location.hash.replace(/^#(?:libro|obra)-/, '');
    if (!/^#(?:libro|obra)-/.test(location.hash)) return;
    const book = books.find(b => b.dataset.id === id);
    if (location.hash.startsWith('#libro-') && book) { selectBook(book, {url:false,scroll:true}); return; }
    const row = document.getElementById('obra-' + id);
    if (row) {
      document.querySelector('#work-search').value = '';
      document.querySelector('#index-category').value = 'all';
      document.querySelector('#work-search').dispatchEvent(new Event('input'));
      row.open = true;
      row.scrollIntoView({behavior:reduced.matches ? 'instant':'smooth',block:'start'});
    }
  };
  document.querySelectorAll('a[href^="#libro-"]').forEach(a => a.addEventListener('click', event => {event.preventDefault();selectBook(books.find(b => '#libro-'+b.dataset.id === a.hash),{scroll:true});}));
  window.addEventListener('hashchange',restoreHash);
  window.addEventListener('popstate',restoreHash);
  selectBook(selected,{url:false});
  if (document.readyState === 'complete') restoreHash();
  else window.addEventListener('load', restoreHash, {once:true});
  const normalize = s => s.normalize('NFD').replace(/[\u0300-\u036f]/g,'').toLowerCase();
  const pressSearch = document.querySelector('#press-search');
  const publication = document.querySelector('#press-publication');
  function filterPress() {
    let count=0;
    document.querySelectorAll('.archive-row').forEach(row => {
      row.hidden = !normalize(row.dataset.search).includes(normalize(pressSearch.value.trim())) || (publication.value !== 'all' && row.dataset.publication !== publication.value);
      if (!row.hidden) count++;
    });
    document.querySelector('#press-count').textContent = `${count} ${count===1?'artículo':'artículos'}`;
    document.querySelector('#press-empty').hidden = count !== 0;
  }
  pressSearch.addEventListener('input', filterPress);
  publication.addEventListener('change', filterPress);
  const search = document.querySelector('#work-search');
  const indexCategory = document.querySelector('#index-category');
  const rows = [...document.querySelectorAll('.index-row')];
  function filterIndex() {
    let count = 0;
    rows.forEach(row => {const show=normalize(row.dataset.search).includes(normalize(search.value.trim())) && (indexCategory.value==='all'||row.dataset.category===indexCategory.value);row.hidden=!show;if(show)count++;});
    document.querySelector('#result-count').textContent = `${count} ${count===1?'obra':'obras'}`;
    document.querySelector('#no-results').hidden = count !== 0;
  }
  search.addEventListener('input',filterIndex);indexCategory.addEventListener('change',filterIndex);
  document.querySelectorAll('.review-card').forEach(card => {
    function activate(){document.querySelectorAll('.review-card').forEach(c=>c.classList.toggle('is-active',c===card));}
    card.addEventListener('click',activate);card.addEventListener('focus',activate);
  });
  const moving = document.querySelector('.moving-type');
  const movingText = moving.firstElementChild;
  const header = document.querySelector('.header');
  const picture = document.querySelector('.hero-picture');
  let scheduled = false;
  function animate() {
    scheduled=false;
    if(reduced.matches)return;
    const box=moving.getBoundingClientRect();
    // Traverse the full overflow while the strip is visible below the sticky header.
    const start = innerHeight - box.height - 24;
    const end = header.getBoundingClientRect().bottom + 24;
    const progress = Math.max(0, Math.min(1, (start - box.top) / Math.max(1, start - end)));
    const travel = Math.max(0, movingText.scrollWidth - moving.clientWidth);
    movingText.style.transform = `translateX(${-travel * progress}px)`;
    const hero=picture.getBoundingClientRect();
    if(hero.top<innerHeight && hero.bottom>0) picture.firstElementChild.style.transform=`translateY(${Math.max(-35,Math.min(35,(innerHeight/2-hero.top)*.08))}px)`;
  }
  function scheduleAnimation() {if(!scheduled){scheduled=true;requestAnimationFrame(animate);}}
  window.addEventListener('scroll', scheduleAnimation, {passive:true});
  window.addEventListener('resize', scheduleAnimation);
  reduced.addEventListener('change', scheduleAnimation);
  new ResizeObserver(scheduleAnimation).observe(movingText);
  animate();
})();
