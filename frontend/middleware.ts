// "use client";

import { NextResponse } from 'next/server'
import type { NextRequest } from 'next/server'
// import { useAuth } from './utils/auth';

export function middleware(request: NextRequest) {
//   const token = request.cookies.get("token")?.value;
//   const { pathname } = request.nextUrl;
//   const { isAdmin, isStudent, isProfessor } = useAuth();

//   // let routeType: 'public' | 'admin' | 'professor' | 'chat' = 'public';

//   // if (pathname.startsWith('/login') || pathname.startsWith('/register')) {
//   //   routeType = 'public';
//   // } else if (pathname.startsWith('/admin')) {
//   //   routeType = 'admin';
//   // } else if (pathname.startsWith('/professor')) {
//   //   routeType = 'professor';
//   // } else if (pathname.startsWith('/chat')) {
//   //   routeType = 'chat';
//   // } else {
//   //   routeType = 'public';
//   // }

//   // if (routeType === 'public') {
//   //   return NextResponse.next();
//   // }

//   // if (!token) {
//   //   const loginUrl = new URL("/login", request.url);
//   //   loginUrl.searchParams.set("returnTo", pathname);
//   //   return NextResponse.redirect(loginUrl);
//   // }

//   // let allowed = false;

//   // if (routeType === 'admin' && isAdmin) allowed = true;
//   // if (routeType === 'professor' && isProfessor) allowed = true;
//   // if (routeType === 'chat' && (isStudent || isAdmin)) allowed = true;

//   // if (!allowed) {
//   //   const unauthorizedUrl = new URL('/unauthorized', request.url);
//   //   return NextResponse.redirect(unauthorizedUrl);
//   // }

  return NextResponse.next();
}
// }

