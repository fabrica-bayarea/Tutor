import { io } from "socket.io-client";

const SOCKET_URL = process.env.NEXT_PUBLIC_API_URL_RUNTIME ?? "http://localhost:5000";

const socket = io(SOCKET_URL, {
    autoConnect: false,
    transports: ["websocket"],
    // Envia o cookie de sessão (httponly) no handshake para o backend autenticar.
    withCredentials: true,
});

export default socket;