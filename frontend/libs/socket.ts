import { io } from "socket.io-client";

const API_URL = process.env.NEXT_PUBLIC_API_URL_RUNTIME ?? "http://localhost:5000";

// Derive the Socket.IO path from the API URL.
// - Production (https://bayarea.dataiesb.com/tutor/api) → path: /tutor/socket.io/
// - Development (http://localhost:5000) → path: /socket.io/
function getSocketPath(apiUrl: string): string {
    try {
        const url = new URL(apiUrl);
        // Remove trailing segments like "/api" to get the base prefix
        const segments = url.pathname.replace(/\/+$/, "").split("/").filter(Boolean);
        // Remove the last segment if it looks like an API suffix (e.g. "api")
        if (segments.length > 0 && segments[segments.length - 1].toLowerCase() === "api") {
            segments.pop();
        }
        const prefix = segments.length > 0 ? `/${segments.join("/")}` : "";
        return `${prefix}/socket.io/`;
    } catch {
        return "/socket.io/";
    }
}

const socket = io(API_URL, {
    autoConnect: false,
    transports: ["polling"],
    upgrade: false,
    path: getSocketPath(API_URL),
    withCredentials: true,
});

export default socket;
