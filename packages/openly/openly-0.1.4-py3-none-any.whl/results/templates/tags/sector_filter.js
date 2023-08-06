var tag = this;

tag.set_active_sector = function (e) {
    localStorage.setItem('active_sector', e.item.sector);
}