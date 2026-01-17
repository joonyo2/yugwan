/**
 * 유관순정신계승사업회 - Main JavaScript
 * =========================================
 */

(function() {
    'use strict';

    // ----------------------------------------
    // DOM Elements
    // ----------------------------------------
    const header = document.getElementById('header');
    const mobileMenuBtn = document.getElementById('mobileMenuBtn');
    const mobileMenu = document.getElementById('mobileMenu');
    const mobileNavLinks = document.querySelectorAll('.mobile-nav-link');
    const navLinks = document.querySelectorAll('.nav-link');

    // ----------------------------------------
    // Header Scroll Effect
    // ----------------------------------------
    function handleHeaderScroll() {
        if (window.scrollY > 50) {
            header.classList.add('scrolled');
        } else {
            header.classList.remove('scrolled');
        }
    }

    window.addEventListener('scroll', handleHeaderScroll);

    // ----------------------------------------
    // Mobile Menu Toggle
    // ----------------------------------------
    function toggleMobileMenu() {
        mobileMenuBtn.classList.toggle('active');
        mobileMenu.classList.toggle('active');
        document.body.style.overflow = mobileMenu.classList.contains('active') ? 'hidden' : '';
    }

    mobileMenuBtn.addEventListener('click', toggleMobileMenu);

    // Close mobile menu when clicking a link
    mobileNavLinks.forEach(link => {
        link.addEventListener('click', () => {
            mobileMenuBtn.classList.remove('active');
            mobileMenu.classList.remove('active');
            document.body.style.overflow = '';
        });
    });

    // ----------------------------------------
    // Smooth Scroll for Navigation Links
    // ----------------------------------------
    function smoothScroll(e) {
        const targetId = this.getAttribute('href');

        // 외부 링크나 다른 페이지 링크는 기본 동작 유지
        if (!targetId || !targetId.startsWith('#') || targetId === '#') return;

        const targetElement = document.querySelector(targetId);

        if (targetElement) {
            e.preventDefault();
            const headerHeight = header.offsetHeight;
            const targetPosition = targetElement.offsetTop - headerHeight;

            window.scrollTo({
                top: targetPosition,
                behavior: 'smooth'
            });
        }
    }

    navLinks.forEach(link => {
        link.addEventListener('click', smoothScroll);
    });

    mobileNavLinks.forEach(link => {
        link.addEventListener('click', smoothScroll);
    });

    // ----------------------------------------
    // Counter Animation
    // ----------------------------------------
    function animateCounter(element, target) {
        const duration = 2000;
        const start = 0;
        const startTime = performance.now();

        function updateCounter(currentTime) {
            const elapsed = currentTime - startTime;
            const progress = Math.min(elapsed / duration, 1);

            // Easing function (easeOutQuart)
            const easeProgress = 1 - Math.pow(1 - progress, 4);
            const current = Math.floor(start + (target - start) * easeProgress);

            element.textContent = current;

            if (progress < 1) {
                requestAnimationFrame(updateCounter);
            } else {
                element.textContent = target;
            }
        }

        requestAnimationFrame(updateCounter);
    }

    // ----------------------------------------
    // Intersection Observer for Animations
    // ----------------------------------------
    const observerOptions = {
        root: null,
        rootMargin: '0px',
        threshold: 0.1
    };

    // Counter Observer
    const counterObserver = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                const counters = entry.target.querySelectorAll('.counter');
                counters.forEach(counter => {
                    const target = parseInt(counter.textContent);
                    animateCounter(counter, target);
                });
                counterObserver.unobserve(entry.target);
            }
        });
    }, observerOptions);

    const metricsSection = document.getElementById('metrics');
    if (metricsSection) {
        counterObserver.observe(metricsSection);
    }

    // AOS-like Animation Observer
    const animationObserver = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                // Add delay if specified
                const delay = entry.target.getAttribute('data-aos-delay') || 0;
                setTimeout(() => {
                    entry.target.classList.add('aos-animate');
                }, parseInt(delay));
                animationObserver.unobserve(entry.target);
            }
        });
    }, {
        ...observerOptions,
        threshold: 0.15
    });

    // Observe all elements with data-aos attribute
    document.querySelectorAll('[data-aos]').forEach(element => {
        animationObserver.observe(element);
    });

    // ----------------------------------------
    // Parallax Effect for Hero Background
    // ----------------------------------------
    const heroSection = document.getElementById('hero');

    function handleParallax() {
        if (heroSection) {
            const scrolled = window.scrollY;
            const heroHeight = heroSection.offsetHeight;

            if (scrolled < heroHeight) {
                const parallaxSpeed = 0.3;
                const yPos = scrolled * parallaxSpeed;

                const heroBgLeft = heroSection.querySelector('.hero-bg-left');
                const heroBgRight = heroSection.querySelector('.hero-bg-right');

                if (heroBgLeft) {
                    heroBgLeft.style.transform = `translateY(${yPos}px)`;
                }
                if (heroBgRight) {
                    heroBgRight.style.transform = `translateY(${yPos * 0.5}px)`;
                }
            }
        }
    }

    window.addEventListener('scroll', handleParallax);

    // ----------------------------------------
    // Active Navigation Highlight
    // ----------------------------------------
    const sections = document.querySelectorAll('section[id]');

    function highlightNavigation() {
        const scrollPosition = window.scrollY + header.offsetHeight + 100;

        sections.forEach(section => {
            const sectionTop = section.offsetTop;
            const sectionHeight = section.offsetHeight;
            const sectionId = section.getAttribute('id');

            if (scrollPosition >= sectionTop && scrollPosition < sectionTop + sectionHeight) {
                navLinks.forEach(link => {
                    link.classList.remove('active');
                    if (link.getAttribute('href') === `#${sectionId}`) {
                        link.classList.add('active');
                    }
                });
            }
        });
    }

    window.addEventListener('scroll', highlightNavigation);

    // ----------------------------------------
    // Map Connection Line Animation
    // ----------------------------------------
    const connectionLine = document.querySelector('.connection-line');

    if (connectionLine) {
        const mapObserver = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    connectionLine.style.animation = 'lineExpand 1.5s ease forwards';
                    mapObserver.unobserve(entry.target);
                }
            });
        }, { threshold: 0.3 });

        const mapVisual = document.querySelector('.map-visual');
        if (mapVisual) {
            mapObserver.observe(mapVisual);
        }
    }

    // Add CSS animation for line expansion
    const styleSheet = document.createElement('style');
    styleSheet.textContent = `
        @keyframes lineExpand {
            from {
                transform: translateY(-50%) scaleX(0);
                transform-origin: left center;
            }
            to {
                transform: translateY(-50%) scaleX(1);
                transform-origin: left center;
            }
        }
    `;
    document.head.appendChild(styleSheet);

    // ----------------------------------------
    // Scroll Progress Indicator (Optional)
    // ----------------------------------------
    function createScrollProgress() {
        const progressBar = document.createElement('div');
        progressBar.className = 'scroll-progress';
        progressBar.style.cssText = `
            position: fixed;
            top: 0;
            left: 0;
            width: 0%;
            height: 3px;
            background: linear-gradient(90deg, var(--accent-gold), var(--accent-gold-light));
            z-index: 1001;
            transition: width 0.1s ease;
        `;
        document.body.appendChild(progressBar);

        window.addEventListener('scroll', () => {
            const scrollHeight = document.documentElement.scrollHeight - window.innerHeight;
            const scrollProgress = (window.scrollY / scrollHeight) * 100;
            progressBar.style.width = `${scrollProgress}%`;
        });
    }

    createScrollProgress();

    // ----------------------------------------
    // Hover Effects Enhancement
    // ----------------------------------------
    const gridItems = document.querySelectorAll('.grid-item');

    gridItems.forEach(item => {
        item.addEventListener('mouseenter', function() {
            this.style.transition = 'all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275)';
        });

        item.addEventListener('mouseleave', function() {
            this.style.transition = 'all 0.3s ease';
        });
    });

    // ----------------------------------------
    // Lazy Loading for Background Images
    // ----------------------------------------
    const lazyBackgrounds = document.querySelectorAll('[data-bg]');

    if ('IntersectionObserver' in window) {
        const bgObserver = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    const bg = entry.target.getAttribute('data-bg');
                    entry.target.style.backgroundImage = `url(${bg})`;
                    bgObserver.unobserve(entry.target);
                }
            });
        }, { rootMargin: '100px' });

        lazyBackgrounds.forEach(element => {
            bgObserver.observe(element);
        });
    }

    // ----------------------------------------
    // Accessibility: Skip to Content
    // ----------------------------------------
    function createSkipLink() {
        const skipLink = document.createElement('a');
        skipLink.href = '#hero';
        skipLink.className = 'skip-link';
        skipLink.textContent = '본문으로 건너뛰기';
        skipLink.style.cssText = `
            position: fixed;
            top: -100px;
            left: 50%;
            transform: translateX(-50%);
            background: var(--accent-gold);
            color: var(--primary-navy);
            padding: 10px 20px;
            border-radius: 4px;
            z-index: 10000;
            font-weight: 600;
            transition: top 0.3s ease;
        `;

        skipLink.addEventListener('focus', () => {
            skipLink.style.top = '10px';
        });

        skipLink.addEventListener('blur', () => {
            skipLink.style.top = '-100px';
        });

        document.body.insertBefore(skipLink, document.body.firstChild);
    }

    createSkipLink();

    // ----------------------------------------
    // Performance: Debounce/Throttle
    // ----------------------------------------
    function throttle(func, limit) {
        let inThrottle;
        return function(...args) {
            if (!inThrottle) {
                func.apply(this, args);
                inThrottle = true;
                setTimeout(() => inThrottle = false, limit);
            }
        };
    }

    // Apply throttle to scroll events
    window.addEventListener('scroll', throttle(handleHeaderScroll, 100));

    // ----------------------------------------
    // Initialize on DOM Ready
    // ----------------------------------------
    document.addEventListener('DOMContentLoaded', () => {
        // Initial header state
        handleHeaderScroll();

        // Add loaded class to body
        document.body.classList.add('loaded');

        // Trigger initial animation for hero content
        setTimeout(() => {
            const heroContent = document.querySelector('.hero-content');
            if (heroContent) {
                heroContent.classList.add('visible');
            }
        }, 100);
    });

    // ----------------------------------------
    // Handle Page Visibility
    // ----------------------------------------
    document.addEventListener('visibilitychange', () => {
        if (document.hidden) {
            // Pause animations when page is not visible
            document.body.classList.add('paused');
        } else {
            document.body.classList.remove('paused');
        }
    });

    // ----------------------------------------
    // Console Easter Egg
    // ----------------------------------------
    console.log('%c유관순정신계승사업회', 'font-size: 24px; font-weight: bold; color: #c5a059;');
    console.log('%c"1919년의 외침, 2026년의 울림이 되다."', 'font-size: 14px; color: #8892b0; font-style: italic;');

})();
