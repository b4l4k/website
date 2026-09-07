const projectHover = window.matchMedia('(hover: hover) and (pointer: fine)');

document.querySelectorAll('.project-item').forEach((item) => {
    const card = item.querySelector('.project-card');
    const front = item.querySelector('.project-front');
    const back = item.querySelector('.project-back');
    const toggle = item.querySelector('.project-toggle');
    const title = item.querySelector('.project-title').textContent;
    let pinned = false;
    let hovered = false;

    function updateCard() {
        const expanded = pinned || hovered || back.contains(document.activeElement);
        item.classList.toggle('is-flipped', expanded);
        toggle.setAttribute('aria-expanded', String(expanded));
        toggle.textContent = expanded ? 'Show image' : 'Show details';
        toggle.setAttribute('aria-label', `${toggle.textContent}: ${title}`);
        front.setAttribute('aria-hidden', String(expanded));
        back.setAttribute('aria-hidden', String(!expanded));
        back.inert = !expanded;
    }

    item.classList.add('is-interactive');
    toggle.hidden = false;
    updateCard();

    toggle.addEventListener('click', () => {
        pinned = toggle.getAttribute('aria-expanded') !== 'true';
        hovered = false;
        updateCard();
    });

    // Tapping the image also reveals details; the button provides keyboard access.
    card.addEventListener('click', (event) => {
        if (!event.target.closest('a')) {
            pinned = true;
            updateCard();
        }
    });

    card.addEventListener('pointerenter', (event) => {
        if (projectHover.matches && event.pointerType === 'mouse') {
            hovered = true;
            updateCard();
        }
    });

    card.addEventListener('pointerleave', () => {
        hovered = false;
        updateCard();
    });

    // Keep a focused link available when the pointer moves off its card.
    back.addEventListener('focusout', () => queueMicrotask(updateCard));

    item.addEventListener('keydown', (event) => {
        if (event.key === 'Escape') {
            pinned = false;
            hovered = false;
            if (back.contains(document.activeElement)) {
                toggle.focus();
            }
            updateCard();
        }
    });
});
