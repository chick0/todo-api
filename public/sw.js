const PRECACHE = "precache-v3";
const PRECACHE_URLS = [
    "/icons/192.png",
    "/minireset.min.css",
    "/Pretendard.css",
    "/Pretendard/Regular.woff2",
    "/Pretendard/SemiBold.woff2",
    "/cache.html",
];

const RUNTIME = "runtime-{tag}";

self.addEventListener("install", (event) => {
    console.log("install");
    event.waitUntil(
        caches
            .open(PRECACHE)
            .then((cache) => cache.addAll(PRECACHE_URLS))
            .then(self.skipWaiting())
    );
});

self.addEventListener("activate", (event) => {
    console.log("activate");
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
    if (event.request.url.startsWith(self.location.origin)) {
        event.respondWith(
            caches.match(event.request).then((cachedResponse) => {
                if (cachedResponse) {
                    console.log("@", event.request.url);
                    return cachedResponse;
                } else {
                    console.log(" ", event.request.url);
                }

                if (event.request.url.includes("assets")) {
                    return caches.open(RUNTIME).then((cache) => {
                        return fetch(event.request).then((response) => {
                            return cache.put(event.request, response.clone()).then(() => {
                                return response;
                            });
                        });
                    });    
                } else {
                    return fetch(event.request).then((response) => {
                        return response;
                    });
                }
            })
        );
    } else {
        console.log("C", event.request.url);
    }
});
