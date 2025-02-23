"use client"

import Link from "next/link"
import { usePathname } from "next/navigation"
import { cn } from "@/lib/utils"
import { Button } from "@/components/ui/button"
import { Home, Users, Package } from "lucide-react"

const routes = [
  {
    label: "Home",
    icon: Home,
    href: "/",
    color: "text-sky-500",
  },
  {
    label: "Patients",
    icon: Users,
    href: "/patients",
    color: "text-violet-500",
  },
  {
    label: "Inventory",
    icon: Package,
    href: "/inventory",
    color: "text-purple-500",
  },
]

export function MainNav() {
  const pathname = usePathname()

  return (
    <nav className="flex items-center space-x-4 lg:space-x-6">
      {routes.map((route) => (
        <Button
          key={route.href}
          variant={pathname === route.href ? "secondary" : "ghost"}
          className={cn("w-full justify-start", pathname === route.href && "bg-muted")}
          asChild
        >
          <Link href={route.href} className="flex items-center gap-x-2">
            <route.icon className={cn("h-5 w-5", route.color)} />
            {route.label}
          </Link>
        </Button>
      ))}
    </nav>
  )
}

