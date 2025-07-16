/* ===== SISTEMA DE TEMAS CORPORATIVO AVANÇADO ===== */

class CorporateThemeManager {
    constructor() {
        this.currentTheme = localStorage.getItem('theme') || 'light';
        this.themeToggleButton = document.getElementById('themeToggleButton');
        this.themeIcon = document.getElementById('themeIcon');
        this.systemPreference = window.matchMedia('(prefers-color-scheme: dark)');
        this.transitionDuration = 300;
        
        this.init();
    }

    init() {
        this.applyTheme(this.currentTheme);
        this.setupEventListeners();
        this.setupSystemPreferenceListener();
        this.setupKeyboardShortcuts();
        this.addThemeTransitions();
        this.createThemePreview();
    }

    setupEventListeners() {
        if (this.themeToggleButton) {
            this.themeToggleButton.addEventListener('click', (e) => {
                e.preventDefault();
                this.toggleTheme();
            });

            // Add hover effects
            this.themeToggleButton.addEventListener('mouseenter', () => {
                this.addHoverEffect();
            });

            this.themeToggleButton.addEventListener('mouseleave', () => {
                this.removeHoverEffect();
            });
        }

        // Listen for theme changes from other tabs
        window.addEventListener('storage', (e) => {
            if (e.key === 'theme') {
                this.applyTheme(e.newValue);
            }
        });
    }

    setupSystemPreferenceListener() {
        this.systemPreference.addEventListener('change', (e) => {
            // Only auto-switch if user hasn't manually set a preference
            if (!localStorage.getItem('theme-manual')) {
                const newTheme = e.matches ? 'dark' : 'light';
                this.applyTheme(newTheme);
            }
        });
    }

    setupKeyboardShortcuts() {
        document.addEventListener('keydown', (e) => {
            // Ctrl/Cmd + Shift + T for theme toggle
            if ((e.ctrlKey || e.metaKey) && e.shiftKey && e.key === 'T') {
                e.preventDefault();
                this.toggleTheme();
                this.showThemeChangeNotification();
            }
        });
    }

    toggleTheme() {
        const newTheme = this.currentTheme === 'light' ? 'dark' : 'light';
        this.applyTheme(newTheme);
        localStorage.setItem('theme-manual', 'true'); // Mark as manually set
        this.createThemeTransitionEffect();
    }

    applyTheme(theme) {
        this.currentTheme = theme;
        
        // Apply theme to document
        document.documentElement.setAttribute('data-theme', theme);
        
        // Save to localStorage
        localStorage.setItem('theme', theme);
        
        // Update icon
        this.updateThemeIcon();
        
        // Update meta theme-color for mobile browsers
        this.updateMetaThemeColor();
        
        // Dispatch custom event
        this.dispatchThemeChangeEvent();
        
        // Update any theme-dependent elements
        this.updateThemeDependentElements();
    }

    updateThemeIcon() {
        if (!this.themeIcon) return;

        const iconClass = this.currentTheme === 'light' ? 'fas fa-moon' : 'fas fa-sun';
        
        // Add rotation animation
        this.themeIcon.style.transform = 'rotate(180deg) scale(0.8)';
        
        setTimeout(() => {
            this.themeIcon.className = iconClass;
            this.themeIcon.style.transform = 'rotate(0deg) scale(1)';
        }, this.transitionDuration / 2);
    }

    updateMetaThemeColor() {
        let metaThemeColor = document.querySelector('meta[name="theme-color"]');
        
        if (!metaThemeColor) {
            metaThemeColor = document.createElement('meta');
            metaThemeColor.name = 'theme-color';
            document.head.appendChild(metaThemeColor);
        }
        
        const color = this.currentTheme === 'light' ? '#134BF2' : '#1e293b';
        metaThemeColor.content = color;
    }

    dispatchThemeChangeEvent() {
        const event = new CustomEvent('themeChanged', {
            detail: {
                theme: this.currentTheme,
                timestamp: Date.now()
            }
        });
        document.dispatchEvent(event);
    }

