const PRECACHE = "precache-v2";
const PRECACHE_URLS = [
    "icons/192.png",
    "minireset.min.css",
    "Pretendard.css",
    "Pretendard/ExtraLight.woff2",
    "Pretendard/Light.woff2",
    "Pretendard/Regular.woff2",
    "Pretendard/SemiBold.woff2",
    "cache.html",
];

const RUNTIME = "runtime-v2";

self.addEventListener("install", (event) => {
    event.waitUntil(
        caches
            .open(PRECACHE)
            .then((cache) => cache.addAll(PRECACHE_URLS))
            .then(self.skipWaiting())
    );
});

self.addEventListener("activate", (event) => {
    const currentCaches = [PRECACHE, RUNTIME];
    event.waitUntil(
        caches
            .keys()
            .then((cache_keys) => {
                return cache_keys.filter((key) => !currentCaches.includes(key));
            })
            .then((delete_keys) => {
                return Promise.all(
                    delete_keys.map((key) => {
                        return caches.delete(key);
                    })
                );
            })
            .then(() => self.clients.claim())
    );
});

self.addEventListener("fetch", (event) => {
    if (event.request.url.startsWith(self.location.origin) && event.request.url.includes("assets")) {
        event.respondWith(
            caches.match(event.request).then((cachedResponse) => {
                if (cachedResponse) {
                    return cachedResponse;
                }

                return caches.open(RUNTIME).then((cache) => {
                    return fetch(event.request).then((response) => {
                        return cache.put(event.request, response.clone()).then(() => {
                            return response;
                        });
                    });
                });
            })
        );
    }
});
