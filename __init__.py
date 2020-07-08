from aqt import gui_hooks, mw
from aqt.browser import SearchContext
from PyQt5 import QtWidgets

from .config import getUserOption, setUserOption


def one_by_note(ctx: SearchContext):
    if not getUserOption("One card by note", True):
        return
    nids = set()
    filtered_card = []
    selected_card = mw.reviewer.card
    selected_cid = selected_card.id if selected_card else 0
    selected_nid = selected_card.nid if selected_card else 0
    idx_of_selected_note = None
    # position of the unique card of note currently in reviewer
    for cid in ctx.card_ids:
        card = mw.col.getCard(cid)
        nid = card.nid
        if nid not in nids:
            filtered_card.append(cid)
            nids.add(nid)
            if nid == selected_nid:
                idx_of_selected_note = len(filtered_card) - 1
        elif cid == selected_cid:  # nid in nids
            filtered_card.pop(idx_of_selected_note)
            filtered_card.append(cid)
    ctx.card_ids = filtered_card


gui_hooks.browser_did_search.append(one_by_note)


def will_show(browser):
    browser.form.action_only_note = QtWidgets.QAction(browser)
    bfan = browser.form.action_only_note
    browser.form.menu_Notes.addAction(bfan)
    bfan.setText("Card/Note")
    bfan.setCheckable(True)
    bfan.setChecked(getUserOption("One card by note"))
    bfan.setShortcut(getUserOption("Shortcut", "Ctrl+Alt+N"))
    bfan.triggered.connect(lambda: on_card_note(browser))


def on_card_note(browser):
    setUserOption("One card by note", not getUserOption(
        "One card by note", True))
    browser.onSearchActivated()  


gui_hooks.browser_will_show.append(will_show)
