"use client";

import Link from 'next/link';

export default function Header() {
  return (
    <header className="bg-black/80 backdrop-blur-lg border-b border-cyan-500/30 shadow-2xl">
      <div className="container mx-auto px-6 py-6">
        <div className="flex items-center justify-between">
          <div className="flex items-center space-x-4">
            <div className="flex items-center space-x-3">
              <div className="w-10 h-10 bg-cyan-600 rounded-xl flex items-center justify-center shadow-lg">
                <svg className="w-6 h-6 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9.663 17h4.673M12 3v1m6.364 1.636l-.707.707M21 12h-1M4 12H3m3.343-5.657l-.707-.707m2.828 9.9a5 5 0 117.072 0l-.548.547A3.374 3.374 0 0014 18.469V19a2 2 0 11-4 0v-.531c0-.895-.356-1.754-.988-2.386l-.548-.547z" />
                </svg>
              </div>
              <h1 className="text-2xl font-bold text-white tracking-wide drop-shadow-lg">Multi-Agent AI</h1>
            </div>
          </div>
          
          <nav className="hidden md:flex items-center space-x-8">
            <Link href="/" className="text-white hover:text-cyan-300 transition-all duration-300 font-medium drop-shadow-md">
              Dashboard
            </Link>
            <Link href="/agents" className="text-white hover:text-cyan-300 transition-all duration-300 font-medium drop-shadow-md">
              Agents
            </Link>
            <Link href="/docs" className="text-white hover:text-cyan-300 transition-all duration-300 font-medium drop-shadow-md">
              Documentation
            </Link>
          </nav>

          <div className="flex items-center space-x-6">
            <div className="hidden sm:flex items-center space-x-3 text-sm text-white">
              <div className="w-3 h-3 bg-green-400 rounded-full shadow-lg shadow-green-400/50"></div>
              <span className="font-medium drop-shadow-md">System Online</span>
            </div>
            <button className="bg-cyan-600 text-white px-6 py-3 rounded-xl hover:bg-cyan-700 transition-all duration-300 font-medium shadow-lg hover:shadow-cyan-500/25">
              Get Started
            </button>
          </div>
        </div>
      </div>
    </header>
  );
}
