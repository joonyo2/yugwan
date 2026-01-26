/**
 * 유관순정신계승사업회 API 클라이언트
 * 백엔드 API 연동을 위한 공통 모듈
 */

const API = {
    // 기본 설정
    BASE_URL: window.location.hostname === 'localhost'
        ? 'http://localhost:8000/api/v1'
        : 'https://api.yugwansun.org/api/v1',

    // JWT 토큰 관리
    getToken() {
        return localStorage.getItem('access_token');
    },

    setToken(access, refresh) {
        localStorage.setItem('access_token', access);
        localStorage.setItem('refresh_token', refresh);
    },

    clearToken() {
        localStorage.removeItem('access_token');
        localStorage.removeItem('refresh_token');
    },

    // 공통 헤더
    getHeaders(isFormData = false) {
        const headers = {};
        if (!isFormData) {
            headers['Content-Type'] = 'application/json';
        }
        const token = this.getToken();
        if (token) {
            headers['Authorization'] = `Bearer ${token}`;
        }
        return headers;
    },

    // 공통 요청 처리
    async request(endpoint, options = {}) {
        const url = `${this.BASE_URL}${endpoint}`;
        const isFormData = options.body instanceof FormData;

        const config = {
            ...options,
            headers: {
                ...this.getHeaders(isFormData),
                ...options.headers
            }
        };

        try {
            const response = await fetch(url, config);

            // 401 에러시 토큰 갱신 시도
            if (response.status === 401 && this.getToken()) {
                const refreshed = await this.refreshToken();
                if (refreshed) {
                    config.headers = this.getHeaders(isFormData);
                    return fetch(url, config).then(r => this.handleResponse(r));
                } else {
                    this.clearToken();
                    window.location.href = '/join/membership.html?redirect=' + encodeURIComponent(window.location.pathname);
                    return;
                }
            }

            return this.handleResponse(response);
        } catch (error) {
            console.error('API Error:', error);
            throw { success: false, message: '네트워크 오류가 발생했습니다.' };
        }
    },

    async handleResponse(response) {
        const data = await response.json().catch(() => ({}));

        if (!response.ok) {
            throw {
                success: false,
                status: response.status,
                message: data.message || data.detail || '요청 처리 중 오류가 발생했습니다.',
                errors: data
            };
        }

        return { success: true, data };
    },

    async refreshToken() {
        const refresh = localStorage.getItem('refresh_token');
        if (!refresh) return false;

        try {
            const response = await fetch(`${this.BASE_URL}/auth/token/refresh/`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ refresh })
            });

            if (response.ok) {
                const data = await response.json();
                this.setToken(data.access, data.refresh || refresh);
                return true;
            }
            return false;
        } catch {
            return false;
        }
    },

    // === 인증 API ===
    auth: {
        async login(email, password) {
            const result = await API.request('/auth/token/', {
                method: 'POST',
                body: JSON.stringify({ email, password })
            });
            return result.data;
        },

        async register(userData) {
            const result = await API.request('/auth/register/', {
                method: 'POST',
                body: JSON.stringify(userData)
            });
            return result.data;
        },

        async getProfile() {
            const result = await API.request('/auth/profile/');
            return result.data;
        },

        async updateProfile(data) {
            const result = await API.request('/auth/profile/', {
                method: 'PATCH',
                body: JSON.stringify(data)
            });
            return result.data;
        },

        async changePassword(currentPassword, newPassword) {
            return API.request('/auth/password/change/', {
                method: 'POST',
                body: JSON.stringify({ current_password: currentPassword, new_password: newPassword })
            });
        },

        async deleteAccount(password) {
            return API.request('/auth/account/delete/', {
                method: 'POST',
                body: JSON.stringify({ password })
            });
        },

        isLoggedIn() {
            return !!API.getToken();
        },

        logout() {
            API.clearToken();
            localStorage.removeItem('yugwan_user');
        }
    },

    // === 웅변대회 API ===
    contest: {
        async apply(formData) {
            return API.request('/contest/apply/', {
                method: 'POST',
                body: formData
            });
        },

        async getMyApplication() {
            return API.request('/contest/my-application/');
        },

        async getWinners(year) {
            const query = year ? `?year=${year}` : '';
            return API.request(`/contest/winners/${query}`);
        }
    },

    // === 자료실 API ===
    archive: {
        async getNotices(params = {}) {
            const query = new URLSearchParams(params).toString();
            return API.request(`/archive/notices/${query ? '?' + query : ''}`);
        },

        async getNotice(id) {
            return API.request(`/archive/notices/${id}/`);
        },

        async getNews(params = {}) {
            const query = new URLSearchParams(params).toString();
            return API.request(`/archive/news/${query ? '?' + query : ''}`);
        },

        async getGalleryAlbums(params = {}) {
            const query = new URLSearchParams(params).toString();
            return API.request(`/archive/gallery/albums/${query ? '?' + query : ''}`);
        },

        async getGalleryAlbum(id) {
            return API.request(`/archive/gallery/albums/${id}/`);
        },

        async getVideos(params = {}) {
            const query = new URLSearchParams(params).toString();
            return API.request(`/archive/gallery/videos/${query ? '?' + query : ''}`);
        }
    },

    // === 후원·참여 API ===
    join: {
        async applyVolunteer(data) {
            return API.request('/join/volunteers/apply/', {
                method: 'POST',
                body: JSON.stringify(data)
            });
        },

        async donate(data) {
            return API.request('/join/donations/', {
                method: 'POST',
                body: JSON.stringify(data)
            });
        },

        async registerMember(data) {
            return API.request('/members/register/', {
                method: 'POST',
                body: JSON.stringify(data)
            });
        }
    },

    // === 팝업 API ===
    popup: {
        async getActive() {
            return API.request('/popups/active/');
        }
    }
};

