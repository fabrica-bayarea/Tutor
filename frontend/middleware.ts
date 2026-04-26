import { NextResponse } from 'next/server'
import type { NextRequest } from 'next/server'

export function middleware(request: NextRequest) {
  const token = request.cookies.get("token")?.value;
  // const { pathname } = request.nextUrl;

  // const isPublicRoute =
  //   pathname.startsWith("/login") ||
  //   pathname.startsWith("/register");

  // if (isPublicRoute) {
  //   if (token) {
  //     return NextResponse.redirect(new URL("/chat", request.url));
  //   }

  //   return NextResponse.next();
  // }

  // if (!token) {
  //   const loginUrl = new URL("/login", request.url);
  //   loginUrl.searchParams.set("returnTo", pathname);
  //   return NextResponse.redirect(loginUrl);
  // }

  return NextResponse.next();
}

export const config = {
  matcher: ["/((?!_next|favicon.ico).*)"],
};
