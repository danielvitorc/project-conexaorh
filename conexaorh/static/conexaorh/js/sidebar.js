/* ===== SIDEBAR CORPORATIVA - JAVASCRIPT AVANÇADO ===== */

class CorporateSidebar {
    constructor() {
        this.sidebar = document.getElementById('sidebar');
        this.themeToggleButton = document.getElementById('themeToggleButton');
        this.themeIcon = document.getElementById('themeIcon');
        this.isExpanded = false;
        this.isMobile = window.innerWidth <= 1024;
        this.currentTheme = localStorage.getItem('theme') || 'light';
        
        this.init();
    }

    init() {
        this.setupEventListeners();
        this.setupTheme();
        this.setupTooltips();
        this.setupRippleEffects();
        this.setupMobileHandling();
        this.setupKeyboardNavigation();
        this.addStatusIndicators();
        this.animateOnLoad();
    }

    setupEventListeners() {
        // Theme toggle
        if (this.themeToggleButton) {
            this.themeToggleButton.addEventListener('click', () => this.toggleTheme());
        }

        // Sidebar hover effects (desktop only)
        if (!this.isMobile && this.sidebar) {
            this.sidebar.addEventListener('mouseenter', () => this.expandSidebar());
            this.sidebar.addEventListener('mouseleave', () => this.collapseSidebar());
        }

        // Window resize handling
        window.addEventListener('resize', () => this.handleResize());

        // Keyboard shortcuts
        document.addEventListener('keydown', (e) => this.handleKeyboardShortcuts(e));

        // Click outside to close mobile sidebar
        document.addEventListener('click', (e) => this.handleOutsideClick(e));
    }

    setupTheme() {
        // Apply saved theme
        document.documentElement.setAttribute('data-theme', this.currentTheme);
        this.updateThemeIcon();
        
        // Add smooth transition for theme changes
        document.documentElement.style.transition = 'all 0.3s cubic-bezier(0.4, 0, 0.2, 1)';
    }

    toggleTheme() {
        this.currentTheme = this.currentTheme === 'light' ? 'dark' : 'light';
        document.documentElement.setAttribute('data-theme', this.currentTheme);
        localStorage.setItem('theme', this.currentTheme);
        this.updateThemeIcon();
        
        // Add visual feedback
        this.addThemeChangeEffect();
    }

    updateThemeIcon() {
        if (this.themeIcon) {
            this.themeIcon.className = this.currentTheme === 'light' ? 'fas fa-moon' : 'fas fa-sun';
        }
    }

    addThemeChangeEffect() {
        // Create a subtle flash effect when changing themes
        const overlay = document.createElement('div');
        overlay.style.cssText = `
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: ${this.currentTheme === 'light' ? '#ffffff' : '#000000'};
            opacity: 0.1;
            pointer-events: none;
            z-index: 9999;
            transition: opacity 0.3s ease;
        `;
        
        document.body.appendChild(overlay);
        
        setTimeout(() => {
            overlay.style.opacity = '0';
            setTimeout(() => overlay.remove(), 300);
        }, 50);
    }

    expandSidebar() {
        if (!this.isMobile && this.sidebar) {
            this.sidebar.classList.add('expanded');
            this.isExpanded = true;
            this.animateNavItems(true);
        }
    }

    collapseSidebar() {
        if (!this.isMobile && this.sidebar) {
            this.sidebar.classList.remove('expanded');
            this.isExpanded = false;
            this.animateNavItems(false);
        }
    }

    animateNavItems(expanding) {
        const navItems = this.sidebar?.querySelectorAll('.sidebar-nav a, .sidebar-item');
        if (!navItems) return;

        navItems.forEach((item, index) => {
            const span = item.querySelector('span');
            if (span) {
                if (expanding) {
                    setTimeout(() => {
                        span.style.transform = 'translateX(0)';
                        span.style.opacity = '1';
                    }, index * 50);
                } else {
                    span.style.transform = 'translateX(-10px)';
                    span.style.opacity = '0';
                }
            }
        });
    }

    setupTooltips() {
        const navItems = this.sidebar?.querySelectorAll('.sidebar-nav a, .sidebar-item');
        if (!navItems) return;

        navItems.forEach(item => {
            const span = item.querySelector('span');
            if (span) {
                const tooltip = document.createElement('div');
                tooltip.className = 'sidebar-tooltip';
                tooltip.textContent = span.textContent;
                item.style.position = 'relative';
                item.appendChild(tooltip);
            }
        });
    }

    setupRippleEffects() {
        const clickableItems = this.sidebar?.querySelectorAll('.sidebar-nav a, .sidebar-item, #themeToggleButton');
        if (!clickableItems) return;

        clickableItems.forEach(item => {
            item.classList.add('ripple');
            
            item.addEventListener('click', (e) => {
                this.createRippleEffect(e, item);
            });
        });
    }