// UI 유틸리티
const UI = {
    // 로딩 오버레이
    showLoading(message = '처리 중...') {
        let overlay = document.getElementById('loading-overlay');
        if (!overlay) {
            overlay = document.createElement('div');
            overlay.id = 'loading-overlay';
            overlay.innerHTML = `
                <div class="loading-content">
                    <div class="loading-spinner"></div>
                    <p class="loading-message">${message}</p>
                </div>
            `;
            document.body.appendChild(overlay);
        } else {
            overlay.querySelector('.loading-message').textContent = message;
            overlay.style.display = 'flex';
        }
    },

    hideLoading() {
        const overlay = document.getElementById('loading-overlay');
        if (overlay) {
            overlay.style.display = 'none';
        }
    },

    // 토스트 메시지
    toast(message, type = 'info', duration = 3000) {
        let container = document.getElementById('toast-container');
        if (!container) {
            container = document.createElement('div');
            container.id = 'toast-container';
            document.body.appendChild(container);
        }

        const toast = document.createElement('div');
        toast.className = `toast toast-${type}`;
        toast.innerHTML = `
            <i class="fas fa-${type === 'success' ? 'check-circle' : type === 'error' ? 'exclamation-circle' : 'info-circle'}"></i>
            <span>${message}</span>
        `;
        container.appendChild(toast);

        setTimeout(() => toast.classList.add('show'), 10);
        setTimeout(() => {
            toast.classList.remove('show');
            setTimeout(() => toast.remove(), 300);
        }, duration);
    },

    // 폼 에러 표시
    showFormErrors(form, errors) {
        // 기존 에러 제거
        form.querySelectorAll('.field-error').forEach(el => el.remove());
        form.querySelectorAll('.error').forEach(el => el.classList.remove('error'));

        // 새 에러 표시
        Object.entries(errors).forEach(([field, messages]) => {
            const input = form.querySelector(`[name="${field}"]`);
            if (input) {
                input.classList.add('error');
                const errorDiv = document.createElement('div');
                errorDiv.className = 'field-error';
                errorDiv.textContent = Array.isArray(messages) ? messages[0] : messages;
                input.parentNode.appendChild(errorDiv);
            }
        });
    },

    // 폼 에러 초기화
    clearFormErrors(form) {
        form.querySelectorAll('.field-error').forEach(el => el.remove());
        form.querySelectorAll('.error').forEach(el => el.classList.remove('error'));
    },

    // 연락처 포맷팅 (하이픈 제거)
    formatPhone(phone) {
        return phone.replace(/[^0-9]/g, '');
    },

    // 날짜 포맷팅
    formatDate(dateString) {
        const date = new Date(dateString);
        return date.toLocaleDateString('ko-KR', {
            year: 'numeric',
            month: 'long',
            day: 'numeric'
        });
    }
};

