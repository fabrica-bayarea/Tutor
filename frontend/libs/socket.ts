import { io } from "socket.io-client";

const API_URL = process.env.NEXT_PUBLIC_API_URL_RUNTIME ?? "http://localhost:5000";

/**
 * Derives the Socket.IO connection origin and path from the API URL.
 *
 * - Dev:  http://localhost:5000        → origin: http://localhost:5000,  path: /socket.io/
 * - Prod: https://bayarea.dataiesb.com/tutor/api → origin: https://bayarea.dataiesb.com, path: /tutor/socket.io/
 */
function getSocketConfig(apiUrl: string): { origin: string; path: string } {
    try {
        const url = new URL(apiUrl);
        const origin = url.origin;

        // Remove trailing slashes and split path segments
        const segments = url.pathname.replace(/\/+$/, "").split("/").filter(Boolean);
        // Remove the last segment if it's "api" (it's the REST prefix, not relevant for socket)
        if (segments.length > 0 && segments[segments.length - 1].toLowerCase() === "api") {
            segments.pop();
        }
        const prefix = segments.length > 0 ? `/${segments.join("/")}` : "";
        const path = `${prefix}/socket.io/`;

        return { origin, path };
    } catch {
        return { origin: "http://localhost:5000", path: "/socket.io/" };
    }
}

const { origin, path } = getSocketConfig(API_URL);

const socket = io(origin, {
    autoConnect: false,
    transports: ["polling"],
    upgrade: false,
    path,
    withCredentials: true,
});

export default socket;
