"""Build public PHH feed artifacts; do not alter Shopify products or PMP settings."""
from phh_select import select
from phh_localize import prepare_translations
from phh_translate import translate
from phh_render import render

if __name__=='__main__':
    records,audit=select()
    tasks,cache=prepare_translations(records)
    if tasks:
        cache=translate(tasks,cache)
    render(records,cache,audit)