// CSS 스타일 주입
(function injectStyles() {
    const style = document.createElement('style');
    style.textContent = `
        /* 로딩 오버레이 */
        #loading-overlay {
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: rgba(10, 25, 47, 0.9);
            display: flex;
            justify-content: center;
            align-items: center;
            z-index: 10000;
        }
        .loading-content {
            text-align: center;
            color: #fff;
        }
        .loading-spinner {
            width: 50px;
            height: 50px;
            border: 4px solid rgba(197, 160, 89, 0.3);
            border-top-color: #c5a059;
            border-radius: 50%;
            animation: spin 1s linear infinite;
            margin: 0 auto 20px;
        }
        @keyframes spin {
            to { transform: rotate(360deg); }
        }
        .loading-message {
            font-size: 1.1rem;
            color: #c5a059;
        }

        /* 토스트 */
        #toast-container {
            position: fixed;
            top: 100px;
            right: 20px;
            z-index: 10001;
        }
        .toast {
            display: flex;
            align-items: center;
            gap: 10px;
            padding: 15px 20px;
            margin-bottom: 10px;
            border-radius: 8px;
            color: #fff;
            font-size: 0.95rem;
            transform: translateX(120%);
            transition: transform 0.3s ease;
            box-shadow: 0 4px 15px rgba(0,0,0,0.2);
        }
        .toast.show {
            transform: translateX(0);
        }
        .toast-success { background: #28a745; }
        .toast-error { background: #dc3545; }
        .toast-info { background: #0a192f; border: 1px solid #c5a059; }

        /* 폼 에러 */
        .field-error {
            color: #dc3545;
            font-size: 0.85rem;
            margin-top: 5px;
        }
        input.error, select.error, textarea.error {
            border-color: #dc3545 !important;
        }
    `;
    document.head.appendChild(style);
})();

// YugwanAPI alias (프론트엔드 페이지에서 사용)
const YugwanAPI = {
    ...API,
    getApiUrl(path) {
        return API.BASE_URL + path;
    },
    setToken(token) {
        localStorage.setItem('access_token', token);
    },
    getToken: API.getToken.bind(API),
    clearToken: API.clearToken.bind(API)
};

// 헤더 로그인 버튼 동적 업데이트
document.addEventListener('DOMContentLoaded', function() {
    updateHeaderAuthButton();
});

function updateHeaderAuthButton() {
    const btnLogin = document.getElementById('btnLoginHeader');
    if (!btnLogin) return;

    if (API.auth.isLoggedIn()) {
        // 로그인된 상태 - 마이페이지로 변경
        const cachedUser = localStorage.getItem('yugwan_user');
        let userName = '마이페이지';
        if (cachedUser) {
            try {
                const user = JSON.parse(cachedUser);
                userName = user.first_name || user.username || '마이페이지';
            } catch (e) {}
        }
        btnLogin.textContent = userName;
        btnLogin.href = 'join/mypage.html';

        // 상대경로 조정 (서브 디렉토리에서 접근 시)
        if (window.location.pathname.includes('/join/') ||
            window.location.pathname.includes('/about/') ||
            window.location.pathname.includes('/contest/') ||
            window.location.pathname.includes('/projects/') ||
            window.location.pathname.includes('/global/') ||
            window.location.pathname.includes('/archive/')) {
            btnLogin.href = 'mypage.html';
            if (!window.location.pathname.includes('/join/')) {
                btnLogin.href = '../join/mypage.html';
            }
        }
    } else {
        // 로그아웃 상태 - 로그인으로 표시
        btnLogin.textContent = '로그인';
        btnLogin.href = 'join/login.html';

        // 상대경로 조정
        if (window.location.pathname.includes('/join/') ||
            window.location.pathname.includes('/about/') ||
            window.location.pathname.includes('/contest/') ||
            window.location.pathname.includes('/projects/') ||
            window.location.pathname.includes('/global/') ||
            window.location.pathname.includes('/archive/')) {
            btnLogin.href = 'login.html';
            if (!window.location.pathname.includes('/join/')) {
                btnLogin.href = '../join/login.html';
            }
        }
    }
}
