"use client"

import { useEffect, useState } from "react"
import { useRouter } from "next/navigation"
import { getUser, getAccessToken, clearAuth } from "@/lib/api"
import type { Usuario } from "@/lib/api"
import { Button } from "@/components/ui/button"
import { Calendar, LogOut } from "lucide-react"

export default function DashboardPage() {
  const router = useRouter()
  const [user, setUser] = useState<Usuario | null>(null)

  useEffect(() => {
    const token = getAccessToken()
    const userData = getUser()

    if (!token || !userData) {
      router.push("/login")
      return
    }

    setUser(userData)
  }, [router])

  const handleLogout = () => {
    clearAuth()
    router.push("/login")
  }

  if (!user) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-primary" />
      </div>
    )
  }

  return (
    <div className="min-h-screen bg-background">
      {/* Header */}
      <header className="border-b border-border bg-card">
        <div className="container mx-auto px-4 h-16 flex items-center justify-between">
          <div className="flex items-center gap-2">
            <Calendar className="w-6 h-6 text-primary" />
            <span className="font-bold text-xl">EventSync</span>
          </div>
          <Button variant="ghost" size="sm" onClick={handleLogout}>
            <LogOut className="w-4 h-4 mr-2" />
            Sair
          </Button>
        </div>
      </header>

      {/* Main Content */}
      <main className="container mx-auto px-4 py-8">
        <div className="max-w-4xl mx-auto">
          <div className="bg-card border border-border rounded-xl p-6 md:p-8">
            <h1 className="text-3xl font-bold mb-2">Olá, {user.username}!</h1>
            <p className="text-muted-foreground mb-6">Bem-vindo ao seu dashboard do EventSync</p>

            <div className="grid gap-4 md:grid-cols-2">
              <div className="p-4 bg-muted rounded-lg">
                <p className="text-sm text-muted-foreground">Email</p>
                <p className="font-medium">{user.email}</p>
              </div>

              <div className="p-4 bg-muted rounded-lg">
                <p className="text-sm text-muted-foreground">Papel</p>
                <p className="font-medium capitalize">{user.papel}</p>
              </div>

              <div className="p-4 bg-muted rounded-lg">
                <p className="text-sm text-muted-foreground">Cidade</p>
                <p className="font-medium">{user.cidade}</p>
              </div>

              <div className="p-4 bg-muted rounded-lg">
                <p className="text-sm text-muted-foreground">ID do Usuário</p>
                <p className="font-medium">{user.id}</p>
              </div>
            </div>

            <div className="mt-8 p-6 bg-primary/5 border border-primary/20 rounded-lg">
              <h2 className="font-semibold text-lg mb-2">Dashboard em Construção</h2>
              <p className="text-sm text-muted-foreground">
                Esta é uma página temporária. As funcionalidades de gerenciamento de eventos serão implementadas nas
                próximas etapas do projeto.
              </p>
            </div>
          </div>
        </div>
      </main>
    </div>
  )
}