    updateThemeDependentElements() {
        // Update charts, graphs, or other theme-dependent components
        const charts = document.querySelectorAll('[data-chart]');
        charts.forEach(chart => {
            this.updateChartTheme(chart);
        });

        // Update syntax highlighting if present
        const codeBlocks = document.querySelectorAll('pre[class*="language-"]');
        codeBlocks.forEach(block => {
            this.updateCodeBlockTheme(block);
        });

        // Update any custom components
        this.updateCustomComponents();
    }

    updateChartTheme(chartElement) {
        // Implementation would depend on chart library used
        // This is a placeholder for chart theme updates
        chartElement.setAttribute('data-theme', this.currentTheme);
    }

    updateCodeBlockTheme(codeBlock) {
        // Update syntax highlighting theme
        const themeClass = this.currentTheme === 'light' ? 'prism-light' : 'prism-dark';
        codeBlock.className = codeBlock.className.replace(/prism-(light|dark)/, themeClass);
    }

    updateCustomComponents() {
        // Update any custom components that need theme-specific handling
        const customComponents = document.querySelectorAll('[data-theme-component]');
        customComponents.forEach(component => {
            component.dispatchEvent(new CustomEvent('themeUpdate', {
                detail: { theme: this.currentTheme }
            }));
        });
    }

    addThemeTransitions() {
        // Add smooth transitions for theme changes
        const transitionCSS = `
            *, *::before, *::after {
                transition: 
                    background-color ${this.transitionDuration}ms cubic-bezier(0.4, 0, 0.2, 1),
                    border-color ${this.transitionDuration}ms cubic-bezier(0.4, 0, 0.2, 1),
                    color ${this.transitionDuration}ms cubic-bezier(0.4, 0, 0.2, 1),
                    box-shadow ${this.transitionDuration}ms cubic-bezier(0.4, 0, 0.2, 1) !important;
            }
        `;

        const style = document.createElement('style');
        style.id = 'theme-transitions';
        style.textContent = transitionCSS;
        document.head.appendChild(style);

        // Remove transitions after theme change to avoid performance issues
        setTimeout(() => {
            const existingStyle = document.getElementById('theme-transitions');
            if (existingStyle) {
                existingStyle.remove();
            }
        }, this.transitionDuration + 100);
    }

    createThemeTransitionEffect() {
        // Create a smooth visual transition effect
        const overlay = document.createElement('div');
        overlay.className = 'theme-transition-overlay';
        overlay.style.cssText = `
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: ${this.currentTheme === 'light' ? '#ffffff' : '#0f172a'};
            opacity: 0;
            pointer-events: none;
            z-index: 9999;
            transition: opacity ${this.transitionDuration}ms cubic-bezier(0.4, 0, 0.2, 1);
        `;

        document.body.appendChild(overlay);

        // Animate overlay
        requestAnimationFrame(() => {
            overlay.style.opacity = '0.1';
            
            setTimeout(() => {
                overlay.style.opacity = '0';
                
                setTimeout(() => {
                    overlay.remove();
                }, this.transitionDuration);
            }, 50);
        });
    }

    createThemePreview() {
        // Create a preview tooltip showing the next theme
        if (!this.themeToggleButton) return;

        const preview = document.createElement('div');
        preview.className = 'theme-preview';
        preview.style.cssText = `
            position: absolute;
            bottom: calc(100% + 12px);
            left: 50%;
            transform: translateX(-50%);
            background: var(--card-bg);
            color: var(--text-color);
            padding: 0.5rem 0.75rem;
            border-radius: 6px;
            font-size: 0.75rem;
            font-weight: 500;
            white-space: nowrap;
            opacity: 0;
            visibility: hidden;
            transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
            z-index: 1001;
            pointer-events: none;
            box-shadow: var(--shadow);
            border: 1px solid var(--border-color);
        `;

        preview.innerHTML = `
            <span class="preview-text">Alternar para tema ${this.currentTheme === 'light' ? 'escuro' : 'claro'}</span>
            <div class="preview-arrow"></div>
        `;

        // Add arrow
        const arrow = preview.querySelector('.preview-arrow');
        arrow.style.cssText = `
            position: absolute;
            top: 100%;
            left: 50%;
            transform: translateX(-50%);
            width: 0;
            height: 0;
            border-left: 4px solid transparent;
            border-right: 4px solid transparent;
            border-top: 4px solid var(--card-bg);
        `;

        this.themeToggleButton.style.position = 'relative';
        this.themeToggleButton.appendChild(preview);

        // Show/hide on hover
        this.themeToggleButton.addEventListener('mouseenter', () => {
            preview.style.opacity = '1';
            preview.style.visibility = 'visible';
            preview.style.transform = 'translateX(-50%) translateY(-4px)';
        });

        this.themeToggleButton.addEventListener('mouseleave', () => {
            preview.style.opacity = '0';
            preview.style.visibility = 'hidden';
            preview.style.transform = 'translateX(-50%) translateY(0)';
        });

        // Update preview text when theme changes
        document.addEventListener('themeChanged', () => {
            const previewText = preview.querySelector('.preview-text');
            if (previewText) {
                previewText.textContent = `Alternar para tema ${this.currentTheme === 'light' ? 'escuro' : 'claro'}`;
            }
        });
    }

