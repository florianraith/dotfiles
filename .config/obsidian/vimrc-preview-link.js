// Open the Page preview popover for the link under the text cursor.
// Loaded from .obsidian.vimrc via ":jsfile". Receives `editor`, `view`, `selection`.

const cursor = editor.getCursor();
const line = editor.getLine(cursor.line);

// Locate a [[wikilink]] or [text](target) spanning the cursor column, and
// remember where its inner text sits so we can anchor to it rather than to the
// surrounding brackets.
let inner = null;
for (const re of [/\[\[([^\[\]]+?)\]\]/g, /\[[^\[\]]*\]\(([^()]+?)\)/g]) {
    let match;
    while ((match = re.exec(line)) !== null) {
        if (cursor.ch >= match.index && cursor.ch <= match.index + match[0].length) {
            const offset = match[0].indexOf(match[1]);
            inner = {
                text: match[1],
                from: match.index + offset,
                to: match.index + offset + match[1].length
            };
            break;
        }
    }
    if (inner) break;
}

if (!inner) {
    console.log('[vimrc preview] no link at cursor:', JSON.stringify(line), cursor.ch);
} else {
    const cm = editor.cm;

    // Anchor the popover to whatever is painted at the middle of the link text.
    const mid = Math.floor((inner.from + inner.to) / 2);
    const coords = cm.coordsAtPos(editor.posToOffset({ line: cursor.line, ch: mid }));
    const targetEl = coords
        ? document.elementFromPoint(Math.round(coords.left + 1),
                                   Math.round((coords.top + coords.bottom) / 2))
        : null;

    // Note: do NOT replay a mouseover on targetEl. That opens a popover which
    // Obsidian's own pointer tracking then closes, because the real cursor
    // isn't over the link, producing a visible flash before this one opens.
    app.workspace.trigger('hover-link', {
        event: new MouseEvent('mouseover', {
            clientX: coords ? Math.round(coords.left + 1) : 0,
            clientY: coords ? Math.round((coords.top + coords.bottom) / 2) : 0,
            metaKey: true,
            ctrlKey: true
        }),
        source: 'editor',
        hoverParent: view,
        targetEl: targetEl || cm.dom,
        linktext: inner.text.split('|')[0].trim(),
        sourcePath: view.file ? view.file.path : ''
    });

    // The popover normally closes when the real pointer leaves the link.
    // Nothing moved the pointer here, so dismiss it on the next keystroke,
    // click or scroll instead.
    const dismiss = () => {
        document.removeEventListener('keydown', dismiss, true);
        document.removeEventListener('mousedown', dismiss, true);
        document.removeEventListener('wheel', dismiss, true);
        if (view.hoverPopover) {
            try { view.hoverPopover.hide(); } catch (e) { /* already gone */ }
            view.hoverPopover = null;
        }
        document.querySelectorAll('.popover.hover-popover').forEach(el => el.remove());
    };

    // Deferred by a tick so the keydown that ran this command doesn't dismiss it.
    window.setTimeout(() => {
        document.addEventListener('keydown', dismiss, true);
        document.addEventListener('mousedown', dismiss, true);
        document.addEventListener('wheel', dismiss, true);
    }, 0);
}
