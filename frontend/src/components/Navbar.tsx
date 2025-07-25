'use client'
import Link from 'next/link'
import { usePathname } from 'next/navigation'
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
    <nav className="bg-black text-white px-6 py-3 flex gap-6">
      {navItems.map(({ href, label }) => (
        <Link
          key={href}
          href={href}
          className={clsx(
            'hover:text-blue-400 transition',
            pathname === href && 'font-semibold underline'
          )}
        >
          {label}
        </Link>
      ))}
    </nav>
  )
}
