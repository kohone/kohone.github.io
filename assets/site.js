(() => {
  const tools = document.querySelector('.catalog-tools');
  if (!tools) return;
  const cards = [...document.querySelectorAll('.product-card')];
  const filters = [...tools.querySelectorAll('[data-filter]')];
  const search = tools.querySelector('input');
  const results = document.querySelector('.results');
  const empty = document.querySelector('.empty-state');
  let category = 'All';
  function update() {
    const query = search.value.trim().toLocaleLowerCase();
    let count = 0;
    for (const card of cards) {
      card.hidden = !((category === 'All' || card.dataset.category === category) && card.dataset.search.includes(query));
      if (!card.hidden) count++;
    }
    results.textContent = `${count} ${count === 1 ? 'app' : 'apps'} found`;
    empty.hidden = count !== 0;
  }
  for (const button of filters) button.addEventListener('click', () => {
    category = button.dataset.filter;
    for (const item of filters) item.setAttribute('aria-pressed', String(item === button));
    update();
  });
  search.addEventListener('input', update);
  tools.hidden = false;
  update();
})();
