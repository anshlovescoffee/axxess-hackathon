import Link from "next/link"
import { Button } from "@/components/ui/button"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { MainNav } from "@/components/main-nav"
import { ClipboardList, Package } from "lucide-react"

export default function Home() {
  return (
    <div className="flex min-h-screen flex-col">
      <header className="sticky top-0 z-50 w-full border-b bg-background/95 backdrop-blur supports-[backdrop-filter]:bg-background/60">
        <div className="container flex h-14 items-center">
          <MainNav />
        </div>
      </header>
      <main className="flex-1">
        <section className="space-y-6 pb-8 pt-6 md:pb-12 md:pt-10 lg:py-32">
          <div className="container flex max-w-[64rem] flex-col items-center gap-4 text-center">
            <h1 className="text-3xl sm:text-5xl md:text-6xl lg:text-7xl font-bold">Welcome to Axxess Health Portal</h1>
            <p className="max-w-[42rem] leading-normal text-muted-foreground sm:text-xl sm:leading-8">
              Efficiently manage patient care and inventory with our comprehensive healthcare management system
            </p>
          </div>
        </section>
        <section className="container space-y-6 py-8 md:py-12 lg:py-24">
          <div className="mx-auto grid justify-center gap-4 sm:grid-cols-2 md:max-w-[64rem] -mt-[150px]">
            <Card>
              <CardHeader>
                <ClipboardList className="h-14 w-14 text-blue-500" />
                <CardTitle>Patient Management</CardTitle>
                <CardDescription>Comprehensive patient information and history tracking</CardDescription>
              </CardHeader>
              <CardContent>
                <Link href="/patients">
                  <Button variant="secondary" className="w-full">
                    View Patients
                  </Button>
                </Link>
              </CardContent>
            </Card>
            <Card>
              <CardHeader>
                <Package className="h-14 w-14 text-purple-500" />
                <CardTitle>Inventory Control</CardTitle>
                <CardDescription>Track and manage medical supplies and equipment</CardDescription>
              </CardHeader>
              <CardContent>
                <Link href="/inventory">
                  <Button variant="secondary" className="w-full">
                    Manage Inventory
                  </Button>
                </Link>
              </CardContent>
            </Card>
          </div>
        </section>
      </main>
    </div>
  )
}

