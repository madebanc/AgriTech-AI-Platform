/**
 * sw.js — AgriTech AI Platform Service Worker
 * Author : Daniel Oyanogbezina
 * Day 12 : Enables offline access and faster loading
 * Day 14 : Adds journal
 * Day 15 : New input helpers stay cached page to offline cache
 *
 * How it works:
 * 1. On install — downloads and caches all app files
 * 2. On fetch   — serves cached files when offline
 * 3. On activate — removes old cached versions
 */

const CACHE_NAME    = 'agritech-ai-v10';
const OFFLINE_URL   = '/AgriTech-AI-Platform/index.html';

// Files to cache on install (the entire app shell)
const CACHE_FILES = [
  '/AgriTech-AI-Platform/',
  '/AgriTech-AI-Platform/index.html',
  '/AgriTech-AI-Platform/analytics.html',
  '/AgriTech-AI-Platform/disease.html',
  '/AgriTech-AI-Platform/journal.html',
  '/AgriTech-AI-Platform/css/style.css',
  '/AgriTech-AI-Platform/js/app.js',
  '/AgriTech-AI-Platform/js/analytics.js',
  '/AgriTech-AI-Platform/js/disease.js',
  '/AgriTech-AI-Platform/js/journal.js',
  '/AgriTech-AI-Platform/js/translations.js',
  '/AgriTech-AI-Platform/icons/icon.svg',
  '/AgriTech-AI-Platform/manifest.json',
];

// External resources to cache (CDN)
const EXTERNAL_CACHE = [
  'https://cdn.jsdelivr.net/npm/chart.js@4.4.0/dist/chart.umd.min.js',
];

// ── Install: cache everything ───────────────────────────────
self.addEventListener('install', event => {
  console.log('[SW] Installing AgriTech AI service worker...');

  event.waitUntil(
    caches.open(CACHE_NAME).then(cache => {
      console.log('[SW] Caching app shell and assets');
      return cache.addAll([...CACHE_FILES, ...EXTERNAL_CACHE]);
    }).then(() => {
      console.log('[SW] All files cached successfully');
      return self.skipWaiting();
    }).catch(err => {
      console.error('[SW] Cache failed:', err);
    })
  );
});

// ── Activate: clean up old caches ──────────────────────────
self.addEventListener('activate', event => {
  console.log('[SW] Activating new service worker...');

  event.waitUntil(
    caches.keys().then(cacheNames => {
      return Promise.all(
        cacheNames
          .filter(name => name !== CACHE_NAME)
          .map(name => {
            console.log('[SW] Deleting old cache:', name);
            return caches.delete(name);
          })
      );
    }).then(() => {
      console.log('[SW] Service worker activated');
      return self.clients.claim();
    })
  );
});

// ── Fetch: serve from cache, fall back to network ──────────
self.addEventListener('fetch', event => {
  const url = new URL(event.request.url);

  if (event.request.method !== 'GET') return;
  if (url.protocol === 'chrome-extension:') return;

  if (url.hostname.includes('onrender.com') ||
      url.hostname.includes('open-meteo.com')) {
    event.respondWith(
      fetch(event.request).catch(() => {
        return new Response(
          JSON.stringify({
            success:  false,
            offline:  true,
            message:  'You are offline. Connect to internet to get live predictions.',
          }),
          {
            status:  503,
            headers: { 'Content-Type': 'application/json' },
          }
        );
      })
    );
    return;
  }

  event.respondWith(
    caches.match(event.request).then(cachedResponse => {
      if (cachedResponse) {
        const fetchPromise = fetch(event.request).then(networkResponse => {
          if (networkResponse && networkResponse.status === 200) {
            const responseClone = networkResponse.clone();
            caches.open(CACHE_NAME).then(cache => {
              cache.put(event.request, responseClone);
            });
          }
          return networkResponse;
        }).catch(() => null);

        return cachedResponse;
      }

      return fetch(event.request).then(networkResponse => {
        if (!networkResponse || networkResponse.status !== 200) {
          return networkResponse;
        }

        const responseClone = networkResponse.clone();
        caches.open(CACHE_NAME).then(cache => {
          cache.put(event.request, responseClone);
        });

        return networkResponse;

      }).catch(() => {
        if (event.request.destination === 'document') {
          return caches.match(OFFLINE_URL);
        }
        return new Response('Offline', { status: 503 });
      });
    })
  );
});

// ── Message handler: manual cache refresh ──────────────────
self.addEventListener('message', event => {
  if (event.data && event.data.type === 'SKIP_WAITING') {
    self.skipWaiting();
  }

  if (event.data && event.data.type === 'CACHE_REFRESH') {
    caches.open(CACHE_NAME).then(cache => {
      CACHE_FILES.forEach(url => {
        fetch(url).then(response => {
          if (response.ok) cache.put(url, response);
        });
      });
    });
    console.log('[SW] Cache refreshed manually');
  }
});