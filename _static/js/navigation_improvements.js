document.addEventListener('DOMContentLoaded', function () {
    // Detect if we're on the homepage
    const currentPath = window.location.pathname;
    const isHomepage = currentPath.endsWith('basis.html') || currentPath.endsWith('/');

    if (isHomepage) {
        document.body.classList.add('index');
    }

    // 1. Highlight current page in sidebar and scroll to it
    const sidebarLinks = document.querySelectorAll('.wy-menu-vertical a');

    sidebarLinks.forEach(link => {
        const linkPath = new URL(link.href, window.location.origin).pathname;

        if (linkPath === currentPath) {
            // Add highlight class
            link.classList.add('current-page-highlight');

            // Scroll the sidebar to center this item IMMEDIATELY (no delay, no animation)
            const sidebar = document.querySelector('.wy-side-scroll');
            if (sidebar) {
                const linkRect = link.getBoundingClientRect();
                const sidebarRect = sidebar.getBoundingClientRect();

                // Calculate scroll position to center the link
                const scrollTop = link.offsetTop - (sidebarRect.height / 2) + (linkRect.height / 2);

                // Use instant scroll (no smooth animation on page load)
                sidebar.scrollTo({
                    top: scrollTop,
                    behavior: 'auto'  // Changed from 'smooth' to 'auto' for instant scroll
                });
            }
        }
    });

    // Note: Breadcrumbs are now fixed via CSS directly, no need to add class here

    // 2. Create floating navigation buttons
    createFloatingNavButtons();

    // 3. Add keyboard navigation (Arrow keys)
    addKeyboardNavigation();
});

function createFloatingNavButtons() {
    // Find prev/next links from <head> <link> tags instead of footer
    const prevLink = document.querySelector('link[rel="prev"]');
    const nextLink = document.querySelector('link[rel="next"]');

    if (!prevLink && !nextLink) return; // No navigation available

    // Create floating container
    const floatingNav = document.createElement('div');
    floatingNav.className = 'floating-nav-buttons';

    // Create Previous button
    if (prevLink) {
        const prevBtn = document.createElement('a');
        prevBtn.href = prevLink.href;
        prevBtn.className = 'floating-nav-btn floating-nav-prev';
        prevBtn.title = `Предыдущая страница (←)\n${prevLink.title || ''}`;
        prevBtn.innerHTML = '<i class="fa fa-chevron-left"></i>';
        floatingNav.appendChild(prevBtn);
    }

    // Create Next button
    if (nextLink) {
        const nextBtn = document.createElement('a');
        nextBtn.href = nextLink.href;
        nextBtn.className = 'floating-nav-btn floating-nav-next';
        nextBtn.title = `Следующая страница (→)\n${nextLink.title || ''}`;
        nextBtn.innerHTML = '<i class="fa fa-chevron-right"></i>';
        floatingNav.appendChild(nextBtn);
    }

    document.body.appendChild(floatingNav);
}

function addKeyboardNavigation() {
    // Use link tags from head for keyboard navigation
    const prevLink = document.querySelector('link[rel="prev"]');
    const nextLink = document.querySelector('link[rel="next"]');

    document.addEventListener('keydown', function (e) {
        // Ignore if user is typing in an input field
        if (e.target.tagName === 'INPUT' || e.target.tagName === 'TEXTAREA') {
            return;
        }

        // Left arrow - previous page
        if (e.key === 'ArrowLeft' && prevLink) {
            window.location.href = prevLink.href;
        }

        // Right arrow - next page
        if (e.key === 'ArrowRight' && nextLink) {
            window.location.href = nextLink.href;
        }
    });
}
