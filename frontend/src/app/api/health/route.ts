import { NextResponse } from 'next/server';

export async function GET() {
  return NextResponse.json({
    status: 'healthy',
    timestamp: new Date().toISOString(),
    system: 'multi_agent_ai_unified',
    version: '2.0.0',
    environment: process.env.NODE_ENV || 'development'
  });
}
