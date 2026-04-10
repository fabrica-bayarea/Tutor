export function middleware(request: NextRequest) {
  const token = request.cookies.get("token")?.value 
  const { pathname } = request.nextUrl

  const publicRoutes = ["/login", "/register"]

  const isPublic = publicRoutes.some(route => pathname.startsWith(route))

  if (isPublic) {
    return NextResponse.next()
  }

  if (!token) {
    return NextResponse.redirect(new URL("/login", request.url))
  }

  return NextResponse.next()
}

export const config = {
  matcher: ["/((?!_next).*)"],
}