    createRippleEffect(event, element) {
        const ripple = document.createElement('span');
        const rect = element.getBoundingClientRect();
        const size = Math.max(rect.width, rect.height);
        const x = event.clientX - rect.left - size / 2;
        const y = event.clientY - rect.top - size / 2;

        ripple.style.cssText = `
            position: absolute;
            width: ${size}px;
            height: ${size}px;
            left: ${x}px;
            top: ${y}px;
            background: rgba(255, 255, 255, 0.3);
            border-radius: 50%;
            transform: scale(0);
            animation: ripple-animation 0.6s ease-out;
            pointer-events: none;
            z-index: 1;
        `;

        element.style.position = 'relative';
        element.style.overflow = 'hidden';
        element.appendChild(ripple);

        setTimeout(() => ripple.remove(), 600);
    }

    setupMobileHandling() {
        if (this.isMobile) {
            this.createMobileToggle();
            this.createOverlay();
        }
    }

    createMobileToggle() {
        const toggle = document.createElement('button');
        toggle.id = 'mobile-sidebar-toggle';
        toggle.innerHTML = '<i class="fas fa-bars"></i>';
        toggle.style.cssText = `
            position: fixed;
            top: 1rem;
            left: 1rem;
            z-index: 1001;
            background: var(--primary-color);
            color: white;
            border: none;
            border-radius: 8px;
            width: 44px;
            height: 44px;
            display: flex;
            align-items: center;
            justify-content: center;
            box-shadow: 0 4px 12px rgba(19, 75, 242, 0.3);
            transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        `;

        toggle.addEventListener('click', () => this.toggleMobileSidebar());
        document.body.appendChild(toggle);
    }

    createOverlay() {
        const overlay = document.createElement('div');
        overlay.className = 'sidebar-overlay';
        overlay.addEventListener('click', () => this.closeMobileSidebar());
        document.body.appendChild(overlay);
    }

    toggleMobileSidebar() {
        if (this.sidebar) {
            this.sidebar.classList.toggle('mobile-open');
            document.querySelector('.sidebar-overlay')?.classList.toggle('active');
            document.body.style.overflow = this.sidebar.classList.contains('mobile-open') ? 'hidden' : '';
        }
    }

    closeMobileSidebar() {
        if (this.sidebar) {
            this.sidebar.classList.remove('mobile-open');
            document.querySelector('.sidebar-overlay')?.classList.remove('active');
            document.body.style.overflow = '';
        }
    }

    handleResize() {
        const wasMobile = this.isMobile;
        this.isMobile = window.innerWidth <= 1024;

        if (wasMobile !== this.isMobile) {
            if (this.isMobile) {
                this.setupMobileHandling();
                this.collapseSidebar();
            } else {
                // Remove mobile elements
                document.getElementById('mobile-sidebar-toggle')?.remove();
                document.querySelector('.sidebar-overlay')?.remove();
                this.closeMobileSidebar();
            }
        }
    }

    handleOutsideClick(event) {
        if (this.isMobile && this.sidebar?.classList.contains('mobile-open')) {
            if (!this.sidebar.contains(event.target) && 
                !event.target.closest('#mobile-sidebar-toggle')) {
                this.closeMobileSidebar();
            }
        }
    }

    setupKeyboardNavigation() {
        const navItems = this.sidebar?.querySelectorAll('.sidebar-nav a, .sidebar-item');
        if (!navItems) return;

        navItems.forEach((item, index) => {
            item.setAttribute('tabindex', '0');
            
            item.addEventListener('keydown', (e) => {
                switch (e.key) {
                    case 'Enter':
                    case ' ':
                        e.preventDefault();
                        item.click();
                        break;
                    case 'ArrowDown':
                        e.preventDefault();
                        this.focusNextItem(index, navItems);
                        break;
                    case 'ArrowUp':
                        e.preventDefault();
                        this.focusPreviousItem(index, navItems);
                        break;
                }
            });
        });
    }

    focusNextItem(currentIndex, items) {
        const nextIndex = (currentIndex + 1) % items.length;
        items[nextIndex].focus();
    }

    focusPreviousItem(currentIndex, items) {
        const prevIndex = currentIndex === 0 ? items.length - 1 : currentIndex - 1;
        items[prevIndex].focus();
    }

    handleKeyboardShortcuts(event) {
        // Ctrl/Cmd + Shift + T for theme toggle
        if ((event.ctrlKey || event.metaKey) && event.shiftKey && event.key === 'T') {
            event.preventDefault();
            this.toggleTheme();
        }

        // Ctrl/Cmd + Shift + S for sidebar toggle (mobile)
        if (this.isMobile && (event.ctrlKey || event.metaKey) && event.shiftKey && event.key === 'S') {
            event.preventDefault();
            this.toggleMobileSidebar();
        }

        // Escape to close mobile sidebar
        if (event.key === 'Escape' && this.isMobile) {
            this.closeMobileSidebar();
        }
    }

    addStatusIndicators() {
        // Add online status indicator (simulated)
        const userProfile = document.querySelector('.user-profile .profile-img');
        if (userProfile) {
            const indicator = document.createElement('div');
            indicator.className = 'status-indicator online';
            userProfile.style.position = 'relative';
            userProfile.appendChild(indicator);
        }

        // Add notification badges to relevant nav items
        this.addNotificationBadges();
    }

