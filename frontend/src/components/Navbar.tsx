'use client'
import Link from 'next/link'
import { usePathname } from 'next/navigation'
import { BarChart3 } from 'lucide-react'
import clsx from 'clsx'

const navItems = [
  { href: '/', label: 'Home' },
  { href: '/trends-ai', label: '📊 Trends AI' },
  { href: '/insight-vault', label: '📁 InsightVault' },
  { href: '/chatbot', label: '🤖 Chatbot' },
]

export default function Navbar() {
  const pathname = usePathname()

  return (
    <nav className="bg-white shadow-sm border-b border-gray-200 sticky top-0 z-50">
      <div className="max-w-7xl mx-auto px-6">
        <div className="flex items-center justify-between h-16">
          
          {/* Left Side: Brand/Logo */}
          <div className="flex-shrink-0">
            <Link href="/" className="flex items-center gap-2">
              <BarChart3 className="h-7 w-7 text-blue-600" />
              <span className="font-bold text-xl text-gray-800 tracking-tight">
                AlphaLens
              </span>
            </Link>
          </div>

          {/* Right Side: Navigation Links */}
          <div className="hidden md:flex md:items-center md:space-x-2">
            {navItems.map(({ href, label }) => {
              const isActive = (href === '/' && pathname === '/') || (href !== '/' && pathname.startsWith(href));

              return (
                <Link
                  key={href}
                  href={href}
                  className={clsx(
                    'px-3 py-2 rounded-md text-sm font-medium transition-colors duration-200 flex items-center gap-2',
                    {
                      'bg-blue-50 text-blue-600': isActive,
                      'text-gray-600 hover:bg-gray-100 hover:text-gray-900': !isActive,
                    }
                  )}
                  aria-current={isActive ? 'page' : undefined}
                >
                  {label}
                </Link>
              );
            })}
          </div>

        </div>
      </div>
    </nav>
  )
}