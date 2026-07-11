// src/app/api/backend/[...path]/route.ts
//
// API Route proxy — berjalan di Next.js server (runtime), bukan browser.
// Semua request ke /api/backend/* di-forward ke backend FastAPI container.
//
// Karena ini runtime code, env var BACKEND_URL dari docker-compose terbaca
// saat server start — tidak perlu di-bake ke bundle saat build.

import { NextRequest, NextResponse } from "next/server";

// URL backend dibaca saat runtime dari environment variable
const BACKEND_URL =
  process.env.BACKEND_URL ||         // set di docker-compose: http://backend:8000
  "http://backend:8000";             // default Docker internal hostname

async function proxyRequest(
  request: NextRequest,
  { params }: { params: Promise<{ path: string[] }> }
): Promise<NextResponse> {
  const { path } = await params;
  const targetPath = path.join("/");

  // Reconstruct query string
  const searchParams = request.nextUrl.searchParams.toString();
  const queryString = searchParams ? `?${searchParams}` : "";

  const targetUrl = `${BACKEND_URL}/${targetPath}${queryString}`;

  // Forward headers (kecuali host)
  const headers = new Headers(request.headers);
  headers.delete("host");

  let body: BodyInit | null = null;
  if (!["GET", "HEAD"].includes(request.method)) {
    body = await request.text();
  }

  try {
    const backendResponse = await fetch(targetUrl, {
      method: request.method,
      headers,
      body,
    });

    // Forward response headers
    const responseHeaders = new Headers(backendResponse.headers);
    // Hapus encoding header agar tidak double-encode
    responseHeaders.delete("content-encoding");
    responseHeaders.delete("transfer-encoding");

    const responseBody = await backendResponse.text();

    return new NextResponse(responseBody, {
      status: backendResponse.status,
      headers: responseHeaders,
    });
  } catch (error) {
    console.error(`[Proxy] Error forwarding to ${targetUrl}:`, error);
    return NextResponse.json(
      { error: "Backend tidak dapat dijangkau", detail: String(error) },
      { status: 502 }
    );
  }
}

export const GET = proxyRequest;
export const POST = proxyRequest;
export const PUT = proxyRequest;
export const PATCH = proxyRequest;
export const DELETE = proxyRequest;
export const OPTIONS = proxyRequest;