    addNotificationBadges() {
        const pendingItems = this.sidebar?.querySelectorAll('a[href*="registros"], a[href*="pendentes"]');
        if (!pendingItems) return;

        pendingItems.forEach(item => {
            // Simulate notification count (in real app, this would come from API)
            const count = Math.floor(Math.random() * 5) + 1;
            if (count > 0) {
                const badge = document.createElement('div');
                badge.className = 'notification-badge';
                badge.setAttribute('data-count', count);
                item.style.position = 'relative';
                item.appendChild(badge);
            }
        });
    }

    animateOnLoad() {
        // Add entrance animation to sidebar
        if (this.sidebar) {
            this.sidebar.style.transform = 'translateX(-100%)';
            this.sidebar.style.opacity = '0';
            
            setTimeout(() => {
                this.sidebar.style.transition = 'all 0.5s cubic-bezier(0.4, 0, 0.2, 1)';
                this.sidebar.style.transform = 'translateX(0)';
                this.sidebar.style.opacity = '1';
            }, 100);
        }

        // Animate nav items
        const navItems = this.sidebar?.querySelectorAll('.sidebar-nav a, .sidebar-item');
        if (navItems) {
            navItems.forEach((item, index) => {
                item.style.opacity = '0';
                item.style.transform = 'translateX(-20px)';
                
                setTimeout(() => {
                    item.style.transition = 'all 0.4s cubic-bezier(0.4, 0, 0.2, 1)';
                    item.style.opacity = '1';
                    item.style.transform = 'translateX(0)';
                }, 200 + (index * 100));
            });
        }
    }

    // Public methods for external use
    setActiveItem(selector) {
        const items = this.sidebar?.querySelectorAll('.sidebar-nav a, .sidebar-item');
        if (!items) return;

        items.forEach(item => item.classList.remove('active'));
        
        const activeItem = this.sidebar?.querySelector(selector);
        if (activeItem) {
            activeItem.classList.add('active');
        }
    }

    updateNotificationCount(selector, count) {
        const item = this.sidebar?.querySelector(selector);
        if (!item) return;

        let badge = item.querySelector('.notification-badge');
        
        if (count > 0) {
            if (!badge) {
                badge = document.createElement('div');
                badge.className = 'notification-badge';
                item.style.position = 'relative';
                item.appendChild(badge);
            }
            badge.setAttribute('data-count', count);
            badge.style.display = 'block';
        } else if (badge) {
            badge.style.display = 'none';
        }
    }

    showLoadingState(selector) {
        const item = this.sidebar?.querySelector(selector);
        if (item) {
            item.classList.add('sidebar-loading');
        }
    }

    hideLoadingState(selector) {
        const item = this.sidebar?.querySelector(selector);
        if (item) {
            item.classList.remove('sidebar-loading');
        }
    }
}

// CSS for ripple animation
const rippleCSS = `
@keyframes ripple-animation {
    to {
        transform: scale(2);
        opacity: 0;
    }
}
`;

// Add CSS to document
const style = document.createElement('style');
style.textContent = rippleCSS;
document.head.appendChild(style);

// Initialize sidebar when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    window.corporateSidebar = new CorporateSidebar();
});

// Export for module use
if (typeof module !== 'undefined' && module.exports) {
    module.exports = CorporateSidebar;
}

// Additional utility functions
const SidebarUtils = {
    // Smooth scroll to top
    scrollToTop() {
        window.scrollTo({
            top: 0,
            behavior: 'smooth'
        });
    },

    // Add loading spinner to any element
    addLoadingSpinner(element) {
        const spinner = document.createElement('div');
        spinner.className = 'loading-spinner';
        spinner.innerHTML = '<i class="fas fa-spinner fa-spin"></i>';
        spinner.style.cssText = `
            position: absolute;
            top: 50%;
            left: 50%;
            transform: translate(-50%, -50%);
            color: var(--primary-color);
            z-index: 10;
        `;
        
        element.style.position = 'relative';
        element.appendChild(spinner);
        return spinner;
    },

    // Remove loading spinner
    removeLoadingSpinner(element) {
        const spinner = element.querySelector('.loading-spinner');
        if (spinner) {
            spinner.remove();
        }
    },

    // Show toast notification
    showToast(message, type = 'info', duration = 3000) {
        const toast = document.createElement('div');
        toast.className = `toast toast-${type}`;
        toast.textContent = message;
        toast.style.cssText = `
            position: fixed;
            top: 20px;
            right: 20px;
            background: var(--card-bg);
            color: var(--text-color);
            padding: 1rem 1.5rem;
            border-radius: 8px;
            box-shadow: var(--shadow-lg);
            border-left: 4px solid var(--primary-color);
            z-index: 10000;
            transform: translateX(100%);
            transition: transform 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        `;

        document.body.appendChild(toast);

        // Animate in
        setTimeout(() => {
            toast.style.transform = 'translateX(0)';
        }, 100);

        // Animate out and remove
        setTimeout(() => {
            toast.style.transform = 'translateX(100%)';
            setTimeout(() => toast.remove(), 300);
        }, duration);
    }
};

// Make utils globally available
window.SidebarUtils = SidebarUtils;