    addHoverEffect() {
        if (this.themeIcon) {
            this.themeIcon.style.transform = 'scale(1.1) rotate(15deg)';
        }
    }

    removeHoverEffect() {
        if (this.themeIcon) {
            this.themeIcon.style.transform = 'scale(1) rotate(0deg)';
        }
    }

    showThemeChangeNotification() {
        const notification = document.createElement('div');
        notification.className = 'theme-notification';
        notification.style.cssText = `
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
            display: flex;
            align-items: center;
            gap: 0.5rem;
        `;

        const icon = this.currentTheme === 'light' ? '☀️' : '🌙';
        const themeName = this.currentTheme === 'light' ? 'Claro' : 'Escuro';
        
        notification.innerHTML = `
            <span>${icon}</span>
            <span>Tema ${themeName} ativado</span>
        `;

        document.body.appendChild(notification);

        // Animate in
        setTimeout(() => {
            notification.style.transform = 'translateX(0)';
        }, 100);

        // Animate out and remove
        setTimeout(() => {
            notification.style.transform = 'translateX(100%)';
            setTimeout(() => notification.remove(), 300);
        }, 2000);
    }

    // Public methods
    getTheme() {
        return this.currentTheme;
    }

    setTheme(theme) {
        if (theme === 'light' || theme === 'dark') {
            this.applyTheme(theme);
            localStorage.setItem('theme-manual', 'true');
        }
    }

    resetToSystemPreference() {
        localStorage.removeItem('theme-manual');
        const systemTheme = this.systemPreference.matches ? 'dark' : 'light';
        this.applyTheme(systemTheme);
    }

    // Theme-specific utilities
    isDarkTheme() {
        return this.currentTheme === 'dark';
    }

    isLightTheme() {
        return this.currentTheme === 'light';
    }

    // Get theme-appropriate colors
    getThemeColors() {
        const colors = {
            light: {
                primary: '#134BF2',
                secondary: '#000000',
                accent: '#0C87F2',
                background: '#F2F2F2',
                surface: '#ffffff',
                text: '#000000',
                textSecondary: '#6B7280'
            },
            dark: {
                primary: '#3B82F6',
                secondary: '#E5E7EB',
                accent: '#60A5FA',
                background: '#0F172A',
                surface: '#1E293B',
                text: '#F1F5F9',
                textSecondary: '#CBD5E1'
            }
        };

        return colors[this.currentTheme];
    }

    // Advanced theme features
    scheduleThemeChange(hour, theme) {
        const now = new Date();
        const scheduledTime = new Date();
        scheduledTime.setHours(hour, 0, 0, 0);

        if (scheduledTime <= now) {
            scheduledTime.setDate(scheduledTime.getDate() + 1);
        }

        const timeUntilChange = scheduledTime.getTime() - now.getTime();

        setTimeout(() => {
            this.setTheme(theme);
            this.showThemeChangeNotification();
        }, timeUntilChange);
    }

