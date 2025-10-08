import { io } from "socket.io-client"

const API_URL = process.env.NEXT_PUBLIC_API_URL || '__API_URL_PLACEHOLDER__';

const socket = io(API_URL)

export default socket