    enableAutoTheme() {
        // Auto switch based on time of day
        const hour = new Date().getHours();
        const isDayTime = hour >= 6 && hour < 18;
        const autoTheme = isDayTime ? 'light' : 'dark';
        
        this.setTheme(autoTheme);
        
        // Schedule next change
        if (isDayTime) {
            this.scheduleThemeChange(18, 'dark'); // Switch to dark at 6 PM
        } else {
            this.scheduleThemeChange(6, 'light'); // Switch to light at 6 AM
        }
    }
}

// Theme-aware component base class
class ThemeAwareComponent {
    constructor(element) {
        this.element = element;
        this.currentTheme = document.documentElement.getAttribute('data-theme');
        
        this.setupThemeListener();
    }

    setupThemeListener() {
        document.addEventListener('themeChanged', (e) => {
            this.currentTheme = e.detail.theme;
            this.onThemeChange(e.detail.theme);
        });
    }

    onThemeChange(theme) {
        // Override in subclasses
        console.log(`Theme changed to ${theme} for component`, this.element);
    }

    getThemeValue(lightValue, darkValue) {
        return this.currentTheme === 'light' ? lightValue : darkValue;
    }
}

// Initialize theme manager when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    window.corporateThemeManager = new CorporateThemeManager();
});

// Export for module use
if (typeof module !== 'undefined' && module.exports) {
    module.exports = { CorporateThemeManager, ThemeAwareComponent };
}

// Global utilities
window.ThemeUtils = {
    // Get current theme
    getCurrentTheme() {
        return window.corporateThemeManager?.getTheme() || 'light';
    },

    // Check if dark theme is active
    isDarkMode() {
        return window.corporateThemeManager?.isDarkTheme() || false;
    },

    // Get theme-appropriate color
    getThemeColor(colorName) {
        const colors = window.corporateThemeManager?.getThemeColors();
        return colors?.[colorName] || '#134BF2';
    },

    // Create theme-aware CSS custom property
    setThemeProperty(property, lightValue, darkValue) {
        const root = document.documentElement;
        const currentTheme = this.getCurrentTheme();
        const value = currentTheme === 'light' ? lightValue : darkValue;
        root.style.setProperty(property, value);
    },

    // Animate element based on theme
    animateThemeChange(element, lightStyles, darkStyles) {
        const currentTheme = this.getCurrentTheme();
        const styles = currentTheme === 'light' ? lightStyles : darkStyles;
        
        Object.assign(element.style, styles);
    }
};

document.addEventListener("DOMContentLoaded", () => {
  // Animar cards na entrada da página
  const cards = document.querySelectorAll(".card-welcome, .card-tabela-estilizada");
  cards.forEach(card => {
    setTimeout(() => {
      card.classList.add("show");
    }, 100); // pequeno delay para efeito nice
  });

  // Dropdown toggle com animação
  const dropdownIcon = document.querySelector(".dropdown-icon");
  const dropdownMenu = document.getElementById("userDropdown");
  // const blur = document.getElementById("blur-background"); // REMOVIDO: Elemento inexistente

  if (dropdownIcon && dropdownMenu) { // Adicionado verificação para garantir que os elementos existem
    dropdownIcon.addEventListener("click", () => {
      dropdownMenu.classList.toggle("show");
      // if (blur) { // REMOVIDO: Lógica do blur-background
      //   blur.style.display = dropdownMenu.classList.contains("show") ? "block" : "none";
      // }
    });

    // Fechar dropdown clicando fora
    document.addEventListener("click", e => {
      if (!dropdownMenu.contains(e.target) && !dropdownIcon.contains(e.target)) {
        dropdownMenu.classList.remove("show");
        // if (blur) { // REMOVIDO: Lógica do blur-background
        //   blur.style.display = "none";
        // }
      }
    });
  }

  // Scroll reveal para tabela (opcional)
  const tabela = document.querySelector(".card-tabela-estilizada");
  if (tabela) {
    const observer = new IntersectionObserver(entries => {
      entries.forEach(entry => {
        if(entry.isIntersecting){
          tabela.classList.add("show");
          observer.disconnect();
        }
      });
    }, {threshold: 0.1});
    observer.observe(tabela);
  }
});
